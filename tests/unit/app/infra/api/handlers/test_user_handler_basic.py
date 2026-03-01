from unittest.mock import Mock

import pytest

from src.app.infra.api.handlers.user_handler import UserHandler


class TestUserHandler:
    @pytest.fixture
    def mock_user_service(self):
        service = Mock()
        return service

    @pytest.fixture
    def user_handler(self, mock_user_service):
        return UserHandler(mock_user_service)

    def test_initialization(self, mock_user_service):
        # Test that UserHandler initializes correctly
        handler = UserHandler(mock_user_service)

        assert handler.user_service == mock_user_service
        assert handler.router is not None
        assert handler.router.prefix == "/users"
        assert "users" in handler.router.tags

    def test_router_has_routes_with_prefix(self, user_handler):
        # Test that router has the expected routes with prefix
        routes = [route.path for route in user_handler.router.routes]

        assert "/users/" in routes
        assert "/users/{user_id}" in routes

    def test_router_setup_called(self, user_handler):
        # Test that _setup_routes was called during initialization
        # If routes exist, _setup_routes was called
        routes = list(user_handler.router.routes)
        assert len(routes) >= 2  # Should have get users and get user by id routes

    def test_user_service_dependency_injection(self, mock_user_service):
        # Test that the user service is properly injected
        handler = UserHandler(mock_user_service)
        assert handler.user_service is mock_user_service

    def test_router_configuration(self, user_handler):
        # Test router configuration
        router = user_handler.router

        assert router.prefix == "/users"
        assert "users" in router.tags
        assert len(router.routes) > 0

    def test_get_users_route_exists(self, user_handler):
        # Test that get users route exists (actually it's a create user route)
        routes = [
            route for route in user_handler.router.routes if route.path == "/users/"
        ]
        assert len(routes) > 0
        assert routes[0].methods.__contains__("POST")

    def test_get_user_by_id_route_exists(self, user_handler):
        # Test that get user by id route exists (actually it's an update user route)
        routes = [
            route
            for route in user_handler.router.routes
            if route.path == "/users/{user_id}"
        ]
        assert len(routes) > 0
        assert routes[0].methods.__contains__("PATCH")
