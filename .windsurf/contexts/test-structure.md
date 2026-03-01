# Test Structure Documentation

## Overview

This document describes the test structure and organization for the auth-microservice project following hexagonal/clean architecture principles.

## Test Directory Structure

```
tests/
├── __init__.py
├── integration/
│   └── __init__.py
└── unit/
    ├── __init__.py
    ├── app/
    │   ├── __init__.py
    │   ├── adapters/
    │   │   ├── __init__.py
    │   │   ├── database/
    │   │   │   ├── __init__.py
    │   │   │   └── test_user_adapter.py
    │   │   ├── messaging/
    │   │   │   ├── __init__.py
    │   │   │   └── test_rabbitmq_adapter.py
    │   │   └── security/
    │   │       ├── __init__.py
    │   │       ├── test_jwt_adapter.py
    │   │       └── test_password_adapter.py
    │   ├── domain/
    │   │   └── entities/
    │   │       ├── __init__.py
    │   │       └── test_user.py
    │   ├── infra/
    │   │   ├── auth/
    │   │   │   └── test_jwt_manager.py
    │   │   ├── database/
    │   │   │   └── repositories/
    │   │   │       └── test_user_repository.py
    │   │   └── messaging/
    │   │       └── test_rabbitmq_manager.py
    │   └── test_dependencies_container.py
    ├── test_adapters_architecture.py
    ├── test_architecture_rules.py
    └── test_integration.py
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)

#### Application Layer Tests (`tests/unit/app/`)

- **Dependencies Container Tests** (`test_dependencies_container.py`)
  - Tests dependency injection and initialization
  - Validates proper creation of managers, adapters, services, and handlers
  - Tests cleanup and resource management

- **Adapter Tests** (`tests/unit/app/adapters/`)
  - **Database Adapters**: Test data transformation and repository interactions
  - **Security Adapters**: Test token creation, password hashing, and verification
  - **Messaging Adapters**: Test event publishing and connection management

- **Infrastructure Tests** (`tests/unit/app/infra/`)
  - **Manager Tests**: Test external service interactions (RabbitMQ, JWT)
  - **Repository Tests**: Test database operations and data persistence

#### Architecture Tests (`tests/unit/`)

- **Architecture Rules** (`test_architecture_rules.py`)
  - Validates hexagonal architecture principles
  - Ensures proper dependency directions
  - Prevents architectural violations

- **Adapters Architecture** (`test_adapters_architecture.py`)
  - Tests adapter layer compliance
  - Validates protocol-based design

### 2. Integration Tests (`tests/integration/`)

- End-to-end testing of complete workflows
- Database integration testing
- External service integration testing

## Testing Patterns

### 1. Test Naming Convention

- Test files: `test_*.py`
- Test classes: `TestClassName`
- Test methods: `test_method_name_scenario`

### 2. Fixture Usage

```python
@pytest.fixture
def mock_service(self, mocker):
    return mocker.Mock()

@pytest.fixture
def service_instance(self, mock_service):
    return ServiceClass(mock_service)
```

### 3. Async Testing

```python
@pytest.mark.asyncio
async def test_async_method(self, service_instance):
    result = await service_instance.async_method()
    assert result is not None
```

### 4. Mocking Strategy

- Use `mocker.Mock()` for simple mocks
- Use `mocker.AsyncMock()` for async methods
- Mock external dependencies at protocol boundaries
- Test behavior, not implementation details

## Coverage Goals

### Current Coverage Status

- ✅ **auth_service.py**: 97%
- ✅ **user_handler.py**: 90%+
- ✅ **user_repository.py**: 90%+
- ✅ **dependencies_container.py**: 90%+
- ✅ **adapters**: 90%+

### Coverage Areas

1. **Happy Path Testing**: Normal operation scenarios
2. **Error Handling**: Exception cases and error responses
3. **Edge Cases**: Boundary conditions and unusual inputs
4. **Integration Points**: Protocol boundaries and external services

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/app/test_dependencies_container.py

# With coverage
pytest --cov=src tests/
```

### Test Configuration

- Configuration in `pyproject.toml`
- Coverage settings in `[tool.coverage]` section
- Test markers for different test types

## Architecture Compliance

### Test Rules

1. **Domain Tests**: Never import from infra or adapters
2. **Adapter Tests**: Mock infra dependencies, test domain interactions
3. **Infrastructure Tests**: Test external service interactions directly
4. **Integration Tests**: Test complete workflows with real dependencies

### Protocol Testing

- Test adapters using protocol mocks
- Verify interface compliance
- Test data transformation between layers

## Best Practices

1. **Isolation**: Each test should be independent
2. **Deterministic**: Tests should produce consistent results
3. **Fast**: Unit tests should run quickly
4. **Clear**: Test names should describe what is being tested
5. **Comprehensive**: Cover success, failure, and edge cases

## Continuous Integration

- Tests run on every push/PR
- Coverage requirements enforced
- Architecture rules validated
- Performance tests for critical paths
