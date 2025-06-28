#!/usr/bin/env python3
"""
应用启动脚本
"""
import os
import signal
import sys
from dotenv import load_dotenv
from app import create_app
from app.utils.nacos_client import get_nacos_client

# 加载环境变量
load_dotenv('config.env')

app = create_app()

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
    
    # 注册服务到Nacos
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
    
    try:
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('DEBUG', 'True').lower() == 'true'
        )
    except KeyboardInterrupt:
        print("\n🛑 用户中断，正在关闭...")
    finally:
        deregister_service_from_nacos() 