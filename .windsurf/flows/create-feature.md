---
description: Create complete feature with all layers and comprehensive testing
---

# Flow: Create Complete Feature

## Overview
End-to-end flow to create a complete feature including domain entities, services, adapters, infrastructure, and full testing suite.

## Prerequisites
- Read `/rules/architecture.yml` for complete architecture rules
- Read all relevant skills in `/skills/`
- Read `/contexts/architecture-context.md` for patterns
- Feature requirements clearly defined

## Tasks

### Task 1: Domain Layer Design
**Timeline**: 30 minutes
**Files**:
- Domain entities in `domain/entities/`
- Domain ports in `domain/ports/`
- Domain services in `domain/services/`

**Steps**:
1. Create entity dataclasses with proper typing
2. Define input/output dataclasses for operations
3. Create port interfaces for external dependencies
4. Implement business logic services
5. Add validation and business rules

### Task 2: Adapter Layer Implementation
**Timeline**: 45 minutes
**Files**:
- Database adapters in `adapters/database/`
- Security adapters in `adapters/security/`
- Messaging adapters in `adapters/messaging/`

**Steps**:
1. Create database models and managers
2. Implement repository adapters
3. Create security adapters if needed
4. Implement messaging adapters for events
5. Add proper error handling and logging

### Task 3: Infrastructure Layer
**Timeline**: 30 minutes
**Files**:
- API handlers in `infra/api/handlers/`
- Database configurations if needed
- Message queue configurations

**Steps**:
1. Create API handlers with routers
2. Implement request/response handling
3. Add middleware if required
4. Configure database connections
5. Setup messaging infrastructure

### Task 4: Dependency Configuration
**Timeline**: 15 minutes
**Files**:
- Update `dependencies_container.py`
- Configuration updates in `settings/`

**Steps**:
1. Add all new dependencies to container
2. Configure database sessions
3. Setup external service connections
4. Configure security settings
5. Add environment variables

### Task 5: Testing Implementation
**Timeline**: 60 minutes
**Files**:
- Unit tests in `tests/unit/app/`
- Integration tests in `tests/integration/`
- E2E tests in `tests/e2e/`

**Steps**:
1. Create unit tests for all domain components
2. Create unit tests for all adapters
3. Create unit tests for API handlers
4. Create integration tests for complete flows
5. Create E2E tests for user scenarios

### Task 6: Documentation and Validation
**Timeline**: 30 minutes
**Files**:
- API documentation
- Architecture documentation
- Deployment documentation

**Steps**:
1. Update OpenAPI/Swagger documentation
2. Create feature documentation
3. Validate architecture compliance
4. Performance testing
5. Security validation

## Detailed Implementation

### Phase 1: Domain Layer

#### 1.1 Create Entities
```python
# domain/entities/feature.py
from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID
from datetime import datetime

@dataclass
class FeatureEntity:
    id: UUID
    name: str
    description: str
    config: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class CreateFeatureInput:
    name: str
    description: str
    config: dict

@dataclass
class CreateFeatureOutput:
    feature: FeatureEntity
    success: bool
    message: Optional[str] = None

@dataclass
class UpdateFeatureInput:
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[dict] = None

@dataclass
class UpdateFeatureOutput:
    feature: FeatureEntity
    success: bool
    message: Optional[str] = None
```

#### 1.2 Create Ports
```python
# domain/ports/feature_repository_port.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.feature import FeatureEntity, CreateFeatureInput, CreateFeatureOutput, UpdateFeatureInput, UpdateFeatureOutput

class FeatureRepositoryPort(ABC):
    @abstractmethod
    async def create(self, input_data: CreateFeatureInput) -> CreateFeatureOutput:
        pass
    
    @abstractmethod
    async def get_by_id(self, feature_id: UUID) -> Optional[FeatureEntity]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[FeatureEntity]:
        pass
    
    @abstractmethod
    async def update(self, input_data: UpdateFeatureInput) -> UpdateFeatureOutput:
        pass
    
    @abstractmethod
    async def delete(self, feature_id: UUID) -> bool:
        pass

# domain/ports/feature_event_port.py
from abc import ABC, abstractmethod

class FeatureEventPort(ABC):
    @abstractmethod
    async def publish_feature_created(self, feature: FeatureEntity):
        pass
    
    @abstractmethod
    async def publish_feature_updated(self, feature: FeatureEntity):
        pass
    
    @abstractmethod
    async def publish_feature_deleted(self, feature_id: UUID):
        pass
```

#### 1.3 Create Service
```python
# domain/services/feature_service.py
from typing import List, Optional
from domain.entities.feature import FeatureEntity, CreateFeatureInput, CreateFeatureOutput, UpdateFeatureInput, UpdateFeatureOutput
from domain.ports.feature_repository_port import FeatureRepositoryPort
from domain.ports.feature_event_port import FeatureEventPort

class FeatureService:
    def __init__(self, repository: FeatureRepositoryPort, event_publisher: FeatureEventPort):
        self.repository = repository
        self.event_publisher = event_publisher
    
    async def create_feature(self, input_data: CreateFeatureInput) -> CreateFeatureOutput:
        if not self._validate_feature_input(input_data):
            return CreateFeatureOutput(
                feature=None,
                success=False,
                message="Invalid feature data"
            )
        
        existing = await self.repository.get_by_name(input_data.name)
        if existing:
            return CreateFeatureOutput(
                feature=None,
                success=False,
                message="Feature with this name already exists"
            )
        
        result = await self.repository.create(input_data)
        
        if result.success:
            await self.event_publisher.publish_feature_created(result.feature)
        
        return result
    
    async def get_feature(self, feature_id: UUID) -> Optional[FeatureEntity]:
        return await self.repository.get_by_id(feature_id)
    
    async def get_all_features(self) -> List[FeatureEntity]:
        return await self.repository.get_all()
    
    async def update_feature(self, input_data: UpdateFeatureInput) -> UpdateFeatureOutput:
        existing = await self.repository.get_by_id(input_data.id)
        if not existing:
            return UpdateFeatureOutput(
                feature=None,
                success=False,
                message="Feature not found"
            )
        
        result = await self.repository.update(input_data)
        
        if result.success:
            await self.event_publisher.publish_feature_updated(result.feature)
        
        return result
    
    async def delete_feature(self, feature_id: UUID) -> bool:
        feature = await self.repository.get_by_id(feature_id)
        if not feature:
            return False
        
        result = await self.repository.delete(feature_id)
        
        if result:
            await self.event_publisher.publish_feature_deleted(feature_id)
        
        return result
    
    def _validate_feature_input(self, input_data: CreateFeatureInput) -> bool:
        return all([
            input_data.name and len(input_data.name.strip()) > 0,
            input_data.description and len(input_data.description.strip()) > 0,
            isinstance(input_data.config, dict)
        ])
```

### Phase 2: Adapter Layer

#### 2.1 Database Manager
```python
# infra/database/managers/feature_manager.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from infra.database.models.feature_model import FeatureModel
import uuid

class FeatureManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, feature_data: dict) -> FeatureModel:
        db_feature = FeatureModel(**feature_data)
        self.session.add(db_feature)
        await self.session.commit()
        await self.session.refresh(db_feature)
        return db_feature
    
    async def get_by_id(self, feature_id: str) -> Optional[FeatureModel]:
        result = await self.session.execute(
            select(FeatureModel).where(FeatureModel.id == feature_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> Optional[FeatureModel]:
        result = await self.session.execute(
            select(FeatureModel).where(FeatureModel.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[FeatureModel]:
        result = await self.session.execute(
            select(FeatureModel).where(FeatureModel.is_active == True)
        )
        return result.scalars().all()
    
    async def update(self, feature_id: str, update_data: dict) -> Optional[FeatureModel]:
        await self.session.execute(
            update(FeatureModel).where(FeatureModel.id == feature_id).values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_id(feature_id)
    
    async def delete(self, feature_id: str) -> bool:
        result = await self.session.execute(
            delete(FeatureModel).where(FeatureModel.id == feature_id)
        )
        await self.session.commit()
        return result.rowcount > 0
```

#### 2.2 Repository Adapter
```python
# adapters/database/feature_repository_adapter.py
from typing import List, Optional
from domain.ports.feature_repository_port import FeatureRepositoryPort
from domain.entities.feature import FeatureEntity, CreateFeatureInput, CreateFeatureOutput, UpdateFeatureInput, UpdateFeatureOutput
from infra.database.managers.feature_manager import FeatureManager
import uuid
from datetime import datetime

class FeatureRepositoryAdapter(FeatureRepositoryPort):
    def __init__(self, manager: FeatureManager):
        self.manager = manager
    
    async def create(self, input_data: CreateFeatureInput) -> CreateFeatureOutput:
        feature_dict = {
            "id": uuid.uuid4(),
            "name": input_data.name,
            "description": input_data.description,
            "config": input_data.config,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        db_feature = await self.manager.create(feature_dict)
        entity = self._model_to_entity(db_feature)
        
        return CreateFeatureOutput(
            feature=entity,
            success=True
        )
    
    async def get_by_id(self, feature_id: uuid.UUID) -> Optional[FeatureEntity]:
        db_feature = await self.manager.get_by_id(str(feature_id))
        return self._model_to_entity(db_feature) if db_feature else None
    
    async def get_by_name(self, name: str) -> Optional[FeatureEntity]:
        db_feature = await self.manager.get_by_name(name)
        return self._model_to_entity(db_feature) if db_feature else None
    
    async def get_all(self) -> List[FeatureEntity]:
        db_features = await self.manager.get_all()
        return [self._model_to_entity(f) for f in db_features]
    
    async def update(self, input_data: UpdateFeatureInput) -> UpdateFeatureOutput:
        update_data = {"updated_at": datetime.utcnow()}
        
        if input_data.name:
            update_data["name"] = input_data.name
        if input_data.description:
            update_data["description"] = input_data.description
        if input_data.config:
            update_data["config"] = input_data.config
        
        db_feature = await self.manager.update(str(input_data.id), update_data)
        
        if not db_feature:
            return UpdateFeatureOutput(
                feature=None,
                success=False,
                message="Feature not found"
            )
        
        entity = self._model_to_entity(db_feature)
        return UpdateFeatureOutput(
            feature=entity,
            success=True
        )
    
    async def delete(self, feature_id: uuid.UUID) -> bool:
        return await self.manager.delete(str(feature_id))
    
    def _model_to_entity(self, db_feature) -> FeatureEntity:
        return FeatureEntity(
            id=db_feature.id,
            name=db_feature.name,
            description=db_feature.description,
            config=db_feature.config,
            is_active=db_feature.is_active,
            created_at=db_feature.created_at,
            updated_at=db_feature.updated_at
        )
```

### Phase 3: Testing Strategy

#### 3.1 Unit Tests
```python
# tests/unit/app/domain/services/test_feature_service.py
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from domain.services.feature_service import FeatureService
from domain.entities.feature import CreateFeatureInput, FeatureEntity

@pytest.mark.asyncio
async def test_create_feature_success():
    mock_repo = AsyncMock()
    mock_events = AsyncMock()
    service = FeatureService(mock_repo, mock_events)
    
    input_data = CreateFeatureInput(
        name="Test Feature",
        description="Test Description",
        config={"key": "value"}
    )
    
    mock_repo.get_by_name.return_value = None
    mock_repo.create.return_value = CreateFeatureOutput(
        feature=FeatureEntity(
            id=uuid4(),
            name="Test Feature",
            description="Test Description",
            config={"key": "value"},
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        success=True
    )
    
    result = await service.create_feature(input_data)
    
    assert result.success is True
    mock_events.publish_feature_created.assert_called_once()
```

## Validation Commands

```bash
# Run complete test suite
pytest tests/ --cov=src/app --cov-report=html

# Check architecture compliance
python -c "
import src.app.dependencies_container
print('Architecture OK')
"

# Run specific feature tests
pytest tests/unit/app/domain/services/test_feature_service.py -v
pytest tests/unit/app/adapters/database/test_feature_repository_adapter.py -v
pytest tests/integration/api/test_feature_integration.py -v

# Performance testing
python -m pytest tests/performance/test_feature_performance.py -v
```

## Success Criteria
- [ ] All domain components implemented
- [ ] All adapters working correctly
- [ ] API endpoints functional
- [ ] Tests passing with 90%+ coverage
- [ ] Architecture rules followed
- [ ] Performance requirements met
- [ ] Security requirements satisfied
- [ ] Documentation complete
