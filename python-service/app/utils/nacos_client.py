"""
Nacos服务发现客户端
"""
import socket
import threading
import time
import logging
from typing import Optional, Dict, Any
from nacos import NacosClient
from app.config import Config

logger = logging.getLogger(__name__)


class NacosServiceRegistry:
    """Nacos服务注册器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = NacosClient(
            server_addresses=config.NACOS_SERVER_ADDR,
            namespace=config.NACOS_NAMESPACE,
            username="nacos",  # 默认用户名
            password="nacos"   # 默认密码
        )
        self.service_name = config.NACOS_SERVICE_NAME
        self.service_ip = config.NACOS_SERVICE_IP
        self.service_port = config.NACOS_SERVICE_PORT
        self.heartbeat_thread = None
        self.is_registered = False
        
    def get_local_ip(self) -> str:
        """获取本机IP地址"""
        try:
            # 创建一个UDP套接字
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接一个外部地址（不需要真实连接）
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def register_service(self) -> bool:
        """注册服务到Nacos"""
        try:
            # 获取本机IP
            service_ip = self.get_local_ip()
            
            # 服务元数据
            metadata = {
                "version": self.config.API_VERSION,
                "weight": 1,
                "enabled": True,
                "healthy": True,
                "ephemeral": True
            }
            
            # 注册服务
            success = self.client.add_naming_instance(
                service_name=self.service_name,
                ip=service_ip,
                port=self.service_port,
                cluster_name="DEFAULT",
                metadata=metadata
            )
            
            if success:
                self.is_registered = True
                logger.info(f"服务注册成功: {self.service_name} -> {service_ip}:{self.service_port}")
                return True
            else:
                logger.error(f"服务注册失败: {self.service_name}")
                return False
                
        except Exception as e:
            logger.error(f"服务注册异常: {str(e)}")
            return False
    
    def deregister_service(self) -> bool:
        """从Nacos注销服务"""
        try:
            service_ip = self.get_local_ip()
            
            success = self.client.remove_naming_instance(
                service_name=self.service_name,
                ip=service_ip,
                port=self.service_port,
                cluster_name="DEFAULT"
            )
            
            if success:
                self.is_registered = False
                logger.info(f"服务注销成功: {self.service_name}")
                return True
            else:
                logger.error(f"服务注销失败: {self.service_name}")
                return False
                
        except Exception as e:
            logger.error(f"服务注销异常: {str(e)}")
            return False
    
    def heartbeat(self):
        """心跳检测线程"""
        while self.is_registered:
            try:
                service_ip = self.get_local_ip()
                
                # 发送心跳
                self.client.send_heartbeat(
                    service_name=self.service_name,
                    ip=service_ip,
                    port=self.service_port,
                    cluster_name="DEFAULT"
                )
                
                logger.debug(f"心跳发送成功: {self.service_name}")
                time.sleep(self.config.NACOS_HEARTBEAT_INTERVAL)
                
            except Exception as e:
                logger.error(f"心跳发送失败: {str(e)}")
                time.sleep(self.config.NACOS_HEARTBEAT_INTERVAL)
    
    def start_heartbeat(self):
        """启动心跳线程"""
        if self.heartbeat_thread is None or not self.heartbeat_thread.is_alive():
            self.heartbeat_thread = threading.Thread(target=self.heartbeat, daemon=True)
            self.heartbeat_thread.start()
            logger.info("心跳线程已启动")
    
    def stop_heartbeat(self):
        """停止心跳线程"""
        self.is_registered = False
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=5)
            logger.info("心跳线程已停止")
    
    def get_service_instances(self, service_name: str) -> list:
        """获取服务实例列表"""
        try:
            instances = self.client.list_naming_instance(service_name)
            return instances
        except Exception as e:
            logger.error(f"获取服务实例失败: {str(e)}")
            return []
    
    def get_service_info(self) -> Dict[str, Any]:
        """获取当前服务信息"""
        return {
            "service_name": self.service_name,
            "service_ip": self.get_local_ip(),
            "service_port": self.service_port,
            "is_registered": self.is_registered,
            "nacos_server": self.config.NACOS_SERVER_ADDR,
            "namespace": self.config.NACOS_NAMESPACE
        }


# 全局Nacos客户端实例
nacos_client: Optional[NacosServiceRegistry] = None


def init_nacos_client(config: Config) -> NacosServiceRegistry:
    """初始化Nacos客户端"""
    global nacos_client
    nacos_client = NacosServiceRegistry(config)
    return nacos_client


def get_nacos_client() -> Optional[NacosServiceRegistry]:
    """获取Nacos客户端实例"""
    return nacos_client 