# Flask API 服务框架

一个现代化的Flask API服务框架，包含完整的用户认证、数据库集成、监控和文档功能，支持Nacos服务发现。

## 功能特性

- 🚀 **Flask 3.0**: 基于最新的Flask框架
- 🔐 **JWT认证**: 完整的用户认证和授权系统
- 🗄️ **数据库集成**: SQLAlchemy ORM，支持多种数据库
- 🔍 **Nacos服务发现**: 自动注册和发现服务
- 📊 **API文档**: 自动生成的Swagger文档
- 🔍 **监控指标**: 系统性能监控
- 🧪 **测试框架**: 完整的单元测试
- 🐳 **Docker支持**: 容器化部署
- 📝 **结构化日志**: JSON格式日志输出
- 🔒 **CORS支持**: 跨域请求处理

## 技术栈

- **后端框架**: Flask 3.0
- **数据库**: SQLAlchemy + PostgreSQL/SQLite
- **认证**: JWT (JSON Web Tokens)
- **服务发现**: Nacos
- **API文档**: Swagger/OpenAPI
- **监控**: Prometheus指标
- **日志**: Structlog
- **测试**: Pytest
- **部署**: Docker + Docker Compose

## 快速开始

### 1. 环境准备

确保你的系统已安装：
- Python 3.11+
- pip
- Docker (可选)
- Nacos Server 2.x

### 2. 启动Nacos

```bash
# 下载并启动Nacos
wget https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.zip
unzip nacos-server-2.2.3.zip
cd nacos/bin
./startup.sh -m standalone
```

Nacos默认访问地址：http://localhost:8848/nacos
默认账号密码：nacos/nacos

### 3. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 4. 配置环境变量

复制配置文件：
```bash
cp config.env .env
```

编辑 `.env` 文件，设置你的配置：
```env
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
NACOS_SERVER_ADDR=127.0.0.1:8848
NACOS_SERVICE_NAME=flask-api
```

### 5. 初始化数据库

```bash
# 初始化数据库
python manage.py init-db

# 创建管理员用户
python manage.py create-admin
```

### 6. 启动应用

```bash
# 一键启动（推荐）
./start.sh

# 或手动启动
python run.py

# 或使用Flask命令
flask run
```

应用将在 http://localhost:5000 启动，并自动注册到Nacos

## Nacos服务发现

### 配置说明

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

### 服务注册流程

1. **应用启动时自动注册**
   - 获取本机IP地址
   - 注册服务到Nacos
   - 启动心跳线程

2. **心跳保活**
   - 定期发送心跳包
   - 保持服务在线状态

3. **优雅关闭**
   - 接收关闭信号
   - 停止心跳线程
   - 从Nacos注销服务

### API端点

#### 服务监控
- `GET /monitoring/nacos/service` - 获取当前服务信息
- `GET /monitoring/nacos/service/{service_name}/instances` - 获取指定服务的实例列表
- `POST /monitoring/nacos/service/register` - 手动注册服务
- `POST /monitoring/nacos/service/deregister` - 手动注销服务

#### 使用示例

```bash
# 获取服务信息
curl http://localhost:5000/monitoring/nacos/service

# 手动注册服务
curl -X POST http://localhost:5000/monitoring/nacos/service/register

# 获取其他服务实例
curl http://localhost:5000/monitoring/nacos/service/user-service/instances
```

### 服务发现

在Nacos控制台可以查看：
- 服务列表
- 服务实例详情
- 健康状态
- 元数据信息

## API端点

### 认证相关
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `POST /auth/refresh` - 刷新令牌

### 用户管理
- `GET /api/v1/users` - 获取用户列表
- `GET /api/v1/users/<id>` - 获取用户详情
- `PUT /api/v1/users/<id>` - 更新用户信息
- `DELETE /api/v1/users/<id>` - 删除用户

### 系统监控
- `GET /api/v1/health` - 健康检查
- `GET /monitoring/metrics` - 系统指标
- `GET /monitoring/nacos/service` - Nacos服务信息

## 使用示例

### 1. 用户注册

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. 用户登录

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. 获取用户列表

```bash
curl -X GET http://localhost:5000/api/v1/users \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. 查看Nacos服务信息

```bash
curl http://localhost:5000/monitoring/nacos/service
```

## 开发指南

### 项目结构

```
python-service/
├── app/                    # 应用主目录
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── extensions.py      # Flask扩展
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── api/               # API蓝图
│   │   ├── __init__.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       └── user.py
│   ├── auth/              # 认证蓝图
│   │   ├── __init__.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       └── auth.py
│   ├── monitoring/        # 监控蓝图
│   │   ├── __init__.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       └── metrics.py
│   └── utils/             # 工具函数
│       ├── __init__.py
│       ├── logger.py
│       └── error_handlers.py
├── tests/                 # 测试文件
│   ├── __init__.py
│   └── test_api.py
├── app.py                 # 应用入口
├── run.py                 # 启动脚本
├── manage.py              # 管理脚本
├── requirements.txt       # 依赖文件
├── Dockerfile             # Docker配置
├── docker-compose.yml     # Docker Compose配置
└── README.md              # 项目说明
```

### 添加新的API端点

1. 在 `app/api/resources/` 目录下创建新的资源文件
2. 在 `app/api/__init__.py` 中注册新的资源
3. 添加相应的测试用例

### 添加新的数据模型

1. 在 `app/models/` 目录下创建新的模型文件
2. 继承 `BaseModel` 类
3. 运行数据库迁移

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api.py

# 生成覆盖率报告
pytest --cov=app tests/
```

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t flask-api .

# 运行容器
docker run -p 5000:5000 flask-api
```

### Docker Compose部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f app

# 停止服务
docker-compose down
```

### 生产环境部署

1. 设置生产环境变量
2. 使用Gunicorn作为WSGI服务器
3. 配置Nginx作为反向代理
4. 设置SSL证书

```bash
# 生产环境启动
gunicorn --bind 0.0.0.0:5000 --workers 4 app:create_app()
```

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| FLASK_ENV | development | Flask环境 |
| DEBUG | True | 调试模式 |
| SECRET_KEY | your-secret-key-here | 应用密钥 |
| DATABASE_URL | sqlite:///app.db | 数据库连接URL |
| REDIS_URL | redis://localhost:6379/0 | Redis连接URL |
| JWT_SECRET_KEY | jwt-secret-key | JWT密钥 |
| LOG_LEVEL | INFO | 日志级别 |

### 数据库配置

支持多种数据库：

- **SQLite** (开发环境)
  ```env
  DATABASE_URL=sqlite:///app.db
  ```

- **PostgreSQL** (生产环境)
  ```env
  DATABASE_URL=postgresql://user:pass@localhost/dbname
  ```

- **MySQL**
  ```env
  DATABASE_URL=mysql://user:pass@localhost/dbname
  ```

## 监控和日志

### 日志配置

应用使用结构化日志，输出JSON格式：

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "info",
  "logger": "app.api.resources.user",
  "message": "User created successfully",
  "user_id": 123
}
```

### 监控指标

访问 `/monitoring/metrics` 获取系统指标：

- CPU使用率
- 内存使用情况
- 磁盘使用情况
- 进程信息

### Nacos监控

访问 `/monitoring/nacos/service` 获取Nacos服务信息：

- 服务注册状态
- 服务实例信息
- 心跳状态
- 元数据信息

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

4. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接字符串格式
   - 确认数据库用户权限

5. **JWT令牌无效**
   - 检查JWT_SECRET_KEY配置
   - 确认令牌格式正确
   - 验证令牌是否过期

6. **CORS错误**
   - 检查CORS_ORIGINS配置
   - 确认请求头设置正确

### 调试模式

启用调试模式获取详细错误信息：

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Nacos调试

1. 访问Nacos控制台：http://localhost:8848/nacos
2. 查看服务列表和实例状态
3. 检查服务元数据信息
4. 查看服务日志

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License 