from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.app.infra.auth.jwt_manager import DecodedToken, JWTManager


class TestJWTManager:
    @pytest.fixture
    def jwt_manager(self):
        return JWTManager("test_secret", "HS256", 30, 7)

    def test_initialization(self):
        # Test that JWTManager initializes correctly
        manager = JWTManager("test_secret", "HS256", 30, 7)

        assert manager.secret_key == "test_secret"
        assert manager.algorithm == "HS256"
        assert manager.access_expire_minutes == 30
        assert manager.refresh_expire_days == 7

    def test_create_access_token(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"

        # Act
        token = jwt_manager.create_access_token(user_id, email)

        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"

        # Act
        token = jwt_manager.create_refresh_token(user_id, email)

        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token_success(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"
        token = jwt_manager.create_access_token(user_id, email)

        # Act
        decoded = jwt_manager.decode_token(token)

        # Assert
        assert isinstance(decoded, DecodedToken)
        assert str(decoded.user_id) == user_id
        assert decoded.email == email
        assert decoded.type == "access"

    def test_verify_token_success(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"
        token = jwt_manager.create_access_token(user_id, email)

        # Act
        result = jwt_manager.verify_token(token)

        # Assert
        assert result is True

    def test_verify_token_invalid(self, jwt_manager):
        # Arrange
        invalid_token = "invalid.token.here"

        # Act
        result = jwt_manager.verify_token(invalid_token)

        # Assert
        assert result is False

    def test_decode_token_invalid(self, jwt_manager):
        # Arrange
        invalid_token = "invalid.token.here"

        # Act & Assert
        with pytest.raises(Exception):  # Should raise JWTError or similar
            jwt_manager.decode_token(invalid_token)

    def test_extract_user_id_from_decoded_token(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"
        token = jwt_manager.create_access_token(user_id, email)

        # Act
        decoded = jwt_manager.decode_token(token)

        # Assert
        assert str(decoded.user_id) == user_id

    def test_token_contains_expected_claims(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"

        # Act
        token = jwt_manager.create_access_token(user_id, email)
        decoded = jwt_manager.decode_token(token)

        # Assert
        assert str(decoded.user_id) == user_id
        assert decoded.email == email
        assert decoded.type == "access"
        assert decoded.exp is not None
        assert decoded.iat is not None

    def test_refresh_token_longer_expiry(self, jwt_manager):
        # Arrange
        user_id = str(uuid4())
        email = "test@example.com"

        # Act
        access_token = jwt_manager.create_access_token(user_id, email)
        refresh_token = jwt_manager.create_refresh_token(user_id, email)

        # Decode both tokens
        access_decoded = jwt_manager.decode_token(access_token)
        refresh_decoded = jwt_manager.decode_token(refresh_token)

        # Assert - Refresh token should have longer expiry
        assert refresh_decoded.exp > access_decoded.exp
        assert access_decoded.type == "access"
        assert refresh_decoded.type == "refresh"

    def test_decoded_token_class(self):
        # Test DecodedToken class initialization
        user_id = str(uuid4())
        email = "test@example.com"
        exp = datetime.now(timezone.utc)
        iat = datetime.now(timezone.utc)
        token_type = "access"

        decoded = DecodedToken(user_id, email, exp, iat, token_type)

        assert str(decoded.user_id) == user_id
        assert decoded.email == email
        assert decoded.exp == exp
        assert decoded.iat == iat
        assert decoded.type == token_type
