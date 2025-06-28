"""
应用配置管理
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    FLASK_ENV: str = Field(default="development", env="FLASK_ENV")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # 数据库配置
    DATABASE_URL: str = Field(
        default="sqlite:///app.db", 
        env="DATABASE_URL"
    )
    
    # Redis配置
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0", 
        env="REDIS_URL"
    )
    
    # JWT配置
    JWT_SECRET_KEY: str = Field(
        default="jwt-secret-key", 
        env="JWT_SECRET_KEY"
    )
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(
        default=3600,  # 1小时
        env="JWT_ACCESS_TOKEN_EXPIRES"
    )
    
    # Nacos服务发现配置
    NACOS_SERVER_ADDR: str = Field(
        default="127.0.0.1:8848", 
        env="NACOS_SERVER_ADDR"
    )
    NACOS_NAMESPACE: str = Field(
        default="public", 
        env="NACOS_NAMESPACE"
    )
    NACOS_GROUP: str = Field(
        default="DEFAULT_GROUP", 
        env="NACOS_GROUP"
    )
    NACOS_SERVICE_NAME: str = Field(
        default="flask-api", 
        env="NACOS_SERVICE_NAME"
    )
    NACOS_SERVICE_IP: str = Field(
        default="127.0.0.1", 
        env="NACOS_SERVICE_IP"
    )
    NACOS_SERVICE_PORT: int = Field(
        default=5000, 
        env="NACOS_SERVICE_PORT"
    )
    NACOS_HEARTBEAT_INTERVAL: int = Field(
        default=5, 
        env="NACOS_HEARTBEAT_INTERVAL"
    )
    NACOS_DEREGISTER_TIME: int = Field(
        default=10, 
        env="NACOS_DEREGISTER_TIME"
    )
    
    # API配置
    API_TITLE: str = Field(default="Flask API", env="API_TITLE")
    API_VERSION: str = Field(default="1.0.0", env="API_VERSION")
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # CORS配置
    CORS_ORIGINS: str = Field(default="*", env="CORS_ORIGINS")
    
    # 监控配置
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    DATABASE_URL = "sqlite:///dev.db"
    LOG_LEVEL = "DEBUG"
    NACOS_SERVICE_NAME = "flask-api-dev"


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    NACOS_SERVICE_NAME = "flask-api-prod"
    
    @property
    def DATABASE_URL(self) -> str:
        """生产环境数据库URL"""
        return os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DATABASE_URL = "sqlite:///test.db"
    WTF_CSRF_ENABLED = False
    NACOS_SERVICE_NAME = "flask-api-test"


# 配置映射
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 