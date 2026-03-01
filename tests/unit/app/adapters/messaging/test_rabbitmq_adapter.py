import pytest

from src.app.adapters.messaging.rabbitmq_adapter import RabbitMQAdapter
from src.app.domain.entities.event_message import EventMessage
from src.app.infra.messaging.rabbitmq_manager import InfraEventMessage


class TestRabbitMQAdapter:
    @pytest.fixture
    def mock_rabbitmq_manager(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def rabbitmq_adapter(self, mock_rabbitmq_manager):
        return RabbitMQAdapter(mock_rabbitmq_manager)

    @pytest.mark.asyncio
    async def test_connect(self, rabbitmq_adapter, mock_rabbitmq_manager, mocker):
        mock_rabbitmq_manager.connect = mocker.AsyncMock()

        await rabbitmq_adapter.connect()

        mock_rabbitmq_manager.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_publish(self, rabbitmq_adapter, mock_rabbitmq_manager, mocker):
        mock_rabbitmq_manager.publish = mocker.AsyncMock()
        event_name = "user_created"
        data = {"user_id": "123", "email": "test@example.com"}
        event_message = EventMessage(event_name=event_name, data=data)

        await rabbitmq_adapter.publish(event_message)

        # Verify that the adapter converts domain EventMessage to InfraEventMessage
        expected_infra_message = InfraEventMessage(
            event_name=event_name,
            data=data,
        )
        mock_rabbitmq_manager.publish.assert_called_once_with(expected_infra_message)

    @pytest.mark.asyncio
    async def test_disconnect(self, rabbitmq_adapter, mock_rabbitmq_manager, mocker):
        mock_rabbitmq_manager.disconnect = mocker.AsyncMock()

        await rabbitmq_adapter.disconnect()

        mock_rabbitmq_manager.disconnect.assert_called_once()

    def test_event_message_creation(self):
        event_name = "user_created"
        data = {"user_id": "123", "email": "test@example.com"}
        event_message = EventMessage(event_name=event_name, data=data)

        assert event_message.event_name == event_name
        assert event_message.data == data

    def test_event_message_creation_empty_data(self):
        event_name = "test_event"
        data = {}
        event_message = EventMessage(event_name=event_name, data=data)

        assert event_message.event_name == event_name
        assert event_message.data == data
