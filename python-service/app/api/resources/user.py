"""
用户API资源
"""
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db


class UserListResource(Resource):
    """用户列表资源"""
    
    def get(self):
        """获取用户列表"""
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        })
    
    def post(self):
        """创建新用户"""
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        # 检查用户是否已存在
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 409
        
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already exists'}, 409
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.save()
        
        return user.to_dict(), 201


class UserResource(Resource):
    """单个用户资源"""
    
    @jwt_required()
    def get(self, user_id):
        """获取用户详情"""
        user = User.query.get_or_404(user_id)
        return user.to_dict()
    
    @jwt_required()
    def put(self, user_id):
        """更新用户信息"""
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # 更新字段
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        user.save()
        return user.to_dict()
    
    @jwt_required()
    def delete(self, user_id):
        """删除用户"""
        user = User.query.get_or_404(user_id)
        user.delete()
        return {'message': 'User deleted successfully'}, 200 