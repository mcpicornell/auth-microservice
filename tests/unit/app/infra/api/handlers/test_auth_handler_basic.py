from unittest.mock import Mock

import pytest

from src.app.infra.api.handlers.auth_handler import AuthHandler


class TestAuthHandler:
    @pytest.fixture
    def mock_user_service(self):
        service = Mock()
        return service

    @pytest.fixture
    def auth_handler(self, mock_user_service):
        return AuthHandler(mock_user_service)

    def test_initialization(self, mock_user_service):
        # Test that AuthHandler initializes correctly
        handler = AuthHandler(mock_user_service)
        
        assert handler.user_service == mock_user_service
        assert handler.router is not None
        assert handler.router.prefix == "/auth"
        assert "authentication" in handler.router.tags

    def test_router_has_routes_with_prefix(self, auth_handler):
        # Test that router has the expected routes with prefix
        routes = [route.path for route in auth_handler.router.routes]
        
        assert "/auth/register" in routes
        assert "/auth/login" in routes
        assert "/auth/me" in routes

    def test_router_setup_called(self, auth_handler):
        # Test that _setup_routes was called during initialization
        # If routes exist, _setup_routes was called
        routes = list(auth_handler.router.routes)
        assert len(routes) >= 3  # Should have register, login, and me routes

    def test_user_service_dependency_injection(self, mock_user_service):
        # Test that the user service is properly injected
        handler = AuthHandler(mock_user_service)
        assert handler.user_service is mock_user_service

    def test_router_configuration(self, auth_handler):
        # Test router configuration
        router = auth_handler.router
        
        assert router.prefix == "/auth"
        assert "authentication" in router.tags
        assert len(router.routes) > 0
