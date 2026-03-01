from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import HTTPException, status

from src.app.infra.api.adapters.user_service_adapter import UserServiceAdapter
from src.app.infra.api.handlers.user_handler import UserHandler
from src.app.infra.api.schemas import CreateUserRequest, UpdateUserRequest


class TestUserHandler:
    def test_user_handler_initialization(self):
        """Test UserHandler initialization."""
        mock_user_service = Mock(spec=UserServiceAdapter)

        handler = UserHandler(mock_user_service)

        assert handler.user_service == mock_user_service
        assert handler.router.prefix == "/users"
        assert handler.router.tags == ["users"]

    @pytest.mark.asyncio
    async def test_create_user_success(self):
        """Test successful user creation."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock successful service response
        mock_result = {
            "success": True,
            "data": {
                "id": str(uuid4()),
                "email": "test@example.com",
                "username": "testuser",
                "is_active": True,
                "is_admin": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
        }

        mock_user_service.create_user = AsyncMock(return_value=mock_result)

        # Get the create_user endpoint from router
        create_route = None
        for route in handler.router.routes:
            if route.path == "/users/" and "POST" in route.methods:
                create_route = route.endpoint
                break

        assert create_route is not None

        # Call the endpoint
        request_data = CreateUserRequest(
            email="test@example.com", username="testuser", password="password123"
        )

        result = await create_route(request_data)

        assert result.email == "test@example.com"
        assert result.username == "testuser"
        assert result.is_active is True
        assert result.is_admin is False

        mock_user_service.create_user.assert_called_once_with(
            email="test@example.com",
            username="testuser",
            password="password123",
        )

    @pytest.mark.asyncio
    async def test_create_user_failure(self):
        """Test failed user creation."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock failed service response
        mock_result = {"success": False, "message": "Email already exists"}

        mock_user_service.create_user = AsyncMock(return_value=mock_result)

        # Get the create_user endpoint from router
        create_route = None
        for route in handler.router.routes:
            if route.path == "/users/" and "POST" in route.methods:
                create_route = route.endpoint
                break

        assert create_route is not None

        # Call the endpoint and expect HTTPException
        request_data = CreateUserRequest(
            email="test@example.com", username="testuser", password="password123"
        )

        with pytest.raises(HTTPException) as exc_info:
            await create_route(request_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "Email already exists"

    @pytest.mark.asyncio
    async def test_create_user_value_error(self):
        """Test user creation with ValueError from service."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock service raising ValueError
        mock_user_service.create_user = AsyncMock(
            side_effect=ValueError("Invalid input")
        )

        # Get the create_user endpoint from router
        create_route = None
        for route in handler.router.routes:
            if route.path == "/users/" and "POST" in route.methods:
                create_route = route.endpoint
                break

        assert create_route is not None

        # Call the endpoint and expect HTTPException
        request_data = CreateUserRequest(
            email="test@example.com", username="testuser", password="password123"
        )

        with pytest.raises(HTTPException) as exc_info:
            await create_route(request_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "Invalid input"

    @pytest.mark.asyncio
    async def test_update_user_success(self):
        """Test successful user update."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock successful service response
        mock_result = {
            "success": True,
            "data": {
                "id": str(uuid4()),
                "email": "updated@example.com",
                "username": "updateduser",
                "is_active": False,
                "is_admin": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
        }

        mock_user_service.update_user = AsyncMock(return_value=mock_result)

        # Get the update_user endpoint from router
        update_route = None
        for route in handler.router.routes:
            if route.path == "/users/{user_id}":
                update_route = route.endpoint
                break

        assert update_route is not None

        # Call the endpoint
        user_id = uuid4()
        request_data = UpdateUserRequest(
            email="updated@example.com",
            username="updateduser",
            is_active=False,
            is_admin=True,
        )

        result = await update_route(user_id, request_data)

        assert result.email == "updated@example.com"
        assert result.username == "updateduser"
        assert result.is_active is False
        assert result.is_admin is True

        mock_user_service.update_user.assert_called_once_with(
            user_id=user_id,
            email="updated@example.com",
            username="updateduser",
            is_active=False,
            is_admin=True,
        )

    @pytest.mark.asyncio
    async def test_update_user_failure(self):
        """Test failed user update."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock failed service response
        mock_result = {"success": False, "message": "User not found"}

        mock_user_service.update_user = AsyncMock(return_value=mock_result)

        # Get the update_user endpoint from router
        update_route = None
        for route in handler.router.routes:
            if route.path == "/users/{user_id}":
                update_route = route.endpoint
                break

        assert update_route is not None

        # Call the endpoint and expect HTTPException
        user_id = uuid4()
        request_data = UpdateUserRequest(email="updated@example.com")

        with pytest.raises(HTTPException) as exc_info:
            await update_route(user_id, request_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "User not found"

    @pytest.mark.asyncio
    async def test_get_user_success(self):
        """Test successful user retrieval by ID."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock successful service response
        mock_result = {
            "success": True,
            "data": {
                "id": str(uuid4()),
                "email": "test@example.com",
                "username": "testuser",
                "is_active": True,
                "is_admin": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
        }

        mock_user_service.get_user = AsyncMock(return_value=mock_result)

        # Get the get_user endpoint from router
        get_route = None
        for route in handler.router.routes:
            if route.path == "/users/{user_id}" and "GET" in route.methods:
                get_route = route.endpoint
                break

        assert get_route is not None

        # Call the endpoint
        user_id = uuid4()
        result = await get_route(user_id)

        assert result.email == "test@example.com"
        assert result.username == "testuser"

        mock_user_service.get_user.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self):
        """Test user retrieval when user not found."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock failed service response
        mock_result = {"success": False, "message": "User not found"}

        mock_user_service.get_user = AsyncMock(return_value=mock_result)

        # Get the get_user endpoint from router
        get_route = None
        for route in handler.router.routes:
            if route.path == "/users/{user_id}" and "GET" in route.methods:
                get_route = route.endpoint
                break

        assert get_route is not None

        # Call the endpoint and expect HTTPException
        user_id = uuid4()

        with pytest.raises(HTTPException) as exc_info:
            await get_route(user_id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self):
        """Test successful user retrieval by email."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock successful service response
        mock_result = {
            "success": True,
            "data": {
                "id": str(uuid4()),
                "email": "test@example.com",
                "username": "testuser",
                "is_active": True,
                "is_admin": False,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
        }

        mock_user_service.get_user_by_email = AsyncMock(return_value=mock_result)

        # Get the get_user_by_email endpoint from router
        get_email_route = None
        for route in handler.router.routes:
            if route.path == "/users/email/{email}":
                get_email_route = route.endpoint
                break

        assert get_email_route is not None

        # Call the endpoint
        result = await get_email_route("test@example.com")

        assert result.email == "test@example.com"
        assert result.username == "testuser"

        mock_user_service.get_user_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self):
        """Test user retrieval by email when user not found."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Mock failed service response
        mock_result = {"success": False, "message": "User not found"}

        mock_user_service.get_user_by_email = AsyncMock(return_value=mock_result)

        # Get the get_user_by_email endpoint from router
        get_email_route = None
        for route in handler.router.routes:
            if route.path == "/users/email/{email}":
                get_email_route = route.endpoint
                break

        assert get_email_route is not None

        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_email_route("nonexistent@example.com")

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"

    @pytest.mark.asyncio
    async def test_list_users(self):
        """Test list users endpoint."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Get the list_users endpoint from router
        list_route = None
        for route in handler.router.routes:
            if route.path == "/users/" and "GET" in route.methods:
                list_route = route.endpoint
                break

        assert list_route is not None

        # Call the endpoint
        result = await list_route()

        assert isinstance(result, dict)
        assert result["message"] == "List users endpoint"

    def test_router_setup(self):
        """Test that router is properly set up with all routes."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        # Check that router has the expected routes
        route_paths = [route.path for route in handler.router.routes]

        assert "/users/" in route_paths  # Create and list users
        assert "/users/{user_id}" in route_paths  # Update and get user
        assert "/users/email/{email}" in route_paths  # Get user by email

        # Check that we have the right number of routes
        assert len(handler.router.routes) == 5

    def test_router_configuration(self):
        """Test router configuration."""
        mock_user_service = Mock(spec=UserServiceAdapter)
        handler = UserHandler(mock_user_service)

        router = handler.router

        assert router.prefix == "/users"
        assert router.tags == ["users"]
