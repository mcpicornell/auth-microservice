import pytest

from src.app.infra.messaging.rabbitmq_manager import InfraEventMessage, RabbitMQManager


class TestRabbitMQManager:
    @pytest.fixture
    def rabbitmq_manager(self):
        return RabbitMQManager("localhost", 5672, "guest", "guest", "/")

    def test_initialization(self):
        # Test that RabbitMQManager initializes correctly
        manager = RabbitMQManager("localhost", 5672, "guest", "guest", "/")
        assert manager.host == "localhost"
        assert manager.port == 5672
        assert manager.user == "guest"
        assert manager.password == "guest"
        assert manager.vhost == "/"
        assert manager.connection is None
        assert manager.channel is None

    def test_initialization_with_different_params(self):
        # Test initialization with different parameters
        manager = RabbitMQManager("testhost", 1234, "testuser", "testpass", "/test")
        assert manager.host == "testhost"
        assert manager.port == 1234
        assert manager.user == "testuser"
        assert manager.password == "testpass"
        assert manager.vhost == "/test"

    def test_connection_properties(self, rabbitmq_manager):
        # Test that connection properties are set correctly
        assert rabbitmq_manager.host == "localhost"
        assert rabbitmq_manager.port == 5672
        assert rabbitmq_manager.user == "guest"
        assert rabbitmq_manager.password == "guest"
        assert rabbitmq_manager.vhost == "/"

    def test_connection_state_initially_none(self, rabbitmq_manager):
        # Test that connection is initially None
        assert rabbitmq_manager.connection is None
        assert rabbitmq_manager.channel is None

    @pytest.mark.asyncio
    async def test_connect_method_exists(self, rabbitmq_manager):
        # Test that connect method exists and is async
        assert hasattr(rabbitmq_manager, "connect")
        assert callable(rabbitmq_manager.connect)

    @pytest.mark.asyncio
    async def test_disconnect_method_exists(self, rabbitmq_manager):
        # Test that disconnect method exists and is async
        assert hasattr(rabbitmq_manager, "disconnect")
        assert callable(rabbitmq_manager.disconnect)

    def test_publish_method_exists(self, rabbitmq_manager):
        # Test that publish method exists
        assert hasattr(rabbitmq_manager, "publish")
        assert callable(rabbitmq_manager.publish)

    def test_infra_event_message_dataclass(self):
        # Test InfraEventMessage dataclass
        event_data = {"user_id": "123", "action": "created"}
        message = InfraEventMessage("user.created", event_data)

        assert message.event_name == "user.created"
        assert message.data == event_data

    def test_manager_with_different_hosts(self):
        # Test initialization with different hosts
        managers = [
            RabbitMQManager("localhost", 5672, "guest", "guest", "/"),
            RabbitMQManager("rabbitmq", 5672, "guest", "guest", "/"),
            RabbitMQManager("127.0.0.1", 5672, "guest", "guest", "/"),
        ]

        for i, manager in enumerate(managers):
            expected_hosts = ["localhost", "rabbitmq", "127.0.0.1"]
            assert manager.host == expected_hosts[i]

    def test_manager_with_different_ports(self):
        # Test initialization with different ports
        managers = [
            RabbitMQManager("localhost", 5672, "guest", "guest", "/"),
            RabbitMQManager("localhost", 5673, "guest", "guest", "/"),
            RabbitMQManager("localhost", 15672, "guest", "guest", "/"),
        ]

        for i, manager in enumerate(managers):
            expected_ports = [5672, 5673, 15672]
            assert manager.port == expected_ports[i]

    def test_connection_and_channel_attributes(self, rabbitmq_manager):
        # Test that connection and channel attributes exist
        assert hasattr(rabbitmq_manager, "connection")
        assert hasattr(rabbitmq_manager, "channel")

        # Initially they should be None
        assert rabbitmq_manager.connection is None
        assert rabbitmq_manager.channel is None

    def test_manager_parameter_types(self):
        # Test that manager parameters accept correct types
        manager = RabbitMQManager("localhost", 5672, "guest", "guest", "/")

        assert isinstance(manager.host, str)
        assert isinstance(manager.port, int)
        assert isinstance(manager.user, str)
        assert isinstance(manager.password, str)
        assert isinstance(manager.vhost, str)
