from src.main import API_V1_PREFIX, app, lifespan


class TestMainUnit:
    def test_app_exists(self):
        # Test that the FastAPI app exists
        assert app is not None
        assert hasattr(app, "title")

    def test_app_has_title(self):
        # Test that the app has a title
        assert app.title is not None
        assert len(app.title) > 0
        assert app.title == "Auth Service"

    def test_app_has_version(self):
        # Test that the app has a version
        assert hasattr(app, "version")
        assert app.version == "1.0.0"

    def test_app_has_routes(self):
        # Test that the app has routes configured
        routes = [route.path for route in app.routes]
        assert len(routes) > 0

    def test_app_configuration(self):
        # Test basic app configuration
        # Check that app has expected attributes
        assert hasattr(app, "include_router")
        assert hasattr(app, "add_middleware")

    def test_app_imports(self):
        # Test that main module can be imported without errors
        import src.main

        assert src.main is not None
        assert hasattr(src.main, "app")

    def test_app_is_fastapi_instance(self):
        # Test that app is a FastAPI instance
        from fastapi import FastAPI

        assert isinstance(app, FastAPI)

        # Check if it has FastAPI-specific methods
        assert hasattr(app, "include_router")
        assert hasattr(app, "add_middleware")
        assert hasattr(app, "get")
        assert hasattr(app, "post")
        assert hasattr(app, "put")
        assert hasattr(app, "delete")

    def test_lifespan_function_exists(self):
        # Test that lifespan function exists
        assert lifespan is not None
        assert callable(lifespan)

    def test_api_v1_prefix_constant(self):
        # Test that API_V1_PREFIX constant exists
        assert API_V1_PREFIX is not None
        assert API_V1_PREFIX == "/v1"

    def test_app_is_singleton(self):
        # Test that app is the same instance when imported multiple times
        from src.main import app as app1
        from src.main import app as app2

        assert app1 is app2
