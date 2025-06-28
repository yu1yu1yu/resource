"""
认证蓝图
"""
from flask import Blueprint
from flask_restful import Api
from .resources.auth import LoginResource, RegisterResource, RefreshResource

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)

# 注册认证资源
auth_api.add_resource(LoginResource, '/login')
auth_api.add_resource(RegisterResource, '/register')
auth_api.add_resource(RefreshResource, '/refresh') 