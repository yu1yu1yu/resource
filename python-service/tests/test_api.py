"""
API测试
"""
import pytest
from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建测试运行器"""
    return app.test_cli_runner()


def test_health_check(client):
    """测试健康检查"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_user_registration(client):
    """测试用户注册"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    response = client.post('/auth/register', json=user_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert 'access_token' in data
    assert 'user' in data
    assert data['user']['username'] == 'testuser'


def test_user_login(client):
    """测试用户登录"""
    # 先注册用户
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    client.post('/auth/register', json=user_data)
    
    # 测试登录
    login_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'access_token' in data
    assert 'user' in data


def test_get_users(client):
    """测试获取用户列表"""
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'users' in data
    assert 'total' in data 