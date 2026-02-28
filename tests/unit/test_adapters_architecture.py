from unittest.mock import Mock

from src.app.adapters.messaging.rabbitmq_adapter import RabbitMQAdapter
from src.app.adapters.security.jwt_adapter import JWTAdapter
from src.app.domain.entities.event_message import EventMessage


def test_jwt_adapter_uses_dataclass():
    mock_jwt_manager = Mock()
    mock_jwt_manager.create_access_token.return_value = "test_token"

    adapter = JWTAdapter(mock_jwt_manager)

    from src.app.domain.entities.token import CreateTokenInput

    input_data = CreateTokenInput(user_id="user123", email="test@example.com")

    result = adapter.create_access_token(input_data)

    assert result.access_token == "test_token"
    assert result.token_type == "bearer"


def test_rabbitmq_adapter_uses_dataclass():
    mock_rabbitmq_manager = Mock()
    adapter = RabbitMQAdapter(mock_rabbitmq_manager)

    event_message = EventMessage(
        event_name="user.created", data={"user_id": "123", "email": "test@example.com"}
    )

    result = adapter._event_message_to_dict(event_message)

    assert result["event_name"] == "user.created"
    assert result["data"]["user_id"] == "123"
    assert result["data"]["email"] == "test@example.com"


def test_adapters_contain_no_business_logic():
    from src.app.adapters.security.password_adapter import PasswordAdapter

    password_adapter = PasswordAdapter()

    hash_result = password_adapter.hash_password("pass")
    verify_result = password_adapter.verify_password("pass", hash_result)

    assert isinstance(hash_result, str)
    assert isinstance(verify_result, bool)
    assert len(hash_result) > 0

    mock_jwt_manager = Mock()
    mock_jwt_manager.create_access_token.return_value = "test_token"

    jwt_adapter = JWTAdapter(mock_jwt_manager)

    from src.app.domain.entities.token import CreateTokenInput

    token_input = CreateTokenInput(user_id="123", email="test@example.com")

    token_output = jwt_adapter.create_access_token(token_input)

    assert token_output.access_token == "test_token"
    assert token_output.token_type == "bearer"
