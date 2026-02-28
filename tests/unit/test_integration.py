import pytest
from fastapi.testclient import TestClient


def test_main_app_creation():
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from src.main import app
    
    assert app is not None
    assert app.title == "Auth Service"
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "auth-service"}


def test_dependencies_container_import():
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from src.app.dependencies_container import DependenciesContainer
    from src.app.settings import get_settings
    
    settings = get_settings()
    container = DependenciesContainer(settings)
    
    assert container is not None
    assert container.settings == settings


def test_domain_entities_creation():
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from src.app.domain.entities.user import CreateUserInput, UserEntity
    from uuid import uuid4
    
    user_input = CreateUserInput(
        email="test@example.com",
        username="testuser",
        password="password123"
    )
    assert user_input.email == "test@example.com"
    assert user_input.username == "testuser"
    assert user_input.password == "password123"
    
    user_id = uuid4()
    user_entity = UserEntity(
        id=user_id,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    assert user_entity.id == user_id
    assert user_entity.email == "test@example.com"
    assert user_entity.is_active == True


if __name__ == "__main__":
    pytest.main([__file__])
