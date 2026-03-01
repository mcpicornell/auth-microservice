# Project Context

## Project Information
- **Name**: auth-microservice
- **Type**: Authentication Microservice
- **Architecture**: Hexagonal (Ports & Adapters)
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Messaging**: RabbitMQ
- **Authentication**: JWT

## Business Domain
Authentication and authorization microservice providing:
- User registration and management
- Authentication (login/logout)
- JWT token management
- Password security
- Event publishing for user actions

## Core Features
1. **User Management**
   - User registration with email validation
   - User profile management
   - Password reset functionality
   - Account activation/deactivation

2. **Authentication**
   - Login with email/password
   - JWT token generation and validation
   - Token refresh mechanism
   - Logout functionality

3. **Security**
   - Password hashing with bcrypt
   - JWT token security
   - Rate limiting for authentication
   - Account lockout mechanisms

4. **Events**
   - User registration events
   - Login/logout events
   - Password change events
   - Account status changes

## Technical Stack

### Core Dependencies
- **FastAPI**: Web framework for API
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **RabbitMQ**: Message queue for events
- **Pydantic**: Data validation (replaced by dataclasses)
- **bcrypt**: Password hashing
- **PyJWT**: JWT token handling

### Development Tools
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **pytest-mock**: Mocking support
- **black**: Code formatting
- **mypy**: Type checking

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Local development
- **PostgreSQL**: Database
- **RabbitMQ**: Message broker

## Current Implementation Status

### Completed Components
- ✅ Hexagonal architecture structure
- ✅ Domain entities with dataclasses
- ✅ Repository pattern implementation
- ✅ JWT security adapter
- ✅ Password security adapter
- ✅ RabbitMQ messaging adapter
- ✅ FastAPI handlers with routers
- ✅ Dependency injection container
- ✅ Comprehensive test suite

### Domain Layer
- **UserEntity**: Core user data structure
- **TokenEntity**: JWT token representation
- **AuthService**: Authentication business logic
- **UserService**: User management business logic
- **Ports**: Repository, security, and messaging interfaces

### Adapter Layer
- **UserRepositoryAdapter**: Database operations for users
- **JWTAdapter**: JWT token generation and validation
- **PasswordAdapter**: Password hashing and verification
- **RabbitMQAdapter**: Event publishing and handling

### Infrastructure Layer
- **UserHandler**: User management API endpoints
- **AuthHandler**: Authentication API endpoints
- **Database Models**: SQLAlchemy models for persistence
- **Database Managers**: Low-level database operations

## API Endpoints

### User Management
- `POST /users/` - Create new user
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/verify` - Verify JWT token

### Health Check
- `GET /health` - Application health status

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Sessions Table (for token management)
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    token_jti VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Event System

### Event Types
- **user_created**: New user registration
- **user_updated**: User profile updated
- **user_deleted**: User account deleted
- **user_login**: Successful user login
- **user_logout**: User logout
- **password_changed**: Password updated

### Event Format
```json
{
    "type": "user_created",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": {
        "user_id": "uuid",
        "email": "user@example.com",
        "username": "username"
    }
}
```

## Configuration

### Environment Variables
```bash
# Database Configuration
DB_SQL_HOST=localhost
DB_SQL_PORT=5432
DB_SQL_NAME=auth_microservice
DB_SQL_USER=auth_user
DB_SQL_PASSWORD=secure_password

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/

# Application Configuration
APP_NAME=auth-microservice
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO
```

## Development Workflow

### Local Development
1. Start services with Docker Compose
2. Run application locally
3. Use pytest for testing
4. Follow architecture rules strictly

### Testing Strategy
- Unit tests for each component
- Integration tests for API endpoints
- Database tests with test containers
- Performance tests for critical paths

### Code Quality
- No comments or docstrings (as per architecture rules)
- English-only documentation
- Type hints required
- Dataclasses instead of dictionaries
- Async-first approach

## Deployment Considerations

### Scalability
- Stateless application design
- Database connection pooling
- Message queue for async processing
- Horizontal scaling support

### Security
- Environment-based configuration
- No plain text credentials
- JWT token security
- Password hashing best practices

### Monitoring
- Health check endpoints
- Structured logging
- Performance metrics
- Error tracking

## Future Enhancements

### Planned Features
- Multi-factor authentication
- Social login integration
- Role-based access control
- Audit logging
- Rate limiting
- Account recovery

### Technical Improvements
- Caching layer
- Database read replicas
- Event sourcing
- API versioning
- GraphQL support
- OpenTelemetry integration

## Integration Points

### External Services
- Email service for verification
- SMS service for 2FA
- Analytics service for user behavior
- Audit service for compliance

### Internal Services
- User profile service
- Notification service
- Analytics service
- Audit service

## Performance Requirements

### Response Times
- Authentication: < 200ms
- User operations: < 500ms
- Health checks: < 50ms

### Throughput
- Concurrent users: 1000+
- Requests per second: 500+
- Database connections: 100 max

### Availability
- Uptime: 99.9%
- Error rate: < 0.1%
- Response time P95: < 1s
