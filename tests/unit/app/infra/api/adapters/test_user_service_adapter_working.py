from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.infra.api.adapters.user_service_adapter import (
    DomainAuthServiceInterface,
    UserServiceAdapter,
)
from src.app.infra.api.dto.responses import (
    CreateUserResponse,
    GetUserResponse,
    LoginResponse,
    UpdateUserResponse,
)


class TestUserServiceAdapter:
    def test_user_service_adapter_initialization(self):
        """Test UserServiceAdapter initialization."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)

        adapter = UserServiceAdapter(mock_auth_service)

        assert adapter.auth_service == mock_auth_service

    @pytest.mark.asyncio
    async def test_create_user(self):
        """Test create_user method."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=CreateUserResponse)
        mock_auth_service.create_user = AsyncMock(return_value=mock_response)

        # Call the method
        result = await adapter.create_user(
            "test@example.com", "testuser", "password123"
        )

        # Verify result and call
        assert result == mock_response
        mock_auth_service.create_user.assert_called_once_with(
            "test@example.com", "testuser", "password123"
        )

    @pytest.mark.asyncio
    async def test_login(self):
        """Test login method."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=LoginResponse)
        mock_auth_service.login = AsyncMock(return_value=mock_response)

        # Call the method
        result = await adapter.login("test@example.com", "password123")

        # Verify result and call
        assert result == mock_response
        mock_auth_service.login.assert_called_once_with(
            "test@example.com", "password123"
        )

    @pytest.mark.asyncio
    async def test_get_user(self):
        """Test get_user method."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=GetUserResponse)
        mock_auth_service.get_user = AsyncMock(return_value=mock_response)

        # Call the method
        user_id = uuid4()
        result = await adapter.get_user(user_id)

        # Verify result and call
        assert result == mock_response
        mock_auth_service.get_user.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email(self):
        """Test get_user_by_email method."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=GetUserResponse)
        mock_auth_service.get_user_by_email = AsyncMock(return_value=mock_response)

        # Call the method
        result = await adapter.get_user_by_email("test@example.com")

        # Verify result and call
        assert result == mock_response
        mock_auth_service.get_user_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_update_user(self):
        """Test update_user method."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=UpdateUserResponse)
        mock_auth_service.update_user = AsyncMock(return_value=mock_response)

        # Call the method
        user_id = uuid4()
        result = await adapter.update_user(
            user_id,
            email="updated@example.com",
            username="updateduser",
            is_active=False,
            is_admin=True,
        )

        # Verify result and call
        assert result == mock_response
        mock_auth_service.update_user.assert_called_once_with(
            user_id, "updated@example.com", "updateduser", False, True
        )

    @pytest.mark.asyncio
    async def test_update_user_partial(self):
        """Test update_user method with partial data."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=UpdateUserResponse)
        mock_auth_service.update_user = AsyncMock(return_value=mock_response)

        # Call the method with only some parameters
        user_id = uuid4()
        result = await adapter.update_user(user_id, email="updated@example.com")

        # Verify result and call
        assert result == mock_response
        mock_auth_service.update_user.assert_called_once_with(
            user_id, "updated@example.com", None, None, None
        )

    @pytest.mark.asyncio
    async def test_update_user_no_parameters(self):
        """Test update_user method with no parameters."""
        mock_auth_service = Mock(spec=DomainAuthServiceInterface)
        adapter = UserServiceAdapter(mock_auth_service)

        # Mock service response
        mock_response = Mock(spec=UpdateUserResponse)
        mock_auth_service.update_user = AsyncMock(return_value=mock_response)

        # Call the method with no optional parameters
        user_id = uuid4()
        result = await adapter.update_user(user_id)

        # Verify result and call
        assert result == mock_response
        mock_auth_service.update_user.assert_called_once_with(
            user_id, None, None, None, None
        )


class TestDomainAuthServiceInterface:
    def test_domain_auth_service_interface_is_abstract(self):
        """Test that DomainAuthServiceInterface is an abstract base class."""
        assert hasattr(DomainAuthServiceInterface, "__abstractmethods__")

        # Check that all required methods are abstract
        abstract_methods = DomainAuthServiceInterface.__abstractmethods__
        assert "create_user" in abstract_methods
        assert "login" in abstract_methods
        assert "get_user" in abstract_methods
        assert "get_user_by_email" in abstract_methods
        assert "update_user" in abstract_methods

    def test_domain_auth_service_interface_cannot_be_instantiated(self):
        """Test that DomainAuthServiceInterface cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DomainAuthServiceInterface()

    def test_domain_auth_service_interface_method_signatures(self):
        """Test that abstract methods have correct signatures."""
        import inspect

        # Check create_user signature
        create_user_sig = inspect.signature(DomainAuthServiceInterface.create_user)
        params = list(create_user_sig.parameters.keys())
        assert "self" in params
        assert "email" in params
        assert "username" in params
        assert "password" in params

        # Check login signature
        login_sig = inspect.signature(DomainAuthServiceInterface.login)
        params = list(login_sig.parameters.keys())
        assert "self" in params
        assert "email" in params
        assert "password" in params

        # Check get_user signature
        get_user_sig = inspect.signature(DomainAuthServiceInterface.get_user)
        params = list(get_user_sig.parameters.keys())
        assert "self" in params
        assert "user_id" in params

        # Check get_user_by_email signature
        get_user_by_email_sig = inspect.signature(
            DomainAuthServiceInterface.get_user_by_email
        )
        params = list(get_user_by_email_sig.parameters.keys())
        assert "self" in params
        assert "email" in params

        # Check update_user signature
        update_user_sig = inspect.signature(DomainAuthServiceInterface.update_user)
        params = list(update_user_sig.parameters.keys())
        assert "self" in params
        assert "user_id" in params
        assert "email" in params
        assert "username" in params
        assert "is_active" in params
        assert "is_admin" in params
