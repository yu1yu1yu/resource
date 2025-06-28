"""
监控指标API
"""
from flask import jsonify
from flask_restful import Resource
import psutil
import time


class MetricsResource(Resource):
    """监控指标资源"""
    
    def get(self):
        """获取系统指标"""
        # 系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 进程信息
        process = psutil.Process()
        process_memory = process.memory_info()
        
        metrics = {
            'timestamp': time.time(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                }
            },
            'process': {
                'memory_rss': process_memory.rss,
                'memory_vms': process_memory.vms,
                'cpu_percent': process.cpu_percent(),
                'num_threads': process.num_threads()
            }
        }
        
        return jsonify(metrics) 