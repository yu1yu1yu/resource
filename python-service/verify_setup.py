#!/usr/bin/env python3
"""
项目设置验证脚本
"""
import os
import sys
import importlib


def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.8或更高版本")
        return False


def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'flask_restful',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'nacos',
        'requests',
        'pydantic',
        'structlog'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def check_config_files():
    """检查配置文件"""
    print("\n⚙️ 检查配置文件...")
    
    config_files = [
        'config.env',
        'requirements.txt',
        'app/config.py',
        'app/utils/nacos_client.py'
    ]
    
    missing_files = []
    
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ 缺少配置文件: {', '.join(missing_files)}")
        return False
    
    return True


def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    required_dirs = [
        'app',
        'app/models',
        'app/api',
        'app/api/resources',
        'app/auth',
        'app/auth/resources',
        'app/monitoring',
        'app/monitoring/resources',
        'app/utils',
        'tests'
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n⚠️ 缺少目录: {', '.join(missing_dirs)}")
        return False
    
    return True


def main():
    """主函数"""
    print("🔍 Flask API + Nacos 项目设置验证")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_config_files(),
        check_project_structure()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 所有检查通过！项目设置正确。")
        print("\n📋 下一步:")
        print("1. 启动Nacos服务器")
        print("2. 运行: python run.py")
        print("3. 或运行: ./start.sh")
        return True
    else:
        print("❌ 部分检查失败，请修复上述问题。")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 