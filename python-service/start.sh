#!/bin/bash

# Flask API 启动脚本

echo "🚀 启动 Flask API 服务..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚙️ 复制环境变量文件..."
    cp config.env .env
fi

# 检查Nacos服务
echo "🔍 检查Nacos服务..."
NACOS_HOST=$(grep NACOS_SERVER_ADDR config.env | cut -d'=' -f2 | cut -d':' -f1)
NACOS_PORT=$(grep NACOS_SERVER_ADDR config.env | cut -d'=' -f2 | cut -d':' -f2)

if nc -z $NACOS_HOST $NACOS_PORT 2>/dev/null; then
    echo "✅ Nacos服务可用: $NACOS_HOST:$NACOS_PORT"
else
    echo "⚠️ Nacos服务不可用: $NACOS_HOST:$NACOS_PORT"
    echo "请确保Nacos服务已启动，或修改config.env中的NACOS_SERVER_ADDR配置"
    read -p "是否继续启动服务? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 初始化数据库
echo "🗄️ 初始化数据库..."
python manage.py init-db

# 启动应用
echo "🌟 启动应用..."
echo "📋 服务信息:"
echo "   - 服务名称: $(grep NACOS_SERVICE_NAME config.env | cut -d'=' -f2)"
echo "   - 服务地址: $(grep HOST config.env | cut -d'=' -f2):$(grep PORT config.env | cut -d'=' -f2)"
echo "   - Nacos地址: $(grep NACOS_SERVER_ADDR config.env | cut -d'=' -f2)"
echo ""

python run.py 