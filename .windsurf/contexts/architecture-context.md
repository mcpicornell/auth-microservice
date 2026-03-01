# Architecture Context

## Project Overview
**auth-microservice** is a hexagonal architecture-based authentication microservice implementing clean architecture principles with proper separation of concerns.

## Architecture Patterns

### Hexagonal (Ports & Adapters) Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        DOMAIN                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Entities  │  │   Services  │  │       Ports         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │   ADAPTERS  │
                    └──────┬──────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │     API     │  │   Database  │  │    Messaging        │  │
│  │  Handlers   │  │  Managers   │  │    Adapters         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### Domain Layer (Core Business Logic)
- **Entities**: Pure dataclasses representing business objects
- **Services**: Business logic coordination between ports
- **Ports**: Abstract interfaces for external dependencies
- **Rules**: No external dependencies, pure business logic only

#### Adapter Layer (External Integrations)
- **Database Adapters**: Implement repository ports
- **Security Adapters**: JWT, password hashing, authentication
- **Messaging Adapters**: Event publishing, message handling
- **Rules**: Implement ports, handle external dependencies, no business logic

#### Infrastructure Layer (Delivery Mechanisms)
- **API Handlers**: FastAPI routers with self-contained logic
- **Database Managers**: SQLAlchemy models and operations
- **Configuration**: Environment variables and settings
- **Rules**: Framework-specific code, no business logic

## Implementation Patterns

### Dataclass Pattern
All entities and I/O objects use dataclasses:
```python
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
    message: Optional[str] = None
```

### Port-Adapter Pattern
```python
# Domain Port
class UserRepositoryPort(ABC):
    @abstractmethod
    async def create(self, input_data: CreateUserInput) -> CreateUserOutput:
        pass

# Adapter Implementation
class UserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, manager: UserManager):
        self.manager = manager
    
    async def create(self, input_data: CreateUserInput) -> CreateUserOutput:
        # Implementation using manager
        pass
```

### Dependency Injection Pattern
```python
class DependenciesContainer:
    def __init__(self):
        self.session = create_async_session()
        self.user_manager = UserManager(self.session)
        self.user_repository = UserRepositoryAdapter(self.user_manager)
        self.user_service = UserService(self.user_repository, self.security_adapter)
        self.user_handler = UserHandler(self.user_service)
```

### Async-First Pattern
All I/O operations are async:
```python
async def create_user(self, input_data: CreateUserInput) -> CreateUserOutput:
    existing = await self.repository.get_by_email(input_data.email)
    if existing:
        return CreateUserOutput(user=None, success=False)
    
    result = await self.repository.create(input_data)
    return result
```

## File Organization

### Domain Layer Structure
```
src/app/domain/
├── entities/
│   ├── user.py
│   ├── auth.py
│   └── token.py
├── ports/
│   ├── user_repository_port.py
│   ├── token_provider_port.py
│   └── event_publisher_port.py
└── services/
    ├── user_service.py
    ├── auth_service.py
    └── token_service.py
```

### Adapter Layer Structure
```
src/app/adapters/
├── database/
│   ├── user_repository_adapter.py
│   └── auth_repository_adapter.py
├── security/
│   ├── jwt_adapter.py
│   └── password_adapter.py
└── messaging/
    └── rabbitmq_adapter.py
```

### Infrastructure Layer Structure
```
src/app/infra/
├── api/
│   └── handlers/
│       ├── user_handler.py
│       └── auth_handler.py
├── database/
│   ├── models/
│   │   ├── user_model.py
│   │   └── auth_model.py
│   └── managers/
│       ├── user_manager.py
│       └── auth_manager.py
└── messaging/
    └── rabbitmq_manager.py
```

## Testing Strategy

### Test Structure Mirrors Source
```
tests/
├── unit/app/
│   ├── domain/
│   │   ├── entities/
│   │   ├── services/
│   │   └── test_ports.py
│   ├── adapters/
│   │   ├── database/
│   │   ├── security/
│   │   └── messaging/
│   └── infra/
│       └── api/handlers/
├── integration/
│   ├── api/
│   ├── database/
│   └── messaging/
└── e2e/
    └── api/
```

### Testing Patterns
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user flows
- **Mock Strategy**: Mock external dependencies, test internal logic

## Configuration Management

### Environment Variables
```python
# Database
DB_SQL_HOST=localhost
DB_SQL_PORT=5432
DB_SQL_NAME=auth_db
DB_SQL_USER=auth_user
DB_SQL_PASSWORD=secure_password

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

### Settings Pattern
```python
@dataclass
class DatabaseSettings:
    host: str
    port: int
    name: str
    user: str
    password: str

@dataclass
class AppSettings:
    database: DatabaseSettings
    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_minutes: int
```

## Security Patterns

### Password Security
- Use bcrypt for password hashing
- Never store plain text passwords
- Validate password strength

### JWT Security
- Use strong secret keys
- Set appropriate expiration times
- Validate tokens on each request

### Data Security
- No plain text credentials in code
- Use environment variables for secrets
- Implement proper access controls

## Error Handling Patterns

### Domain Layer Errors
```python
async def create_user(self, input_data: CreateUserInput) -> CreateUserOutput:
    if not self.validate_input(input_data):
        return CreateUserOutput(
            user=None,
            success=False,
            message="Invalid input data"
        )
    
    try:
        result = await self.repository.create(input_data)
        return result
    except Exception as e:
        return CreateUserOutput(
            user=None,
            success=False,
            message=f"Internal error: {str(e)}"
        )
```

### Infrastructure Layer Errors
```python
@self.router.post("/", response_model=CreateUserOutput)
async def create_user(input_data: CreateUserInput):
    try:
        return await self.user_service.create_user(input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Performance Patterns

### Database Optimization
- Use async database operations
- Implement proper connection pooling
- Use database indexes appropriately

### Caching Strategy
- Cache frequently accessed data
- Use appropriate cache invalidation
- Consider distributed caching for scale

### Async Patterns
- Use async/await for all I/O operations
- Implement proper concurrency control
- Use connection pooling for external services

## Monitoring and Observability

### Logging Strategy
- Use structured logging
- Include correlation IDs
- Log important business events

### Metrics Collection
- Track business metrics
- Monitor performance indicators
- Alert on error thresholds

### Health Checks
- Implement health check endpoints
- Monitor database connectivity
- Check external service availability
