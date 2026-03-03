from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.app.domain.entities.event_message import EventUserData
from src.app.infra.messaging.rabbitmq_manager import InfraEventMessage, RabbitMQManager


class TestRabbitMQManager:
    def test_rabbitmq_manager_initialization(self):
        """Test RabbitMQManager initialization."""
        manager = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        assert manager.host == "localhost"
        assert manager.port == 5672
        assert manager.user == "guest"
        assert manager.password == "guest"
        assert manager.vhost == "/"
        assert manager.connection is None
        assert manager.channel is None

    @pytest.mark.asyncio
    async def test_connect_success(self):
        """Test successful connection to RabbitMQ."""
        manager = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        with patch(
            "src.app.infra.messaging.rabbitmq_manager.connect_robust"
        ) as mock_connect:
            mock_connection = Mock()
            mock_channel = Mock()
            mock_channel.declare_exchange = AsyncMock()
            mock_connection.channel = AsyncMock(return_value=mock_channel)
            mock_connect.return_value = mock_connection

            await manager.connect()

            assert manager.connection == mock_connection
            assert manager.channel == mock_channel
            mock_connect.assert_called_once()
            mock_connection.channel.assert_called_once()
            mock_channel.declare_exchange.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Test disconnection from RabbitMQ."""
        manager = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        # Mock existing connection
        mock_connection = Mock()
        mock_connection.close = AsyncMock()
        mock_connection.is_closed = False

        manager.connection = mock_connection

        await manager.disconnect()

        mock_connection.close.assert_called_once()
        # Note: The actual implementation doesn't set connection to None

    @pytest.mark.asyncio
    async def test_disconnect_with_no_connection(self):
        """Test disconnection when no connection exists."""
        manager = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        # Should not raise any exceptions
        await manager.disconnect()

    @pytest.mark.asyncio
    async def test_publish_success(self):
        """Test successful message publishing."""
        manager = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        # Mock connection and channel
        mock_connection = Mock()
        mock_new_channel = Mock()
        mock_new_channel.default_exchange = Mock()
        mock_new_channel.default_exchange.publish = AsyncMock()

        mock_connection.channel = AsyncMock(return_value=mock_new_channel)
        manager.connection = mock_connection

        message = InfraEventMessage(
            event_name="test.event",
            data=EventUserData(
                user_id="123", email="test@example.com", username="testuser"
            ),
        )

        await manager.publish(message)

        mock_connection.channel.assert_called_once()
        mock_new_channel.default_exchange.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_publish_with_no_connection(self):
        """Test publishing when no connection exists."""
        manager = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        with patch(
            "src.app.infra.messaging.rabbitmq_manager.connect_robust"
        ) as mock_connect:
            mock_connection = Mock()
            mock_channel = Mock()
            mock_new_channel = Mock()
            mock_new_channel.default_exchange = Mock()
            mock_new_channel.default_exchange.publish = AsyncMock()

            mock_connection.channel = AsyncMock(return_value=mock_channel)
            mock_channel.declare_exchange = AsyncMock()
            mock_channel.default_exchange = Mock()
            mock_channel.default_exchange.publish = AsyncMock()
            mock_connect.return_value = mock_connection

            message = InfraEventMessage(
                event_name="test.event",
                data=EventUserData(
                    user_id="123", email="test@example.com", username="testuser"
                ),
            )

            await manager.publish(message)

            # Should connect first
            mock_connect.assert_called_once()
            mock_connection.channel.assert_called()
            mock_channel.declare_exchange.assert_called_once()
            mock_channel.default_exchange.publish.assert_called_once()

    def test_infra_event_message_creation(self):
        """Test InfraEventMessage creation."""
        message = InfraEventMessage(
            event_name="user.created",
            data={"user_id": "123", "email": "test@example.com"},
        )

        assert message.event_name == "user.created"
        assert message.data == {"user_id": "123", "email": "test@example.com"}

    def test_infra_event_message_with_empty_data(self):
        """Test InfraEventMessage creation with empty data."""
        message = InfraEventMessage(event_name="test.event", data={})

        assert message.event_name == "test.event"
        assert message.data == {}

    def test_manager_with_different_configurations(self):
        """Test manager with different configuration values."""
        # Test with custom configuration
        manager1 = RabbitMQManager(
            host="custom-host",
            port=1234,
            user="custom-user",
            password="custom-password",
            vhost="/custom-vhost",
        )

        assert manager1.host == "custom-host"
        assert manager1.port == 1234
        assert manager1.user == "custom-user"
        assert manager1.password == "custom-password"
        assert manager1.vhost == "/custom-vhost"

        # Test with default-like configuration
        manager2 = RabbitMQManager(
            host="localhost", port=5672, user="guest", password="guest", vhost="/"
        )

        assert manager2.host == "localhost"
        assert manager2.port == 5672
        assert manager2.user == "guest"
        assert manager2.password == "guest"
        assert manager2.vhost == "/"
