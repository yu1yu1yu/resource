"""
监控蓝图
"""
from flask import Blueprint
from flask_restful import Api
from .resources.metrics import MetricsResource
from .resources.nacos import (
    NacosServiceResource, 
    NacosServiceInstancesResource,
    NacosServiceRegisterResource,
    NacosServiceDeregisterResource
)

monitoring_bp = Blueprint('monitoring', __name__)
monitoring_api = Api(monitoring_bp)

# 注册监控资源
monitoring_api.add_resource(MetricsResource, '/metrics')
monitoring_api.add_resource(NacosServiceResource, '/nacos/service')
monitoring_api.add_resource(NacosServiceInstancesResource, '/nacos/service/<string:service_name>/instances')
monitoring_api.add_resource(NacosServiceRegisterResource, '/nacos/service/register')
monitoring_api.add_resource(NacosServiceDeregisterResource, '/nacos/service/deregister') 