from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.app.adapters.security.jwt_adapter import JWTAdapter
from src.app.domain.entities.token import CreateTokenInput
from src.app.infra.auth.jwt_manager import DecodedToken as InfraDecodedToken


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
            user_id=sample_input.user_id, email=sample_input.email
        )
        assert result.access_token == expected_token
        assert result.refresh_token == ""
        assert result.token_type == "bearer"
        assert result.expires_in == 1800

    def test_create_refresh_token(self, jwt_adapter, mock_jwt_manager, sample_input):
        expected_token = "refresh_token_123"
        mock_jwt_manager.create_refresh_token.return_value = expected_token

        result = jwt_adapter.create_refresh_token(sample_input)

        mock_jwt_manager.create_refresh_token.assert_called_once_with(
            user_id=sample_input.user_id, email=sample_input.email
        )
        assert result.access_token == ""
        assert result.refresh_token == expected_token
        assert result.token_type == "bearer"
        assert result.expires_in == 604800

    def test_decode_token(self, jwt_adapter, mock_jwt_manager):
        token = "test_token"
        user_id = uuid4()
        email = "test@example.com"
        exp_time = datetime.now(timezone.utc)
        iat_time = datetime.now(timezone.utc)

        # Mock infra DecodedToken
        infra_decoded = InfraDecodedToken(
            sub=str(user_id),
            email=email,
            exp=exp_time,
            iat=iat_time,
            token_type="access",
        )
        mock_jwt_manager.decode_token.return_value = infra_decoded

        result = jwt_adapter.decode_token(token)

        mock_jwt_manager.decode_token.assert_called_once_with(token)
        assert result.sub == str(user_id)
        assert result.email == email
        assert result.exp == int(exp_time.timestamp())
        assert result.iat == int(iat_time.timestamp())
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
