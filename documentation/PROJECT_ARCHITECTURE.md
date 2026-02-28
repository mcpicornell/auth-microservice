# Auth Microservice - Complete Architecture Documentation

## Project Overview

Hexagonal architecture authentication microservice with clean separation of concerns, dependency injection, and async-first design.

## Architecture Principles

### Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Domain Layer  │◄──►│  Adapter Layer │◄──►│ Infra Layer     │
│                 │    │                 │    │                 │
│ • Entities      │    │ • Database      │    │ • Models        │
│ • Ports         │    │ • Security      │    │ • API Handlers  │
│ • Services      │    │ • Messaging     │    │ • Framework     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
    Settings ◄──────────────────┼──────────────────► External
    (Config)               (Dependencies)         (Services)
```

## Directory Structure

```
src/app/
├── domain/                    # Core business logic
│   ├── entities/             # Dataclasses
│   │   ├── user.py          # User entities
│   │   └── token.py         # Token entities
│   ├── ports/               # Abstract interfaces
│   │   ├── user_repository_port.py
│   │   ├── token_provider_port.py
│   │   └── event_publisher_port.py
│   └── services/            # Business logic
│       └── auth_service.py
├── adapters/                # External integrations
│   ├── database/            # Repository implementations
│   │   └── user_adapter.py
│   ├── security/           # JWT, Password
│   │   ├── jwt_adapter.py
│   │   └── password_adapter.py
│   └── messaging/          # RabbitMQ
│       └── rabbitmq_adapter.py
├── infra/                   # Infrastructure
│   ├── database/           # Database models
│   │   └── models.py
│   └── api/                # API layer
│       └── handlers/
│           ├── auth_handler.py
│           └── user_handler.py
├── settings/                # Configuration
│   ├── app_settings.py
│   └── __init__.py
└── dependencies_container.py # Dependency injection
```

## Implementation Details

### Domain Layer

**Entities**: Pure dataclasses with business logic
```python
@dataclass
class UserEntity:
    id: UUID
    email: str
    username: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False
```

**Ports**: Abstract interfaces for external dependencies
```python
class UserRepositoryPort(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass
```

**Services**: Core business logic implementation
```python
class AuthService:
    def __init__(self, user_repository, token_provider, event_publisher):
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.event_publisher = event_publisher
```

### Adapter Layer

**Database Adapter**: Implements repository port
```python
class UserAdapter(UserRepositoryPort):
    def __init__(self, session_factory):
        self.session_factory = session_factory
```

**Security Adapter**: JWT token management
```python
class JWTAdapter(TokenProviderPort):
    def __init__(self, settings):
        self.settings = settings
```

### Infrastructure Layer

**Database Models**: SQLAlchemy models
```python
class UserDB(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
```

**API Handlers**: FastAPI route handlers
```python
class AuthHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/auth")
```

## Configuration Management

### Settings Class
```python
class Settings(BaseSettings):
    DB_SQL_URL: str
    JWT_SECRET_KEY: str
    RABBITMQ_HOST: str = "localhost"
```

### Environment Variables (.env.pro)
```bash
DB_SQL_URL=postgresql://user:password@localhost:5432/auth_db
JWT_SECRET_KEY=your-secret-key
RABBITMQ_HOST=localhost
```

## Dependency Injection

### DependenciesContainer
```python
class DependenciesContainer:
    def __init__(self, settings):
        self.settings = settings
    
    async def initialize(self):
        await self._initialize_database()
        await self._initialize_adapters()
        await self._initialize_services()
        await self._initialize_handlers()
```

### Application Lifecycle
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    container = DependenciesContainer(settings)
    await container.initialize()
    app.state.container = container
    yield
    await container.close()
```

## API Endpoints

### Authentication Routes (/auth)
- POST /auth/register - User registration
- POST /auth/login - User login
- GET /auth/me - Current user profile

### User Routes (/users)
- GET /users/{user_id} - Get user by ID
- GET /users/email/{email} - Get user by email
- GET /users/ - List users (placeholder)
- DELETE /users/{user_id} - Delete user (placeholder)

### System Routes
- GET /health - Health check

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## External Dependencies

### Database
- PostgreSQL with asyncpg driver
- SQLAlchemy 2.0 with async support

### Message Queue
- RabbitMQ for event publishing
- Async connection handling

### Security
- JWT tokens with jose library
- bcrypt password hashing

## Development Workflow

### Adding New Components

1. **Create Adapter**: Use `/create-adapter` workflow
2. **Create Handler**: Use `/create-handler` workflow
3. **Add Tests**: Update test files
4. **Update Container**: Add to DependenciesContainer

### Testing Strategy

- Unit tests for domain logic
- Integration tests for API endpoints
- Mock external dependencies

## Deployment

### Docker Configuration
```yaml
services:
  auth-service:
    build: .
    env_file: .env.pro
    ports: ["8000:8000"]
```

### Environment Setup
1. PostgreSQL database
2. RabbitMQ message broker
3. Environment variables configuration

## Rules and Constraints

### Forbidden Patterns
- No comments or docstrings
- No plain text credentials
- No business logic in adapters
- No framework code in domain

### Required Patterns
- Dependency injection
- Async-first design
- Port-adapter pattern
- Dataclasses for entities

## Questions for Implementation

1. **Password Verification**: Should password verification be moved to a separate security service in the domain layer, or remain in the auth service?

2. **Event Publishing**: Should we implement event sourcing with actual database persistence for events, or keep the current RabbitMQ-only approach?

3. **User Roles**: Do you want to implement a more sophisticated role-based access control system beyond the simple is_admin flag?

4. **API Versioning**: Should we implement API versioning (v1, v2) in the routes, and if so, what's your preferred approach?

## Performance Considerations

- Database connection pooling
- Async I/O for all external calls
- Event publishing is fire-and-forget
- JWT tokens have configurable expiration

## Security Notes

- JWT secret key must be set in production
- Password hashing uses bcrypt
- All passwords are hashed before storage
- No sensitive data in logs
