"""
用户模型
"""
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import BaseModel
from app.extensions import db


class User(BaseModel):
    """用户模型"""
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin
        })
        return data
    
    def __repr__(self):
        return f'<User {self.username}>' 