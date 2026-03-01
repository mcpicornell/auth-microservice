from unittest.mock import patch

import pytest

from src.app.settings.app_settings import Settings


class TestAppSettings:
    def test_app_settings_default_values(self):
        """Test AppSettings with default values."""
        with patch.dict("os.environ", {}, clear=True):
            settings = Settings()

            # Test default values (from .env.pro file)
            assert (
                settings.DB_SQL_URL
                == "postgresql://user:password@localhost:5432/auth_db"
            )
            assert settings.DB_SQL_ECHO is False
            assert (
                settings.JWT_SECRET_KEY == "dev-secret-key-change-in-production-12345"
            )
            assert settings.JWT_ALGORITHM == "HS256"
            assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
            assert settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS == 7
            assert settings.RABBITMQ_HOST == "localhost"
            assert settings.RABBITMQ_PORT == 5672
            assert settings.RABBITMQ_USER == "guest"
            assert settings.RABBITMQ_PASSWORD == "guest"
            assert settings.RABBITMQ_VHOST == "/"
            assert settings.APP_NAME == "Auth Service"
            assert settings.DEBUG is True

    def test_app_settings_from_environment(self):
        """Test AppSettings loading from environment variables."""
        env_vars = {
            "DB_SQL_URL": "postgresql://user:pass@localhost/db",
            "DB_SQL_ECHO": "true",
            "JWT_SECRET_KEY": "test_secret_key",
            "JWT_ALGORITHM": "RS256",
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES": "60",
            "JWT_REFRESH_TOKEN_EXPIRE_DAYS": "14",
            "RABBITMQ_HOST": "rabbitmq.example.com",
            "RABBITMQ_PORT": "5673",
            "RABBITMQ_USER": "admin",
            "RABBITMQ_PASSWORD": "admin123",
            "RABBITMQ_VHOST": "/test_vhost",
        }

        with patch.dict("os.environ", env_vars, clear=True):
            settings = Settings()

            assert settings.DB_SQL_URL == "postgresql://user:pass@localhost/db"
            assert settings.DB_SQL_ECHO is True
            assert settings.JWT_SECRET_KEY == "test_secret_key"
            assert settings.JWT_ALGORITHM == "RS256"
            assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 60
            assert settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS == 14
            assert settings.RABBITMQ_HOST == "rabbitmq.example.com"
            assert settings.RABBITMQ_PORT == 5673
            assert settings.RABBITMQ_USER == "admin"
            assert settings.RABBITMQ_PASSWORD == "admin123"
            assert settings.RABBITMQ_VHOST == "/test_vhost"

    def test_app_settings_partial_environment(self):
        """Test AppSettings with partial environment variables."""
        env_vars = {
            "JWT_SECRET_KEY": "partial_secret",
            "RABBITMQ_HOST": "partial-host",
        }

        with patch.dict("os.environ", env_vars, clear=True):
            settings = Settings()

            # Environment variables should be loaded
            assert settings.JWT_SECRET_KEY == "partial_secret"
            assert settings.RABBITMQ_HOST == "partial-host"

            # Default values should be used for missing variables
            assert (
                settings.DB_SQL_URL
                == "postgresql://user:password@localhost:5432/auth_db"
            )
            assert settings.DB_SQL_ECHO is False
            assert settings.JWT_ALGORITHM == "HS256"
            assert settings.RABBITMQ_PORT == 5672
            assert settings.RABBITMQ_USER == "guest"

    def test_app_settings_boolean_conversion(self):
        """Test boolean conversion for DB_SQL_ECHO."""
        # Test various boolean string representations
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
        ]

        for env_value, expected in test_cases:
            with patch.dict("os.environ", {"DB_SQL_ECHO": env_value}, clear=True):
                settings = Settings()
                assert settings.DB_SQL_ECHO == expected, f"Failed for {env_value}"

    def test_app_settings_integer_conversion(self):
        """Test integer conversion for numeric settings."""
        env_vars = {
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES": "120",
            "JWT_REFRESH_TOKEN_EXPIRE_DAYS": "30",
            "RABBITMQ_PORT": "1234",
        }

        with patch.dict("os.environ", env_vars, clear=True):
            settings = Settings()

            assert isinstance(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES, int)
            assert isinstance(settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS, int)
            assert isinstance(settings.RABBITMQ_PORT, int)

            assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 120
            assert settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS == 30
            assert settings.RABBITMQ_PORT == 1234

    def test_app_settings_invalid_integer(self):
        """Test handling of invalid integer values."""
        with patch.dict("os.environ", {"RABBITMQ_PORT": "invalid_port"}, clear=True):
            # This should raise a validation error
            with pytest.raises(ValueError):
                Settings()

    def test_app_settings_model_validation(self):
        """Test Pydantic model validation."""
        # Test invalid JWT algorithm
        with patch.dict("os.environ", {"JWT_ALGORITHM": "INVALID_ALGO"}, clear=True):
            # This should not raise an error for string fields, but we can test the field exists
            settings = Settings()
            assert settings.JWT_ALGORITHM == "INVALID_ALGO"

    def test_app_settings_immutability(self):
        """Test that settings are mutable after creation."""
        with patch.dict("os.environ", {}, clear=True):
            settings = Settings()

            # Settings should be mutable (Pydantic models are mutable by default)
            settings.JWT_SECRET_KEY = "new_secret"
            assert settings.JWT_SECRET_KEY == "new_secret"

    def test_app_settings_repr(self):
        """Test string representation of settings."""
        with patch.dict("os.environ", {}, clear=True):
            settings = Settings()

            repr_str = repr(settings)
            assert "Settings" in repr_str
            assert "DB_SQL_URL" in repr_str

    def test_app_settings_equality(self):
        """Test settings equality comparison."""
        with patch.dict("os.environ", {}, clear=True):
            settings1 = Settings()
            settings2 = Settings()

            # Same environment should produce equal settings
            assert settings1 == settings2

    def test_get_settings_function(self):
        """Test the get_settings function."""
        from src.app.settings import get_settings

        with patch.dict("os.environ", {}, clear=True):
            settings = get_settings()

            assert isinstance(settings, Settings)
            assert (
                settings.DB_SQL_URL
                == "postgresql://user:password@localhost:5432/auth_db"
            )

    def test_settings_singleton_behavior(self):
        """Test that get_settings returns consistent results."""
        from src.app.settings import get_settings

        with patch.dict("os.environ", {}, clear=True):
            settings1 = get_settings()
            settings2 = get_settings()

            # Should return the same configuration
            assert settings1.DB_SQL_URL == settings2.DB_SQL_URL
            assert settings1.JWT_SECRET_KEY == settings2.JWT_SECRET_KEY
