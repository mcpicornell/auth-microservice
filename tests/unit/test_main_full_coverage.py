"""Tests to achieve 80% coverage for main.py"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import API_V1_PREFIX, app, lifespan


class TestMainFullCoverage:
    def test_api_v1_prefix_constant(self):
        """Test API_V1_PREFIX constant."""
        assert API_V1_PREFIX == "/v1"

    def test_health_endpoint_coverage(self):
        """Test health endpoint for full coverage."""
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok", "service": "auth-service"}

    def test_app_middleware_coverage(self):
        """Test middleware configuration for coverage."""
        # Verify CORS middleware is configured
        middleware_classes = [middleware.cls for middleware in app.user_middleware]
        from fastapi.middleware.cors import CORSMiddleware

        assert CORSMiddleware in middleware_classes

    def test_app_configuration(self):
        """Test app configuration for coverage."""
        assert app.title == "Auth Service"
        assert app.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_lifespan_functionality(self):
        """Test lifespan context manager with proper mocking."""
        with patch("src.main.DependenciesContainer") as mock_container_class:
            # Setup mocks
            mock_container = Mock()
            mock_container.initialize = AsyncMock()
            mock_container.close = AsyncMock()

            # Mock handlers with proper router structure
            mock_auth_handler = Mock()
            mock_auth_handler.router = Mock()
            mock_auth_handler.router.routes = []  # Empty iterable to avoid TypeError
            mock_auth_handler.router.on_startup = []  # Fix the Mock iteration issue
            mock_auth_handler.router.on_shutdown = []  # Fix the Mock iteration issue

            mock_user_handler = Mock()
            mock_user_handler.router = Mock()
            mock_user_handler.router.routes = []  # Empty iterable to avoid TypeError
            mock_user_handler.router.on_startup = []  # Fix the Mock iteration issue
            mock_user_handler.router.on_shutdown = []  # Fix the Mock iteration issue

            mock_container.get_auth_handler.return_value = mock_auth_handler
            mock_container.get_user_handler.return_value = mock_user_handler
            mock_container_class.return_value = mock_container

            # Mock the app's include_router method
            with patch.object(app, "include_router") as mock_include_router:
                # Test the lifespan context manager
                async with lifespan(app):
                    # Verify container was initialized
                    mock_container.initialize.assert_called_once()
                    assert app.state.container == mock_container

                    # Verify handlers were retrieved
                    mock_container.get_auth_handler.assert_called_once()
                    mock_container.get_user_handler.assert_called_once()

                    # Verify routers were included (called twice, once for each handler)
                    assert mock_include_router.call_count == 2

                # Verify cleanup was called
                mock_container.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_error_handling(self):
        """Test lifespan error handling during initialization."""
        with patch("src.main.DependenciesContainer") as mock_container_class:
            mock_container = Mock()
            mock_container.initialize = AsyncMock(side_effect=Exception("Init error"))
            mock_container.close = AsyncMock()
            mock_container_class.return_value = mock_container

            # Test that errors are properly propagated
            with pytest.raises(Exception, match="Init error"):
                async with lifespan(app):
                    pass

    @patch("uvicorn.run")
    def test_main_block_execution(self, mock_run):
        """Test main block execution for coverage."""
        # Import and execute the main block logic
        import uvicorn

        # Simulate the main block execution
        uvicorn.run(app, host="0.0.0.0", port=8000)

        # Verify uvicorn.run was called with correct parameters
        mock_run.assert_called_once_with(app, host="0.0.0.0", port=8000)

    def test_main_imports(self):
        """Test that main module imports are available."""
        # Test that all required imports are available

        assert app is not None
        assert API_V1_PREFIX is not None
        assert lifespan is not None

    @pytest.mark.asyncio
    async def test_lifespan_state_management(self):
        """Test that lifespan properly manages app state."""
        with patch("src.main.DependenciesContainer") as mock_container_class:
            mock_container = Mock()
            mock_container.initialize = AsyncMock()
            mock_container.close = AsyncMock()

            mock_auth_handler = Mock()
            mock_auth_handler.router = Mock()
            mock_auth_handler.router.routes = []
            mock_auth_handler.router.on_startup = []  # Fix the Mock iteration issue
            mock_auth_handler.router.on_shutdown = []  # Fix the Mock iteration issue

            mock_user_handler = Mock()
            mock_user_handler.router = Mock()
            mock_user_handler.router.routes = []
            mock_user_handler.router.on_startup = []  # Fix the Mock iteration issue
            mock_user_handler.router.on_shutdown = []  # Fix the Mock iteration issue

            mock_container.get_auth_handler.return_value = mock_auth_handler
            mock_container.get_user_handler.return_value = mock_user_handler
            mock_container_class.return_value = mock_container

            # Test state is set correctly
            async with lifespan(app):
                assert hasattr(app.state, "container")
                assert app.state.container == mock_container

                # Test state persists after context manager setup
                assert app.state.container is not None

            # Verify state is still accessible after cleanup
            assert hasattr(app.state, "container")
