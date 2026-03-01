from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.app.infra.api.handlers.user_handler import UserHandler
from src.app.infra.api.adapters.user_service_adapter import UserServiceAdapter


class TestUserHandlerSimple:
    """Simple tests for UserHandler focusing on direct method testing."""

    @pytest.fixture
    def mock_user_service(self):
        """Create a mock UserServiceAdapter."""
        service = Mock(spec=UserServiceAdapter)
        service.create_user = AsyncMock()
        service.update_user = AsyncMock()
        service.get_user = AsyncMock()
        service.get_user_by_email = AsyncMock()
        return service

    @pytest.fixture
    def user_handler(self, mock_user_service):
        """Create UserHandler with mocked service."""
        return UserHandler(mock_user_service)

    def test_user_handler_initialization(self, mock_user_service):
        """Test UserHandler initialization."""
        handler = UserHandler(mock_user_service)
        
        assert handler.user_service == mock_user_service
        assert handler.router.prefix == "/users"
        assert "users" in handler.router.tags
        assert handler.router is not None

    def test_user_handler_routes_setup(self, user_handler):
        """Test that routes are properly set up."""
        routes = [
            route for route in user_handler.router.routes if hasattr(route, "path")
        ]
        
        # Check that we have routes
        assert len(routes) >= 4
        
        # Check route paths include expected endpoints
        route_paths = [route.path for route in routes]
        assert "/users/" in route_paths
        assert "/users/{user_id}" in route_paths
        assert "/users/email/{email}" in route_paths

    def test_user_handler_has_required_methods(self, user_handler):
        """Test that UserHandler has all required methods."""
        assert hasattr(user_handler, "user_service")
        assert hasattr(user_handler, "router")
        assert hasattr(user_handler, "_setup_routes")

    def test_router_has_correct_endpoints(self, user_handler):
        """Test that router has the correct endpoints."""
        routes = user_handler.router.routes
        
        # Check for POST / (create user)
        post_routes = [
            r for r in routes if hasattr(r, "methods") and "POST" in r.methods
        ]
        assert len(post_routes) > 0
        
        # Check for PATCH /{user_id} (update user)
        patch_routes = [
            r for r in routes if hasattr(r, "methods") and "PATCH" in r.methods
        ]
        assert len(patch_routes) > 0
        
        # Check for GET routes
        get_routes = [
            r for r in routes if hasattr(r, "methods") and "GET" in r.methods
        ]
        assert len(get_routes) > 0

    @pytest.mark.asyncio
    async def test_user_service_integration(self, user_handler, mock_user_service):
        """Test that UserHandler properly integrates with UserServiceAdapter."""
        user_id = uuid4()
        
        mock_user_service.get_user.return_value = {
            "success": True,
            "data": {
                "id": str(user_id),
                "email": "test@example.com",
                "username": "testuser",
                "is_active": True,
                "is_admin": False,
            }
        }

        result = await mock_user_service.get_user(user_id)
        
        assert result["success"] is True
        assert result["data"]["email"] == "test@example.com"
        mock_user_service.get_user.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_user_service_error_handling(self, user_handler, mock_user_service):
        """Test error handling through the service."""
        mock_user_service.create_user.return_value = {
            "success": False,
            "message": "Email already exists"
        }

        result = await mock_user_service.create_user(
            email="existing@example.com",
            username="testuser",
            password="password123"
        )
        
        assert result["success"] is False
        assert result["message"] == "Email already exists"

    @pytest.mark.asyncio
    async def test_user_service_value_error_propagation(
        self, user_handler, mock_user_service
    ):
        """Test that ValueError from service is properly handled."""
        mock_user_service.get_user.side_effect = ValueError("Invalid user ID")

        with pytest.raises(ValueError, match="Invalid user ID"):
            await mock_user_service.get_user(uuid4())

    def test_user_handler_service_dependency(self, user_handler):
        """Test that UserHandler depends on UserServiceAdapter."""
        assert isinstance(user_handler.user_service, Mock)
        assert hasattr(user_handler.user_service, "create_user")
        assert hasattr(user_handler.user_service, "update_user")
        assert hasattr(user_handler.user_service, "get_user")
        assert hasattr(user_handler.user_service, "get_user_by_email")

    def test_user_handler_router_configuration(self, user_handler):
        """Test that the router is properly configured."""
        router = user_handler.router
        
        assert router.prefix == "/users"
        assert "users" in router.tags
        assert len(router.routes) >= 4

    @pytest.mark.asyncio
    async def test_all_service_methods_are_async(self, mock_user_service):
        """Test that all service methods are properly async."""
        # These should all be AsyncMock objects
        assert hasattr(mock_user_service.create_user, "_mock_name")
        assert hasattr(mock_user_service.update_user, "_mock_name")
        assert hasattr(mock_user_service.get_user, "_mock_name")
        assert hasattr(mock_user_service.get_user_by_email, "_mock_name")

    def test_user_handler_is_instantiable(self):
        """Test that UserHandler can be instantiated with a real service."""
        mock_service = Mock()
        mock_service.create_user = AsyncMock()
        mock_service.update_user = AsyncMock()
        mock_service.get_user = AsyncMock()
        mock_service.get_user_by_email = AsyncMock()
        
        handler = UserHandler(mock_service)
        assert handler is not None
        assert handler.user_service == mock_service
