"""
Nacos监控API
"""
from flask import jsonify
from flask_restful import Resource
from app.utils.nacos_client import get_nacos_client


class NacosServiceResource(Resource):
    """Nacos服务监控资源"""
    
    def get(self):
        """获取Nacos服务信息"""
        nacos_client = get_nacos_client()
        
        if nacos_client is None:
            return jsonify({
                'error': 'Nacos client not initialized',
                'status': 'error'
            }), 500
        
        try:
            service_info = nacos_client.get_service_info()
            
            # 获取所有服务实例
            all_services = []
            try:
                # 这里可以添加获取所有服务的逻辑
                # 由于nacos-sdk-python的限制，可能需要通过HTTP API获取
                pass
            except Exception as e:
                pass
            
            return jsonify({
                'status': 'success',
                'service_info': service_info,
                'all_services': all_services
            })
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500


class NacosServiceInstancesResource(Resource):
    """Nacos服务实例资源"""
    
    def get(self, service_name):
        """获取指定服务的实例列表"""
        nacos_client = get_nacos_client()
        
        if nacos_client is None:
            return jsonify({
                'error': 'Nacos client not initialized',
                'status': 'error'
            }), 500
        
        try:
            instances = nacos_client.get_service_instances(service_name)
            
            return jsonify({
                'status': 'success',
                'service_name': service_name,
                'instances': instances,
                'count': len(instances)
            })
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500


class NacosServiceRegisterResource(Resource):
    """Nacos服务注册资源"""
    
    def post(self):
        """手动注册服务"""
        nacos_client = get_nacos_client()
        
        if nacos_client is None:
            return jsonify({
                'error': 'Nacos client not initialized',
                'status': 'error'
            }), 500
        
        try:
            success = nacos_client.register_service()
            
            if success:
                nacos_client.start_heartbeat()
                return jsonify({
                    'message': 'Service registered successfully',
                    'status': 'success'
                }), 200
            else:
                return jsonify({
                    'error': 'Failed to register service',
                    'status': 'error'
                }), 500
                
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500


class NacosServiceDeregisterResource(Resource):
    """Nacos服务注销资源"""
    
    def post(self):
        """手动注销服务"""
        nacos_client = get_nacos_client()
        
        if nacos_client is None:
            return jsonify({
                'error': 'Nacos client not initialized',
                'status': 'error'
            }), 500
        
        try:
            nacos_client.stop_heartbeat()
            success = nacos_client.deregister_service()
            
            if success:
                return jsonify({
                    'message': 'Service deregistered successfully',
                    'status': 'success'
                }), 200
            else:
                return jsonify({
                    'error': 'Failed to deregister service',
                    'status': 'error'
                }), 500
                
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500 