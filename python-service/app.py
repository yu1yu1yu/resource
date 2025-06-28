#!/usr/bin/env python3
"""
Flask应用主入口文件
"""
import os
import signal
import sys
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, jwt
from app.api import api_bp
from app.auth import auth_bp
from app.monitoring import monitoring_bp
from app.utils.logger import setup_logging
from app.utils.nacos_client import init_nacos_client, get_nacos_client


def create_app(config_class=Config):
    """
    应用工厂函数
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    initialize_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 设置CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 设置日志
    setup_logging()
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 初始化Nacos客户端
    init_nacos_client(config_class)
    
    return app


def initialize_extensions(app):
    """初始化Flask扩展"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')


def register_error_handlers(app):
    """注册错误处理器"""
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)


def register_service_to_nacos():
    """注册服务到Nacos"""
    nacos_client = get_nacos_client()
    if nacos_client:
        success = nacos_client.register_service()
        if success:
            nacos_client.start_heartbeat()
            print(f"✅ 服务已注册到Nacos: {nacos_client.service_name}")
        else:
            print("❌ 服务注册到Nacos失败")
    else:
        print("⚠️ Nacos客户端未初始化")


def deregister_service_from_nacos():
    """从Nacos注销服务"""
    nacos_client = get_nacos_client()
    if nacos_client:
        nacos_client.stop_heartbeat()
        success = nacos_client.deregister_service()
        if success:
            print(f"✅ 服务已从Nacos注销: {nacos_client.service_name}")
        else:
            print("❌ 服务从Nacos注销失败")
    else:
        print("⚠️ Nacos客户端未初始化")


def signal_handler(signum, frame):
    """信号处理器，用于优雅关闭"""
    print("\n🛑 接收到关闭信号，正在优雅关闭...")
    deregister_service_from_nacos()
    sys.exit(0)


if __name__ == '__main__':
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    app = create_app()
    
    # 注册服务到Nacos
    register_service_to_nacos()
    
    try:
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('FLASK_ENV') == 'development'
        )
    except KeyboardInterrupt:
        print("\n🛑 用户中断，正在关闭...")
    finally:
        deregister_service_from_nacos() 