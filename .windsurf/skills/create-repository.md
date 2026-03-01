---
description: Create a repository with database operations and manager
---

# Skill: Create Repository

## Overview
Creates a complete repository pattern with database models, manager classes, and proper separation between infrastructure and adapters.

## Prerequisites
- Read `/rules/architecture.yml` for structure guidelines
- Read `/contexts/architecture-context.md` for repository patterns
- Identify database type and entity structure

## Steps

### 1. Create Database Model
**Location**: `src/app/infra/database/models/<entity>_model.py`
```python
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from infra.database.base import Base
import uuid
from datetime import datetime

class <Entity>Model(Base):
    __tablename__ = "<table_name>"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field1 = Column(String(255), nullable=False)
    field2 = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
```

### 2. Create Repository Manager
**Location**: `src/app/infra/database/managers/<entity>_manager.py`
```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from infra.database.models.<entity>_model import <Entity>Model
from domain.entities.<entity> import <Entity>Entity

class <Entity>Manager:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, entity_data: dict) -> <Entity>Model:
        db_entity = <Entity>Model(**entity_data)
        self.session.add(db_entity)
        await self.session.commit()
        await self.session.refresh(db_entity)
        return db_entity
    
    async def get_by_id(self, entity_id: str) -> Optional[<Entity>Model]:
        result = await self.session.execute(
            select(<Entity>Model).where(<Entity>Model.id == entity_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_field(self, field_name: str, value: str) -> Optional[<Entity>Model]:
        result = await self.session.execute(
            select(<Entity>Model).where(getattr(<Entity>Model, field_name) == value)
        )
        return result.scalar_one_or_none()
    
    async def update(self, entity_id: str, update_data: dict) -> Optional[<Entity>Model]:
        await self.session.execute(
            update(<Entity>Model).where(<Entity>Model.id == entity_id).values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_id(entity_id)
    
    async def delete(self, entity_id: str) -> bool:
        result = await self.session.execute(
            delete(<Entity>Model).where(<Entity>Model.id == entity_id)
        )
        await self.session.commit()
        return result.rowcount > 0
```

### 3. Create Repository Port
**Location**: `src/app/domain/ports/<entity>_repository_port.py`
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output

class <Entity>RepositoryPort(ABC):
    @abstractmethod
    async def create(self, input_data: <Action><Entity>Input) -> <Action><Entity>Output:
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[<Entity>Entity]:
        pass
    
    @abstractmethod
    async def get_by_field(self, field_name: str, value: str) -> Optional[<Entity>Entity]:
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, update_data: dict) -> Optional[<Entity>Entity]:
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        pass
```

### 4. Create Repository Adapter
**Location**: `src/app/adapters/database/<entity>_repository_adapter.py`
```python
from typing import Optional
from domain.ports.<entity>_repository_port import <Entity>RepositoryPort
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output
from infra.database.managers.<entity>_manager import <Entity>Manager

class <Entity>RepositoryAdapter(<Entity>RepositoryPort):
    def __init__(self, manager: <Entity>Manager):
        self.manager = manager
    
    async def create(self, input_data: <Action><Entity>Input) -> <Action><Entity>Output:
        entity_dict = input_data.__dict__
        db_entity = await self.manager.create(entity_dict)
        entity = self._model_to_entity(db_entity)
        return <Action><Entity>Output(entity=entity, success=True)
    
    async def get_by_id(self, entity_id: str) -> Optional[<Entity>Entity]:
        db_entity = await self.manager.get_by_id(entity_id)
        return self._model_to_entity(db_entity) if db_entity else None
    
    async def get_by_field(self, field_name: str, value: str) -> Optional[<Entity>Entity]:
        db_entity = await self.manager.get_by_field(field_name, value)
        return self._model_to_entity(db_entity) if db_entity else None
    
    async def update(self, entity_id: str, update_data: dict) -> Optional[<Entity>Entity]:
        db_entity = await self.manager.update(entity_id, update_data)
        return self._model_to_entity(db_entity) if db_entity else None
    
    async def delete(self, entity_id: str) -> bool:
        return await self.manager.delete(entity_id)
    
    def _model_to_entity(self, db_entity) -> <Entity>Entity:
        return <Entity>Entity(
            id=str(db_entity.id),
            field1=db_entity.field1,
            field2=db_entity.field2,
            created_at=db_entity.created_at,
            updated_at=db_entity.updated_at,
            is_active=db_entity.is_active
        )
```

### 5. Add to Dependencies Container
**Location**: `src/app/dependencies_container.py`
```python
from adapters.database.<entity>_repository_adapter import <Entity>RepositoryAdapter
from infra.database.managers.<entity>_manager import <Entity>Manager

class DependenciesContainer:
    def __init__(self):
        # Existing dependencies...
        self.<entity>_manager = <Entity>Manager(self.session)
        self.<entity>_repository = <Entity>RepositoryAdapter(self.<entity>_manager)
```

### 6. Create Unit Tests
**Location**: `tests/app/adapters/database/test_<entity>_repository_adapter.py`
```python
import pytest
from unittest.mock import AsyncMock, Mock
from adapters.database.<entity>_repository_adapter import <Entity>RepositoryAdapter

@pytest.mark.asyncio
async def test_create():
    mock_manager = AsyncMock()
    adapter = <Entity>RepositoryAdapter(mock_manager)
    input_data = <Action><Entity>Input(field1="test")
    
    result = await adapter.create(input_data)
    
    assert result.success is True
    mock_manager.create.assert_called_once()
```

### 7. Create Integration Tests
**Location**: `tests/integration/database/test_<entity>_repository_integration.py`
```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from infra.database.managers.<entity>_manager import <Entity>Manager
from adapters.database.<entity>_repository_adapter import <Entity>RepositoryAdapter

@pytest.mark.asyncio
async def test_repository_integration(test_session: AsyncSession):
    manager = <Entity>Manager(test_session)
    adapter = <Entity>RepositoryAdapter(manager)
    
    input_data = <Action><Entity>Input(field1="test")
    result = await adapter.create(input_data)
    
    assert result.success is True
    assert result.entity.field1 == "test"
```

## Validation
- [ ] Database model follows SQLAlchemy patterns
- [ ] Manager handles database operations only
- [ ] Repository port defines interface
- [ ] Repository adapter implements port
- [ ] Model to entity mapping correct
- [ ] Dependency injection configured
- [ ] Tests cover all CRUD operations
- [ ] No business logic in repository
