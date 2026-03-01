---
description: Create complete API endpoint with handler, service, and tests
---

# Flow: Create API Endpoint

## Overview
Complete flow to create a new API endpoint from scratch including handler, service coordination, routing, and comprehensive testing.

## Prerequisites
- Read `/rules/architecture.yml` for API structure
- Read `/skills/create-handler.md` for handler patterns
- Read `/skills/create-service.md` for service patterns
- Read `/contexts/architecture-context.md` for implementation guidelines

## Tasks

### Task 1: Define API Contract
**Timeline**: 5 minutes
**Files**: 
- Create input/output dataclasses in `domain/entities/`
- Define endpoint contract and validation rules

**Steps**:
1. Create input dataclass with validation
2. Create output dataclass with response structure
3. Define HTTP status codes and error responses

### Task 2: Implement Business Logic
**Timeline**: 15 minutes
**Files**:
- Create/update service in `domain/services/`
- Implement business rules and validation
- Add port coordination if needed

**Steps**:
1. Add business method to existing service or create new
2. Implement input validation
3. Add business rule enforcement
4. Handle error scenarios

### Task 3: Create API Handler
**Timeline**: 10 minutes
**Files**:
- Create handler in `infra/api/handlers/`
- Set up FastAPI router and routes
- Implement request/response handling

**Steps**:
1. Create handler class with service dependency
2. Initialize router with proper prefix and tags
3. Implement endpoint method
4. Add error handling and status codes

### Task 4: Configure Dependencies
**Timeline**: 5 minutes
**Files**:
- Update `dependencies_container.py`
- Register new handler and dependencies
- Ensure proper injection

**Steps**:
1. Add handler to container
2. Wire up service dependencies
3. Configure router registration

### Task 5: Create Unit Tests
**Timeline**: 15 minutes
**Files**:
- Service tests in `tests/app/domain/services/`
- Handler tests in `tests/app/infra/api/handlers/`

**Steps**:
1. Test service business logic
2. Test handler request/response
3. Mock external dependencies
4. Cover error scenarios

### Task 6: Create Integration Tests
**Timeline**: 10 minutes
**Files**:
- API integration tests in `tests/integration/api/`
- End-to-end flow validation

**Steps**:
1. Test complete request flow
2. Validate database operations
3. Test error responses
4. Verify status codes and responses

### Task 7: Documentation and Validation
**Timeline**: 5 minutes
**Files**:
- Update API documentation
- Validate architecture compliance

**Steps**:
1. Ensure OpenAPI documentation is complete
2. Validate against architecture rules
3. Verify test coverage
4. Check security requirements

## Implementation Checklist

### Dataclasses
- [ ] Input dataclass with proper validation
- [ ] Output dataclass with response structure
- [ ] Proper typing and optional fields
- [ ] Validation rules implemented

### Service Layer
- [ ] Business logic implemented
- [ ] Port coordination correct
- [ ] Error handling comprehensive
- [ ] No external dependencies

### Handler Layer
- [ ] Router properly initialized
- [ ] Endpoint method implemented
- [ ] Request/response mapping correct
- [ ] Status codes appropriate

### Dependencies
- [ ] Container updated with new dependencies
- [ ] Proper injection configured
- [ ] No circular dependencies
- [ ] Lifecycle management correct

### Testing
- [ ] Unit tests for service layer
- [ ] Unit tests for handler layer
- [ ] Integration tests for API
- [ ] Error scenarios covered
- [ ] Mock configurations correct

### Architecture Compliance
- [ ] No business logic in handlers
- [ ] Proper layer separation
- [ ] Dataclass usage consistent
- [ ] Async patterns followed
- [ ] Security requirements met

## Example Implementation

### Step 1: Create Dataclasses
```python
# domain/entities/user.py
@dataclass
class CreateUserInput:
    email: str
    username: str
    password: str

@dataclass
class CreateUserOutput:
    user: UserEntity
    success: bool
    message: Optional[str] = None
```

### Step 2: Update Service
```python
# domain/services/user_service.py
async def create_user(self, input_data: CreateUserInput) -> CreateUserOutput:
    existing = await self.user_repository.get_by_email(input_data.email)
    if existing:
        return CreateUserOutput(
            user=None,
            success=False,
            message="User already exists"
        )
    
    hashed_password = await self.security_adapter.hash_password(input_data.password)
    user_input = CreateUserInput(
        email=input_data.email,
        username=input_data.username,
        password=hashed_password
    )
    
    return await self.user_repository.create(user_input)
```

### Step 3: Create Handler
```python
# infra/api/handlers/user_handler.py
class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.post("/", response_model=CreateUserOutput, status_code=201)
        async def create_user(input_data: CreateUserInput):
            return await self.user_service.create_user(input_data)
```

### Step 4: Update Container
```python
# dependencies_container.py
class DependenciesContainer:
    def __init__(self):
        # Existing dependencies...
        self.user_handler = UserHandler(self.user_service)
```

## Validation Commands

```bash
# Run unit tests
pytest tests/unit/app/domain/services/test_user_service.py -v

# Run handler tests
pytest tests/unit/app/infra/api/handlers/test_user_handler.py -v

# Run integration tests
pytest tests/integration/api/test_user_integration.py -v

# Check architecture compliance
python -c "from src.app.dependencies_container import DependenciesContainer; print('OK')"

# Run all tests
pytest tests/ --cov=src/app --cov-report=html
```

## Success Criteria
- [ ] All tests passing
- [ ] API endpoint functional
- [ ] Architecture rules followed
- [ ] Documentation complete
- [ ] Security requirements met
- [ ] Performance acceptable
