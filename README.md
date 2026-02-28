# Auth Microservice

Authentication microservice with hexagonal architecture.

## Architecture

This project follows hexagonal architecture (ports & adapters pattern):

```
src/app/
├── domain/          # Business logic and entities
├── adapters/        # External integrations (database, messaging, etc.)
├── infra/           # Infrastructure components (API handlers)
├── settings/        # Configuration management
└── dependencies_container.py  # Dependency injection
```

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- RabbitMQ 3.12+
- Docker & Docker Compose

## Setup

### 1. Install Dependencies

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 2. Start External Services

Start PostgreSQL and RabbitMQ separately:

```bash
# Start PostgreSQL
docker run -d \
  --name auth-postgres \
  -e POSTGRES_DB=auth_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15-alpine

# Start RabbitMQ
docker run -d \
  --name auth-rabbitmq \
  -e RABBITMQ_DEFAULT_USER=guest \
  -e RABBITMQ_DEFAULT_PASS=guest \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3.12-management-alpine
```

### 3. Configure Environment

Copy and configure environment variables:

```bash
cp .env.pro.example .env.pro
# Edit .env.pro with your configuration
```

### 4. Run Application

```bash
# Development mode
uv run python src/main.py

# Or with Docker Compose
docker-compose up
```

## API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests:

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/app --cov-report=html
```

## Development

### Adding New Components

Use the available workflows:

- `/create-adapter` - Create new adapters with input/output dataclasses
- `/create-handler` - Create new API handlers with self-contained router

### Code Style

- No comments in the code
- All documentation in English only
- Use dataclasses for all data transfer
- Follow hexagonal architecture principles

## Environment Variables

Key environment variables (see `.env.pro`):

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

## Docker Deployment

Build and run with Docker:

```bash
# Build image
docker build -t auth-service .

# Run container
docker run -d \
  --name auth-service \
  --env-file .env.pro \
  -p 8000:8000 \
  auth-service
```

## Health Check

```bash
curl http://localhost:8000/health
```

## License

Private project.
