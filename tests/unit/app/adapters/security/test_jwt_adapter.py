from uuid import uuid4

import pytest

from src.app.adapters.security.jwt_adapter import JWTAdapter
from src.app.domain.entities.token import CreateTokenInput, DecodedToken


class TestJWTAdapter:
    @pytest.fixture
    def mock_jwt_manager(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def jwt_adapter(self, mock_jwt_manager):
        return JWTAdapter(mock_jwt_manager)

    @pytest.fixture
    def sample_input(self):
        return CreateTokenInput(user_id=uuid4(), email="test@example.com")

    def test_create_access_token(self, jwt_adapter, mock_jwt_manager, sample_input):
        expected_token = "access_token_123"
        mock_jwt_manager.create_access_token.return_value = expected_token

        result = jwt_adapter.create_access_token(sample_input)

        mock_jwt_manager.create_access_token.assert_called_once_with(
            sample_input.user_id, sample_input.email
        )
        assert result.access_token == expected_token
        assert result.refresh_token == ""
        assert result.token_type == "bearer"
        assert result.expires_in == 0

    def test_create_refresh_token(self, jwt_adapter, mock_jwt_manager, sample_input):
        expected_token = "refresh_token_123"
        mock_jwt_manager.create_refresh_token.return_value = expected_token

        result = jwt_adapter.create_refresh_token(sample_input)

        mock_jwt_manager.create_refresh_token.assert_called_once_with(
            sample_input.user_id, sample_input.email
        )
        assert result.access_token == ""
        assert result.refresh_token == expected_token
        assert result.token_type == "bearer"
        assert result.expires_in == 0

    def test_decode_token(self, jwt_adapter, mock_jwt_manager):
        token = "test_token"
        user_id = str(uuid4())
        email = "test@example.com"
        expected_decoded = DecodedToken(
            sub=user_id, email=email, exp=1234567890, iat=1234567800, type="access"
        )
        mock_jwt_manager.decode_token.return_value = expected_decoded

        result = jwt_adapter.decode_token(token)

        mock_jwt_manager.decode_token.assert_called_once_with(token)
        assert result.sub == user_id
        assert result.email == email
        assert result.exp == 1234567890
        assert result.iat == 1234567800
        assert result.type == "access"

    def test_verify_token(self, jwt_adapter, mock_jwt_manager):
        token = "test_token"
        mock_jwt_manager.verify_token.return_value = True

        result = jwt_adapter.verify_token(token)

        mock_jwt_manager.verify_token.assert_called_once_with(token)
        assert result is True

    def test_verify_token_invalid(self, jwt_adapter, mock_jwt_manager):
        token = "invalid_token"
        mock_jwt_manager.verify_token.return_value = False

        result = jwt_adapter.verify_token(token)

        mock_jwt_manager.verify_token.assert_called_once_with(token)
        assert result is False
