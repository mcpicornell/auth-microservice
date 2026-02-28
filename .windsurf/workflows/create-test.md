---
description: Create comprehensive tests based on architecture context
---

# Test Creation Workflow

## Context Loading

1. Read `.windsurf/architecture-rules.yml` for project structure
2. Apply hexagonal architecture testing principles
3. Follow dependency injection testing patterns
4. Use async testing with pytest-asyncio
5. Mock external dependencies appropriately
6. No comments or docstrings in tests
7. Follow existing test patterns in `tests/`

## Test Structure Rules

### Test Organization
```
tests/
├── unit/                     # Unit tests (mirrors src/app structure)
│   ├── app/                 # App structure mirror
│   │   ├── domain/          # Domain layer tests
│   │   ├── adapters/        # Adapter tests
│   │   ├── infra/           # Infrastructure tests
│   │   ├── settings/        # Settings tests
│   │   └── test_dependencies_container.py  # Container tests
│   ├── test_adapters_architecture.py  # Architecture validation
│   ├── test_architecture_rules.py      # Rules compliance
│   ├── test_basic_structure.py         # Basic structure tests
│   ├── test_integration.py             # Integration setup
│   └── test_main.py                    # Main app tests
├── integration/              # Integration tests
│   ├── api/                 # API endpoint tests
│   ├── database/            # Database tests
│   └── messaging/           # Message queue tests
└── e2e/                     # End-to-end tests
    └── api/                 # Full API flow tests
```

### Testing Patterns

#### Domain Tests
- Test business logic in isolation
- Use pure dataclasses
- No external dependencies
- Focus on edge cases and validation

#### Adapter Tests
- Mock external dependencies
- Test port implementations
- Verify integration behavior
- Use AsyncMock for async methods

#### Service Tests
- Mock all ports
- Test business logic coordination
- Verify event publishing
- Test error handling

#### API Tests
- Use TestClient for FastAPI
- Test all endpoints
- Verify status codes
- Test response models

## Test Generation Guidelines

### For Domain Entities
```python
def test_entity_creation():
    entity = EntityClass(valid_data)
    assert entity.field == expected_value

def test_entity_validation():
    with pytest.raises(ValueError):
        EntityClass(invalid_data)
```

### For Services
```python
@pytest.mark.asyncio
async def test_service_method():
    mock_repo = Mock(spec=RepositoryPort)
    service = ServiceClass(mock_repo, mock_other)
    result = await service.method(input_data)
    assert result == expected_output
    mock_repo.method.assert_called_once()
```

### For Adapters
```python
@pytest.mark.asyncio
async def test_adapter_method():
    mock_session = AsyncMock()
    adapter = AdapterClass(session_factory)
    result = await adapter.method(input_data)
    assert result == expected_output
```

### For API Handlers
```python
def test_endpoint():
    mock_service = Mock()
    handler = HandlerClass(mock_service)
    client = TestClient(app)
    response = client.post("/endpoint", json=test_data)
    assert response.status_code == 200
    assert response.json() == expected_response
```

## Mock Strategy

### Domain Ports
- Use `Mock(spec=PortInterface)`
- Configure return values
- Verify method calls

### External Dependencies
- Database: Use `AsyncMock` for sessions
- HTTP: Use `TestClient` or `AsyncMock`
- Message Queue: Mock publisher methods

### Configuration
- Use test settings
- Override environment variables
- Mock external services

## Test Data Management

### Fixtures
```python
@pytest.fixture
def sample_user_data():
    return CreateUserInput(
        email="test@example.com",
        username="testuser",
        password="password123"
    )
```

### Factories
```python
def create_user_entity(**overrides):
    defaults = {
        "id": uuid4(),
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "hashed"
    }
    defaults.update(overrides)
    return UserEntity(**defaults)
```

## Coverage Requirements

### Minimum Coverage
- Domain: 95%
- Services: 90%
- Adapters: 85%
- API: 80%

### Critical Paths
- User registration flow
- Authentication flow
- Token validation
- Error handling

## Test Execution

### Running Tests
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# All tests with coverage
pytest tests/ --cov=src/app --cov-report=html

# Specific test file
pytest tests/unit/app/domain/test_user_service.py -v

# Tests from app structure mirror
pytest tests/unit/app/ -v
```

### Test Categories
```bash
# Fast tests only
pytest tests/ -m "not slow"

# Slow tests (integration, e2e)
pytest tests/ -m "slow"
```

## Implementation Steps

1. **Analyze Target Files**: Examine the files to test in `src/app/`
2. **Identify Test Types**: Unit, integration, or API tests
3. **Create Test Structure**: Organize files in `tests/unit/app/` mirroring `src/app/`
4. **Generate Test Cases**: Cover all methods and edge cases
5. **Add Mocks**: Configure dependencies correctly
6. **Verify Coverage**: Ensure adequate test coverage
7. **Run Tests**: Confirm all tests pass

## File Input Processing

### Single File Testing
- Analyze class/method structure from `src/app/`
- Generate corresponding test file in `tests/unit/app/` maintaining same path structure
- Example: `src/app/domain/user.py` → `tests/unit/app/domain/test_user.py`

### Multiple Files Testing
- Group by layer (domain, adapters, infra)
- Create comprehensive test suites in respective directories
- Test interactions between components

### Directory Testing
- Recursively analyze all Python files in `src/app/`
- Generate test files for each component maintaining directory structure
- Create integration tests for interactions in `tests/integration/`

## Quality Assurance

### Test Quality Checks
- No comments or docstrings
- Proper async/await usage
- Correct mock configurations
- Clear assertion messages
- Appropriate test data

### Code Style
- Follow existing test patterns
- Use descriptive test names
- Keep tests focused and small
- Avoid test duplication
