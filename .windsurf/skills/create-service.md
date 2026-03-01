---
description: Create a domain service with business logic and port coordination
---

# Skill: Create Service

## Overview
Creates a domain service with pure business logic, coordinating between multiple ports and following clean architecture principles.

## Prerequisites
- Read `/rules/architecture.yml` for domain layer rules
- Read `/contexts/architecture-context.md` for service patterns
- Identify business requirements and port dependencies

## Steps

### 1. Define Service Interface
**Location**: `src/app/domain/services/<name>_service.py`
```python
from typing import Optional
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output
from domain.ports.<repo>_port import <Repo>Port
from domain.ports.<external>_port import <External>Port

class <Name>Service:
    def __init__(self, <repo>: <Repo>Port, <external>: <External>Port):
        self.<repo> = <repo>
        self.<external> = <external>
    
    async def <action>(self, input_data: <Action><Entity>Input) -> <Action><Entity>Output:
        existing = await self.<repo>.get_by_field("field", input_data.field)
        if existing:
            return <Action><Entity>Output(
                entity=None,
                success=False,
                message="Already exists"
            )
        
        result = await self.<repo>.create(input_data)
        
        if result.success:
            await self.<external>.publish_event({
                "type": "<entity>_created",
                "data": result.entity.__dict__
            })
        
        return result
    
    async def <other_action>(self, entity_id: str) -> Optional[<Entity>Entity]:
        entity = await self.<repo>.get_by_id(entity_id)
        if not entity:
            return None
        
        await self.<external>.publish_event({
            "type": "<entity>_accessed",
            "data": {"id": entity_id}
        })
        
        return entity
```

### 2. Create Business Logic Methods
**Location**: Same file, add validation and business rules
```python
def _validate_<action>_input(self, input_data: <Action><Entity>Input) -> bool:
    if not input_data.field or len(input_data.field) < 3:
        return False
    if input_data.field2 and not self._is_valid_format(input_data.field2):
        return False
    return True

def _is_valid_format(self, value: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value))

async def _check_business_rules(self, input_data: <Action><Entity>Input) -> tuple[bool, str]:
    if await self._exists_with_different_criteria(input_data):
        return False, "Conflict with existing data"
    
    if not self._meets_business_requirements(input_data):
        return False, "Does not meet business requirements"
    
    return True, "Valid"

async def _exists_with_different_criteria(self, input_data: <Action><Entity>Input) -> bool:
    existing = await self.<repo>.get_by_field("unique_field", input_data.unique_field)
    return existing is not None

def _meets_business_requirements(self, input_data: <Action><Entity>Input) -> bool:
    return all([
        input_data.required_field,
        len(input_data.required_field) >= 3,
        input_data.optional_field is None or len(input_data.optional_field) > 0
    ])
```

### 3. Add Error Handling
**Location**: Same file, add comprehensive error handling
```python
async def <action>_with_error_handling(self, input_data: <Action><Entity>Input) -> <Action><Entity>Output:
    try:
        if not self._validate_<action>_input(input_data):
            return <Action><Entity>Output(
                entity=None,
                success=False,
                message="Invalid input data"
            )
        
        is_valid, message = await self._check_business_rules(input_data)
        if not is_valid:
            return <Action><Entity>Output(
                entity=None,
                success=False,
                message=message
            )
        
        return await self.<action>(input_data)
    
    except Exception as e:
        return <Action><Entity>Output(
            entity=None,
            success=False,
            message=f"Internal error: {str(e)}"
        )
```

### 4. Add to Dependencies Container
**Location**: `src/app/dependencies_container.py`
```python
from domain.services.<name>_service import <Name>Service

class DependenciesContainer:
    def __init__(self):
        # Existing dependencies...
        self.<name>_service = <Name>Service(
            <repo>=self.<repo>_repository,
            <external>=self.<external>_adapter
        )
```

### 5. Create Unit Tests
**Location**: `tests/app/domain/services/test_<name>_service.py`
```python
import pytest
from unittest.mock import AsyncMock, Mock
from domain.services.<name>_service import <Name>Service

@pytest.mark.asyncio
async def test_<action>_success():
    mock_repo = AsyncMock()
    mock_external = AsyncMock()
    service = <Name>Service(mock_repo, mock_external)
    
    input_data = <Action><Entity>Input(field="test")
    mock_repo.get_by_field.return_value = None
    mock_repo.create.return_value = <Action><Entity>Output(
        entity=<Entity>Entity(id="1", field="test"),
        success=True
    )
    
    result = await service.<action>(input_data)
    
    assert result.success is True
    mock_repo.create.assert_called_once_with(input_data)
    mock_external.publish_event.assert_called_once()

@pytest.mark.asyncio
async def test_<action>_already_exists():
    mock_repo = AsyncMock()
    mock_external = AsyncMock()
    service = <Name>Service(mock_repo, mock_external)
    
    input_data = <Action><Entity>Input(field="test")
    existing_entity = <Entity>Entity(id="1", field="test")
    mock_repo.get_by_field.return_value = existing_entity
    
    result = await service.<action>(input_data)
    
    assert result.success is False
    assert "Already exists" in result.message
    mock_repo.create.assert_not_called()

@pytest.mark.asyncio
async def test_validation():
    mock_repo = AsyncMock()
    mock_external = AsyncMock()
    service = <Name>Service(mock_repo, mock_external)
    
    invalid_input = <Action><Entity>Input(field="")
    
    assert not service._validate_<action>_input(invalid_input)

@pytest.mark.asyncio
async def test_business_rules():
    mock_repo = AsyncMock()
    mock_external = AsyncMock()
    service = <Name>Service(mock_repo, mock_external)
    
    input_data = <Action><Entity>Input(field="test")
    mock_repo.get_by_field.return_value = None
    
    is_valid, message = await service._check_business_rules(input_data)
    
    assert is_valid is True
    assert message == "Valid"
```

### 6. Create Integration Tests
**Location**: `tests/integration/domain/test_<name>_service_integration.py`
```python
import pytest
from domain.services.<name>_service import <Name>Service
from adapters.database.<entity>_repository_adapter import <Entity>RepositoryAdapter
from adapters.messaging.<external>_adapter import <External>Adapter

@pytest.mark.asyncio
async def test_service_integration(test_session, test_messaging):
    repo_adapter = <Entity>RepositoryAdapter(<Entity>Manager(test_session))
    external_adapter = <External>Adapter(test_messaging)
    service = <Name>Service(repo_adapter, external_adapter)
    
    input_data = <Action><Entity>Input(field="integration_test")
    
    result = await service.<action>(input_data)
    
    assert result.success is True
    assert result.entity.field == "integration_test"
```

## Validation
- [ ] Service has pure business logic
- [ ] No external dependencies in domain
- [ ] Proper port coordination
- [ ] Input validation implemented
- [ ] Business rules enforced
- [ ] Error handling comprehensive
- [ ] Unit tests cover all scenarios
- [ ] Integration tests validate flow
- [ ] Dependency injection configured
- [ ] No framework-specific code
