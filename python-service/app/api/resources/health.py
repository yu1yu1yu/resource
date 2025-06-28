"""
健康检查API
"""
from flask import jsonify
from flask_restful import Resource
from datetime import datetime


class HealthResource(Resource):
    """健康检查资源"""
    
    def get(self):
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'flask-api',
            'version': '1.0.0'
        }) 