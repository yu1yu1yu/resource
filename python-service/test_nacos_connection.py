#!/usr/bin/env python3
"""
Nacos连接测试脚本
"""
import requests
import json
from app.config import Config


def test_nacos_connection():
    """测试Nacos连接"""
    config = Config()
    
    print("🔍 测试Nacos连接...")
    print(f"Nacos服务器地址: {config.NACOS_SERVER_ADDR}")
    print(f"命名空间: {config.NACOS_NAMESPACE}")
    print(f"服务名称: {config.NACOS_SERVICE_NAME}")
    print()
    
    # 测试Nacos HTTP API连接
    try:
        nacos_url = f"http://{config.NACOS_SERVER_ADDR}/nacos/v1/ns/operator/metrics"
        response = requests.get(nacos_url, timeout=5)
        
        if response.status_code == 200:
            print("✅ Nacos服务器连接成功")
            metrics = response.json()
            print(f"   - 服务数量: {metrics.get('serviceCount', 'N/A')}")
            print(f"   - 实例数量: {metrics.get('instanceCount', 'N/A')}")
        else:
            print(f"❌ Nacos服务器响应异常: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Nacos服务器")
        print("   请确保Nacos服务已启动，或检查NACOS_SERVER_ADDR配置")
    except requests.exceptions.Timeout:
        print("❌ 连接Nacos服务器超时")
    except Exception as e:
        print(f"❌ 连接Nacos服务器失败: {str(e)}")
    
    print()
    
    # 测试服务注册
    try:
        from app.utils.nacos_client import NacosServiceRegistry
        
        print("🔧 测试Nacos客户端...")
        registry = NacosServiceRegistry(config)
        
        # 获取本地IP
        local_ip = registry.get_local_ip()
        print(f"   本地IP: {local_ip}")
        
        # 获取服务信息
        service_info = registry.get_service_info()
        print(f"   服务信息: {json.dumps(service_info, indent=2, ensure_ascii=False)}")
        
        print("✅ Nacos客户端初始化成功")
        
    except ImportError as e:
        print(f"❌ 导入Nacos客户端失败: {str(e)}")
        print("   请确保已安装nacos-sdk-python依赖")
    except Exception as e:
        print(f"❌ Nacos客户端初始化失败: {str(e)}")


if __name__ == '__main__':
    test_nacos_connection() 