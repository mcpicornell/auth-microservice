from uuid import uuid4

from src.app.infra.api.dto.responses import (
    CreateUserResponse,
    GetUserResponse,
    LoginResponse,
    UpdateUserResponse,
    UserResponse,
)


class TestUserResponse:
    def test_user_response_creation(self):
        user_id = uuid4()
        user = UserResponse(
            id=user_id,
            email="test@example.com",
            username="testuser",
            is_active=True,
            is_admin=False,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        assert user.id == user_id
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.is_active is True
        assert user.is_admin is False
        assert user.created_at == "2023-01-01T00:00:00Z"
        assert user.updated_at == "2023-01-01T00:00:00Z"


class TestCreateUserResponse:
    def test_create_user_response_success(self):
        user_id = uuid4()
        user = UserResponse(
            id=user_id,
            email="test@example.com",
            username="testuser",
            is_active=True,
            is_admin=False,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        response = CreateUserResponse(
            success=True,
            message="User created successfully",
            user=user,
        )

        assert response.success is True
        assert response.message == "User created successfully"
        assert response.user == user

    def test_create_user_response_failure(self):
        response = CreateUserResponse(
            success=False,
            message="Email already exists",
        )

        assert response.success is False
        assert response.message == "Email already exists"
        assert response.user is None


class TestLoginResponse:
    def test_login_response_creation(self):
        response = LoginResponse(
            access_token="access_token_123",
            refresh_token="refresh_token_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            username="testuser",
            token_type="bearer",
        )

        assert response.access_token == "access_token_123"
        assert response.refresh_token == "refresh_token_123"
        assert response.user_id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.email == "test@example.com"
        assert response.username == "testuser"
        assert response.token_type == "bearer"


class TestGetUserResponse:
    def test_get_user_response_success(self):
        user_id = uuid4()
        user = UserResponse(
            id=user_id,
            email="test@example.com",
            username="testuser",
            is_active=True,
            is_admin=False,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

        response = GetUserResponse(
            success=True,
            message="User found",
            user=user,
        )

        assert response.success is True
        assert response.message == "User found"
        assert response.user == user

    def test_get_user_response_not_found(self):
        response = GetUserResponse(
            success=False,
            message="User not found",
        )

        assert response.success is False
        assert response.message == "User not found"
        assert response.user is None


class TestUpdateUserResponse:
    def test_update_user_response_success(self):
        user_id = uuid4()
        user = UserResponse(
            id=user_id,
            email="updated@example.com",
            username="updateduser",
            is_active=True,
            is_admin=False,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-02T00:00:00Z",
        )

        response = UpdateUserResponse(
            success=True,
            message="User updated successfully",
            user=user,
        )

        assert response.success is True
        assert response.message == "User updated successfully"
        assert response.user == user

    def test_update_user_response_not_found(self):
        response = UpdateUserResponse(
            success=False,
            message="User not found",
        )

        assert response.success is False
        assert response.message == "User not found"
        assert response.user is None
