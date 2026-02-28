from httpx import AsyncClient
from uuid import uuid4

from src.main import app


class TestMain:
    
    async def test_health_endpoint(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert data["service"] == "auth-service"
    
    async def test_create_user_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_data = {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
            
            response = await ac.post("/users/", json=user_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["username"] == "testuser"
            assert data["is_active"] is True
            assert data["is_admin"] is False
            assert "id" in data
            assert "created_at" in data
            assert "updated_at" in data
    
    async def test_create_user_duplicate_email_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_data = {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
            
            await ac.post("/users/", json=user_data)
            
            duplicate_user = {
                "email": "test@example.com",
                "username": "differentuser",
                "password": "password123"
            }
            
            response = await ac.post("/users/", json=duplicate_user)
            
            assert response.status_code == 400
            assert "Email already registered" in response.json()["detail"]
    
    async def test_update_user_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            create_data = {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
            
            create_response = await ac.post("/users/", json=create_data)
            user_id = create_response.json()["id"]
            
            update_data = {
                "email": "updated@example.com",
                "is_active": False
            }
            
            response = await ac.patch(f"/users/{user_id}", json=update_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "updated@example.com"
            assert data["username"] == "testuser"
            assert data["is_active"] is False
            assert data["is_admin"] is False
    
    async def test_get_user_by_id_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            create_data = {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
            
            create_response = await ac.post("/users/", json=create_data)
            user_id = create_response.json()["id"]
            
            response = await ac.get(f"/users/{user_id}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == user_id
            assert data["email"] == "test@example.com"
            assert data["username"] == "testuser"
