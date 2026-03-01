from datetime import datetime, timezone

from src.app.domain.entities.token_payload import TokenPayload


class TestTokenPayload:
    def test_token_payload_creation(self):
        # Test that TokenPayload can be created with all required fields
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        assert payload.sub == "user123"
        assert payload.email == "test@example.com"
        assert payload.exp == exp_time
        assert payload.iat == now
        assert payload.type == "access"

    def test_token_payload_with_refresh_type(self):
        # Test TokenPayload with refresh token type
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload = TokenPayload(
            sub="user456",
            email="refresh@example.com",
            exp=exp_time,
            iat=now,
            type="refresh",
        )

        assert payload.sub == "user456"
        assert payload.email == "refresh@example.com"
        assert payload.type == "refresh"

    def test_token_payload_dataclass_properties(self):
        # Test that TokenPayload is a dataclass with proper properties
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload = TokenPayload(
            sub="user789",
            email="dataclass@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        # Test that it's a dataclass (has __dict__ and proper __repr__)
        assert hasattr(payload, "__dict__")
        assert "sub" in payload.__dict__
        assert "email" in payload.__dict__
        assert "exp" in payload.__dict__
        assert "iat" in payload.__dict__
        assert "type" in payload.__dict__

    def test_token_payload_equality(self):
        # Test that two TokenPayloads with same data are equal
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload1 = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        payload2 = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        assert payload1 == payload2

    def test_token_payload_inequality(self):
        # Test that TokenPayloads with different data are not equal
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload1 = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        payload2 = TokenPayload(
            sub="user456",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        assert payload1 != payload2

    def test_token_payload_repr(self):
        # Test that TokenPayload has a proper string representation
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        repr_str = repr(payload)
        assert "TokenPayload" in repr_str
        assert "user123" in repr_str
        assert "test@example.com" in repr_str
        assert "access" in repr_str

    def test_token_payload_field_types(self):
        # Test that fields have correct types
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        assert isinstance(payload.sub, str)
        assert isinstance(payload.email, str)
        assert isinstance(payload.exp, datetime)
        assert isinstance(payload.iat, datetime)
        assert isinstance(payload.type, str)

    def test_token_payload_with_different_datetimes(self):
        # Test TokenPayload with different datetime values
        iat_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        exp_time = datetime(2023, 1, 1, 13, 0, 0, tzinfo=timezone.utc)

        payload = TokenPayload(
            sub="user123",
            email="datetime@example.com",
            exp=exp_time,
            iat=iat_time,
            type="access",
        )

        assert payload.iat == iat_time
        assert payload.exp == exp_time
        assert payload.exp > payload.iat

    def test_token_payload_immutable_fields(self):
        # Test that dataclass fields are mutable by default (not frozen)
        now = datetime.now(timezone.utc)
        exp_time = datetime.now(timezone.utc)

        payload = TokenPayload(
            sub="user123",
            email="test@example.com",
            exp=exp_time,
            iat=now,
            type="access",
        )

        # Test that we can modify fields (dataclass is not frozen)
        original_sub = payload.sub
        payload.sub = "modified_user"
        assert payload.sub == "modified_user"
        assert payload.sub != original_sub
