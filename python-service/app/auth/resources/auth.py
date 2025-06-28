"""
认证API资源
"""
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User


class LoginResource(Resource):
    """登录资源"""
    
    def post(self):
        """用户登录"""
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return {'error': 'Missing username or password'}, 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            if not user.is_active:
                return {'error': 'Account is disabled'}, 401
            
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }, 200
        else:
            return {'error': 'Invalid username or password'}, 401


class RegisterResource(Resource):
    """注册资源"""
    
    def post(self):
        """用户注册"""
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
        
        # 生成令牌
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 201


class RefreshResource(Resource):
    """刷新令牌资源"""
    
    @jwt_required(refresh=True)
    def post(self):
        """刷新访问令牌"""
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        return {
            'access_token': new_access_token
        }, 200 