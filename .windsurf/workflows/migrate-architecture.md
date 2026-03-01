---
description: Migrate existing code to new architecture patterns
---

# Flow: Architecture Migration

## Overview
Systematic migration of existing code to follow hexagonal architecture patterns with proper separation of concerns and dependency injection.

## Prerequisites
- Read `/rules/architecture.yml` for target architecture
- Read `/contexts/architecture-context.md` for patterns
- Existing codebase analysis completed
- Migration plan defined

## Tasks

### Task 1: Analysis and Planning
**Timeline**: 60 minutes
**Files**:
- Create migration plan document
- Analyze existing code structure
- Identify migration priorities

**Steps**:
1. Map existing components to new architecture
2. Identify circular dependencies
3. Plan migration order (domain → adapters → infra)
4. Define rollback strategy

### Task 2: Domain Layer Migration
**Timeline**: 120 minutes
**Files**:
- Migrate entities to dataclasses
- Create domain services
- Define ports for external dependencies

**Steps**:
1. Convert existing models to domain entities
2. Extract business logic into services
3. Create port interfaces
4. Remove external dependencies from domain

### Task 3: Adapter Layer Creation
**Timeline**: 90 minutes
**Files**:
- Create repository adapters
- Implement security adapters
- Create messaging adapters

**Steps**:
1. Implement database adapters
2. Create security adapters for auth
3. Implement messaging for events
4. Add proper error handling

### Task 4: Infrastructure Refactoring
**Timeline**: 90 minutes
**Files**:
- Refactor API handlers
- Update database configurations
- Migrate settings and configuration

**Steps**:
1. Create new API handlers with routers
2. Update database connections
3. Migrate configuration to settings
4. Remove old infrastructure code

### Task 5: Dependency Injection Setup
**Timeline**: 60 minutes
**Files**:
- Create dependencies container
- Wire all dependencies
- Update main application

**Steps**:
1. Create comprehensive dependency container
2. Wire all adapters and services
3. Update application entry point
4. Test dependency resolution

### Task 6: Testing Migration
**Timeline**: 120 minutes
**Files**:
- Migrate existing tests
- Create new test structure
- Add integration tests

**Steps**:
1. Update test structure to mirror new architecture
2. Migrate existing test logic
3. Add tests for new components
4. Create integration test suite

### Task 7: Validation and Cleanup
**Timeline**: 60 minutes
**Files**:
- Remove old code
- Update documentation
- Performance validation

**Steps**:
1. Remove deprecated code
2. Update API documentation
3. Validate performance
4. Security review

## Migration Strategy

### Phase 1: Domain First
1. **Identify Business Logic**
   - Extract pure business rules
   - Identify entities and value objects
   - Map business processes

2. **Create Domain Entities**
   - Convert existing models to dataclasses
   - Remove framework dependencies
   - Add proper validation

3. **Implement Domain Services**
   - Extract business logic from controllers
   - Create service interfaces
   - Implement business rules

### Phase 2: Adapter Implementation
1. **Database Adapters**
   - Create repository patterns
   - Implement port interfaces
   - Handle data transformation

2. **Security Adapters**
   - Implement JWT handling
   - Password hashing
   - Authentication flows

3. **Messaging Adapters**
   - Event publishing
   - Message handling
   - Queue management

### Phase 3: Infrastructure Migration
1. **API Handlers**
   - Create FastAPI routers
   - Implement request handling
   - Add proper error responses

2. **Configuration**
   - Environment variables
   - Settings management
   - Security configuration

## Example Migration

### Before: Old Structure
```python
# old_models.py
from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

# old_controller.py
from fastapi import FastAPI, Depends
from database import get_db
from old_models import User

app = FastAPI()

@app.post("/users")
async def create_user(user_data: dict, db=Depends(get_db)):
    user = User(email=user_data["email"], password=user_data["password"])
    db.add(user)
    db.commit()
    return {"id": user.id}
```

### After: New Architecture

#### Domain Layer
```python
# domain/entities/user.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class UserEntity:
    id: UUID
    email: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True

@dataclass
class CreateUserInput:
    email: str
    password: str

@dataclass
class CreateUserOutput:
    user: UserEntity
    success: bool
    message: str = None

# domain/ports/user_repository_port.py
from abc import ABC, abstractmethod
from domain.entities.user import UserEntity, CreateUserInput, CreateUserOutput

class UserRepositoryPort(ABC):
    @abstractmethod
    async def create(self, input_data: CreateUserInput) -> CreateUserOutput:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity:
        pass

# domain/services/user_service.py
from domain.ports.user_repository_port import UserRepositoryPort
from domain.ports.security_port import SecurityPort

class UserService:
    def __init__(self, repository: UserRepositoryPort, security: SecurityPort):
        self.repository = repository
        self.security = security
    
    async def create_user(self, input_data: CreateUserInput) -> CreateUserOutput:
        existing = await self.repository.get_by_email(input_data.email)
        if existing:
            return CreateUserOutput(
                user=None,
                success=False,
                message="User already exists"
            )
        
        hashed_password = await self.security.hash_password(input_data.password)
        user_input = CreateUserInput(
            email=input_data.email,
            password=hashed_password
        )
        
        return await self.repository.create(user_input)
```

#### Adapter Layer
```python
# adapters/database/user_repository_adapter.py
from domain.ports.user_repository_port import UserRepositoryPort
from domain.entities.user import UserEntity, CreateUserInput, CreateUserOutput
from infra.database.managers.user_manager import UserManager

class UserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, manager: UserManager):
        self.manager = manager
    
    async def create(self, input_data: CreateUserInput) -> CreateUserOutput:
        user_data = {
            "email": input_data.email,
            "hashed_password": input_data.password
        }
        db_user = await self.manager.create(user_data)
        entity = self._model_to_entity(db_user)
        
        return CreateUserOutput(
            user=entity,
            success=True
        )
    
    async def get_by_email(self, email: str) -> UserEntity:
        db_user = await self.manager.get_by_email(email)
        return self._model_to_entity(db_user) if db_user else None
```

#### Infrastructure Layer
```python
# infra/api/handlers/user_handler.py
from fastapi import APIRouter, Depends
from domain.services.user_service import UserService
from domain.entities.user import CreateUserInput, CreateUserOutput

class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.post("/", response_model=CreateUserOutput, status_code=201)
        async def create_user(input_data: CreateUserInput):
            return await self.user_service.create_user(input_data)

# dependencies_container.py
class DependenciesContainer:
    def __init__(self):
        self.session = create_async_session()
        self.user_manager = UserManager(self.session)
        self.security_adapter = SecurityAdapter()
        self.user_repository = UserRepositoryAdapter(self.user_manager)
        self.user_service = UserService(self.user_repository, self.security_adapter)
        self.user_handler = UserHandler(self.user_service)
```

## Migration Checklist

### Pre-Migration
- [ ] Existing code analyzed
- [ ] Migration plan created
- [ ] Backup strategy defined
- [ ] Test environment prepared

### Domain Migration
- [ ] All entities converted to dataclasses
- [ ] Business logic extracted to services
- [ ] Port interfaces defined
- [ ] Domain layer isolated

### Adapter Migration
- [ ] Repository adapters implemented
- [ ] Security adapters created
- [ ] Messaging adapters added
- [ ] External dependencies handled

### Infrastructure Migration
- [ ] API handlers created with routers
- [ ] Database configuration updated
- [ ] Settings management implemented
- [ ] Old infrastructure removed

### Testing Migration
- [ ] Test structure updated
- [ ] All tests migrated
- [ ] Integration tests added
- [ ] Coverage maintained

### Post-Migration
- [ ] Old code removed
- [ ] Documentation updated
- [ ] Performance validated
- [ ] Security reviewed

## Validation Commands

```bash
# Test new architecture
python -c "from src.app.dependencies_container import DependenciesContainer; print('Container OK')"

# Run migrated tests
pytest tests/unit/app/ -v

# Run integration tests
pytest tests/integration/ -v

# Check architecture compliance
python -c "
import src.app.domain.entities
import src.app.domain.services
import src.app.adapters.database
import src.app.infra.api
print('Architecture layers OK')
"

# Performance comparison
python -m pytest tests/performance/ -v
```

## Rollback Strategy
1. **Git Branches**: Maintain separate branches for each migration phase
2. **Feature Flags**: Use flags to switch between old and new implementations
3. **Database Backups**: Keep database backups before schema changes
4. **Incremental Deployment**: Deploy changes incrementally with monitoring

## Success Criteria
- [ ] All functionality preserved
- [ ] Architecture rules followed
- [ ] Tests passing with adequate coverage
- [ ] Performance maintained or improved
- [ ] Security requirements met
- [ ] Documentation complete and accurate
