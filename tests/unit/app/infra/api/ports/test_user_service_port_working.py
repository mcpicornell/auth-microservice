from abc import ABC
from uuid import UUID

import pytest

from src.app.infra.api.ports.user_service_port import UserServicePort


class TestUserServicePort:
    def test_user_service_port_is_abstract(self):
        """Test that UserServicePort is an abstract base class."""
        assert hasattr(UserServicePort, "__abstractmethods__")

        # Check that all required methods are abstract
        abstract_methods = UserServicePort.__abstractmethods__
        assert "create_user" in abstract_methods
        assert "login" in abstract_methods
        assert "get_user" in abstract_methods
        assert "get_user_by_email" in abstract_methods
        assert "update_user" in abstract_methods

    def test_user_service_port_inherits_from_abc(self):
        """Test that UserServicePort inherits from ABC."""
        assert issubclass(UserServicePort, ABC)

    def test_user_service_port_cannot_be_instantiated(self):
        """Test that UserServicePort cannot be instantiated directly."""
        with pytest.raises(TypeError):
            UserServicePort()

    def test_user_service_port_method_signatures(self):
        """Test that abstract methods have correct signatures."""
        import inspect

        # Check create_user signature
        create_user_sig = inspect.signature(UserServicePort.create_user)
        params = list(create_user_sig.parameters.keys())
        assert "self" in params
        assert "email" in params
        assert "username" in params
        assert "password" in params

        # Check login signature
        login_sig = inspect.signature(UserServicePort.login)
        params = list(login_sig.parameters.keys())
        assert "self" in params
        assert "email" in params
        assert "password" in params

        # Check get_user signature
        get_user_sig = inspect.signature(UserServicePort.get_user)
        params = list(get_user_sig.parameters.keys())
        assert "self" in params
        assert "user_id" in params

        # Check get_user_by_email signature
        get_user_by_email_sig = inspect.signature(UserServicePort.get_user_by_email)
        params = list(get_user_by_email_sig.parameters.keys())
        assert "self" in params
        assert "email" in params

        # Check update_user signature
        update_user_sig = inspect.signature(UserServicePort.update_user)
        params = list(update_user_sig.parameters.keys())
        assert "self" in params
        assert "user_id" in params
        assert "email" in params
        assert "username" in params
        assert "is_active" in params
        assert "is_admin" in params

    def test_concrete_implementation_can_be_created(self):
        """Test that a concrete implementation can be created."""

        class ConcreteUserService(UserServicePort):
            async def create_user(self, email: str, username: str, password: str):
                return {"success": True, "data": {}}

            async def login(self, email: str, password: str):
                return {"success": True, "data": {}}

            async def get_user(self, user_id: UUID):
                return {"success": True, "data": {}}

            async def get_user_by_email(self, email: str):
                return {"success": True, "data": {}}

            async def update_user(
                self,
                user_id: UUID,
                email=None,
                username=None,
                is_active=None,
                is_admin=None,
            ):
                return {"success": True, "data": {}}

        # Should be able to instantiate concrete implementation
        concrete_service = ConcreteUserService()
        assert concrete_service is not None
        assert isinstance(concrete_service, UserServicePort)
