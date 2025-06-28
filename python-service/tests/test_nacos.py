"""
Nacos服务发现测试
"""
import pytest
from unittest.mock import Mock, patch
from app import create_app
from app.utils.nacos_client import NacosServiceRegistry, init_nacos_client, get_nacos_client
from app.config import Config


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    
    with app.app_context():
        yield app


@pytest.fixture
def nacos_config():
    """Nacos测试配置"""
    config = Config()
    config.NACOS_SERVER_ADDR = "127.0.0.1:8848"
    config.NACOS_NAMESPACE = "public"
    config.NACOS_SERVICE_NAME = "test-service"
    config.NACOS_SERVICE_PORT = 5000
    return config


@pytest.fixture
def mock_nacos_client(nacos_config):
    """模拟Nacos客户端"""
    with patch('app.utils.nacos_client.NacosClient') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        registry = NacosServiceRegistry(nacos_config)
        registry.client = mock_instance
        yield registry


def test_nacos_service_registry_init(nacos_config):
    """测试Nacos服务注册器初始化"""
    registry = NacosServiceRegistry(nacos_config)
    
    assert registry.service_name == "test-service"
    assert registry.service_port == 5000
    assert registry.is_registered is False


def test_get_local_ip():
    """测试获取本地IP"""
    registry = NacosServiceRegistry(Config())
    ip = registry.get_local_ip()
    
    assert ip is not None
    assert isinstance(ip, str)


@patch('app.utils.nacos_client.NacosClient')
def test_register_service_success(mock_nacos_client, nacos_config):
    """测试服务注册成功"""
    mock_instance = Mock()
    mock_instance.add_naming_instance.return_value = True
    mock_nacos_client.return_value = mock_instance
    
    registry = NacosServiceRegistry(nacos_config)
    registry.client = mock_instance
    
    success = registry.register_service()
    
    assert success is True
    assert registry.is_registered is True
    mock_instance.add_naming_instance.assert_called_once()


@patch('app.utils.nacos_client.NacosClient')
def test_register_service_failure(mock_nacos_client, nacos_config):
    """测试服务注册失败"""
    mock_instance = Mock()
    mock_instance.add_naming_instance.return_value = False
    mock_nacos_client.return_value = mock_instance
    
    registry = NacosServiceRegistry(nacos_config)
    registry.client = mock_instance
    
    success = registry.register_service()
    
    assert success is False
    assert registry.is_registered is False


@patch('app.utils.nacos_client.NacosClient')
def test_deregister_service_success(mock_nacos_client, nacos_config):
    """测试服务注销成功"""
    mock_instance = Mock()
    mock_instance.remove_naming_instance.return_value = True
    mock_nacos_client.return_value = mock_instance
    
    registry = NacosServiceRegistry(nacos_config)
    registry.client = mock_instance
    registry.is_registered = True
    
    success = registry.deregister_service()
    
    assert success is True
    assert registry.is_registered is False
    mock_instance.remove_naming_instance.assert_called_once()


def test_get_service_info(nacos_config):
    """测试获取服务信息"""
    registry = NacosServiceRegistry(nacos_config)
    
    info = registry.get_service_info()
    
    assert 'service_name' in info
    assert 'service_ip' in info
    assert 'service_port' in info
    assert 'is_registered' in info
    assert info['service_name'] == "test-service"
    assert info['service_port'] == 5000


def test_init_nacos_client(nacos_config):
    """测试初始化Nacos客户端"""
    client = init_nacos_client(nacos_config)
    
    assert client is not None
    assert isinstance(client, NacosServiceRegistry)
    assert client.service_name == "test-service"


def test_get_nacos_client(nacos_config):
    """测试获取Nacos客户端"""
    # 先初始化
    init_nacos_client(nacos_config)
    
    # 再获取
    client = get_nacos_client()
    
    assert client is not None
    assert isinstance(client, NacosServiceRegistry) 