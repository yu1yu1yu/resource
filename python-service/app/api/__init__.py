"""
API蓝图
"""
from flask import Blueprint
from flask_restful import Api
from .resources.user import UserResource, UserListResource
from .resources.health import HealthResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# 注册API资源
api.add_resource(HealthResource, '/health')
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>') 