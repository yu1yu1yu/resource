# Nacos服务发现集成指南

## 概述

本项目已成功集成Nacos服务发现功能，支持自动服务注册、心跳保活和优雅关闭。

## 功能特性

### ✅ 已完成功能

1. **自动服务注册**
   - 应用启动时自动注册到Nacos
   - 自动获取本机IP地址
   - 支持自定义服务名称和端口

2. **心跳保活机制**
   - 定期发送心跳包
   - 可配置心跳间隔
   - 自动重连机制

3. **优雅关闭**
   - 信号处理器（SIGINT, SIGTERM）
   - 自动停止心跳线程
   - 从Nacos注销服务

4. **监控API**
   - 服务状态查询
   - 手动注册/注销
   - 服务实例列表

5. **配置管理**
   - 环境变量配置
   - 多环境支持
   - 自动配置验证

## 项目结构

```
python-service/
├── app/
│   ├── config.py              # Nacos配置项
│   ├── utils/
│   │   └── nacos_client.py    # Nacos客户端实现
│   └── monitoring/
│       └── resources/
│           └── nacos.py       # Nacos监控API
├── config.env                 # 环境变量配置
├── requirements.txt           # 包含nacos-sdk-python
├── run.py                     # 启动脚本（集成Nacos）
├── start.sh                   # 一键启动脚本
└── tests/
    └── test_nacos.py          # Nacos功能测试
```

## 配置说明

### 环境变量

```env
# Nacos服务发现配置
NACOS_SERVER_ADDR=127.0.0.1:8848
NACOS_NAMESPACE=public
NACOS_GROUP=DEFAULT_GROUP
NACOS_SERVICE_NAME=flask-api
NACOS_SERVICE_IP=127.0.0.1
NACOS_SERVICE_PORT=5000
NACOS_HEARTBEAT_INTERVAL=5
NACOS_DEREGISTER_TIME=10
```

### 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| NACOS_SERVER_ADDR | 127.0.0.1:8848 | Nacos服务器地址 |
| NACOS_NAMESPACE | public | 命名空间 |
| NACOS_GROUP | DEFAULT_GROUP | 服务分组 |
| NACOS_SERVICE_NAME | flask-api | 服务名称 |
| NACOS_SERVICE_IP | 127.0.0.1 | 服务IP（自动获取） |
| NACOS_SERVICE_PORT | 5000 | 服务端口 |
| NACOS_HEARTBEAT_INTERVAL | 5 | 心跳间隔（秒） |
| NACOS_DEREGISTER_TIME | 10 | 注销时间（秒） |

## 使用方法

### 1. 启动Nacos服务器

```bash
# 下载Nacos
wget https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.zip
unzip nacos-server-2.2.3.zip
cd nacos/bin

# 启动Nacos
./startup.sh -m standalone
```

### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 3. 启动Flask应用

```bash
# 一键启动（推荐）
./start.sh

# 或手动启动
python run.py
```

### 4. 验证服务注册

访问Nacos控制台：http://localhost:8848/nacos
- 用户名：nacos
- 密码：nacos

在服务列表中可以看到注册的 `flask-api` 服务。

## API端点

### 服务监控

- `GET /monitoring/nacos/service` - 获取当前服务信息
- `GET /monitoring/nacos/service/{service_name}/instances` - 获取指定服务的实例列表
- `POST /monitoring/nacos/service/register` - 手动注册服务
- `POST /monitoring/nacos/service/deregister` - 手动注销服务

### 使用示例

```bash
# 获取服务信息
curl http://localhost:5000/monitoring/nacos/service

# 手动注册服务
curl -X POST http://localhost:5000/monitoring/nacos/service/register

# 获取其他服务实例
curl http://localhost:5000/monitoring/nacos/service/user-service/instances
```

## 核心实现

### NacosServiceRegistry类

```python
class NacosServiceRegistry:
    def __init__(self, config: Config):
        # 初始化Nacos客户端
        
    def register_service(self) -> bool:
        # 注册服务到Nacos
        
    def deregister_service(self) -> bool:
        # 从Nacos注销服务
        
    def heartbeat(self):
        # 心跳检测线程
        
    def get_service_instances(self, service_name: str) -> list:
        # 获取服务实例列表
```

### 服务注册流程

1. **应用启动**
   ```python
   # 初始化Nacos客户端
   init_nacos_client(config)
   
   # 注册服务
   nacos_client.register_service()
   nacos_client.start_heartbeat()
   ```

2. **心跳保活**
   ```python
   # 定期发送心跳
   while self.is_registered:
       self.client.send_heartbeat(...)
       time.sleep(heartbeat_interval)
   ```

3. **优雅关闭**
   ```python
   # 信号处理
   def signal_handler(signum, frame):
       nacos_client.stop_heartbeat()
       nacos_client.deregister_service()
   ```

## 测试

### 运行测试

```bash
# 运行Nacos相关测试
pytest tests/test_nacos.py

# 运行所有测试
pytest
```

### 连接测试

```bash
# 测试Nacos连接
python test_nacos_connection.py
```

## 故障排除

### 常见问题

1. **Nacos连接失败**
   - 检查Nacos服务是否启动
   - 验证NACOS_SERVER_ADDR配置
   - 确认网络连接

2. **服务注册失败**
   - 检查服务名称是否重复
   - 验证IP和端口配置
   - 查看Nacos控制台日志

3. **心跳失败**
   - 检查网络连接
   - 验证Nacos服务状态
   - 调整心跳间隔配置

### 调试方法

1. **查看日志**
   ```bash
   # 启用调试日志
   export LOG_LEVEL=DEBUG
   python run.py
   ```

2. **检查Nacos控制台**
   - 访问：http://localhost:8848/nacos
   - 查看服务列表和实例状态
   - 检查服务元数据

3. **API调试**
   ```bash
   # 获取服务信息
   curl http://localhost:5000/monitoring/nacos/service
   ```

## 扩展功能

### 服务发现

可以通过Nacos客户端获取其他服务实例：

```python
nacos_client = get_nacos_client()
instances = nacos_client.get_service_instances("user-service")
```

### 负载均衡

结合服务发现可以实现负载均衡：

```python
import random

def get_service_instance(service_name):
    instances = nacos_client.get_service_instances(service_name)
    if instances:
        return random.choice(instances)
    return None
```

### 配置中心

Nacos还支持配置中心功能，可以进一步扩展：

```python
# 获取配置
config = nacos_client.get_config("flask-api", "DEFAULT_GROUP")

# 监听配置变化
nacos_client.add_config_watcher("flask-api", "DEFAULT_GROUP", callback)
```

## 总结

✅ **集成完成**：Flask应用已成功集成Nacos服务发现

✅ **功能完整**：支持自动注册、心跳保活、优雅关闭

✅ **监控完善**：提供完整的监控API和测试

✅ **文档齐全**：包含详细的使用说明和故障排除

现在你可以：
1. 启动Nacos服务器
2. 运行 `pip install -r requirements.txt` 安装依赖
3. 使用 `./start.sh` 启动应用
4. 在Nacos控制台查看注册的服务 