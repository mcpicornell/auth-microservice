---
description: Create comprehensive tests for any component following architecture patterns
---

# Skill: Create Tests

## Overview
Creates comprehensive tests for any component following the established test structure and architecture patterns.

## Prerequisites
- Read `/rules/architecture.yml` for architecture compliance
- Read `/contexts/test-structure.md` for test organization
- Read `/contexts/architecture-context.md` for implementation patterns
- Identify component type and testing requirements

## Test Types by Component

### Domain Entity Tests
**Location**: `tests/unit/app/domain/entities/test_<entity>.py`

```python
import pytest
from uuid import uuid4
from datetime import datetime

from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output

class Test<Entity>Entity:
    def test_entity_creation_success(self):
        entity = <Entity>Entity(
            id=uuid4(),
            field1="test_value",
            field2="optional_value",
            created_at=datetime.utcnow()
        )
        
        assert entity.field1 == "test_value"
        assert entity.field2 == "optional_value"
        assert entity.is_active is True
    
    def test_entity_with_minimal_data(self):
        entity = <Entity>Entity(
            id=uuid4(),
            field1="test_value",
            created_at=datetime.utcnow()
        )
        
        assert entity.field1 == "test_value"
        assert entity.field2 is None
    
    def test_entity_invalid_data(self):
        with pytest.raises(TypeError):
            <Entity>Entity(
                id=None,
                field1="test_value"
            )

class Test<Action><Entity>Input:
    def test_input_creation_success(self):
        input_data = <Action><Entity>Input(
            field1="required_value",
            field2="optional_value"
        )
        
        assert input_data.field1 == "required_value"
        assert input_data.field2 == "optional_value"
    
    def test_input_minimal_data(self):
        input_data = <Action><Entity>Input(field1="required_value")
        
        assert input_data.field1 == "required_value"
        assert input_data.field2 is None

class Test<Action><Entity>Output:
    def test_output_success(self):
        entity = <Entity>Entity(
            id=uuid4(),
            field1="test_value",
            created_at=datetime.utcnow()
        )
        
        output = <Action><Entity>Output(
            entity=entity,
            success=True,
            message="Operation completed"
        )
        
        assert output.success is True
        assert output.entity.field1 == "test_value"
        assert output.message == "Operation completed"
    
    def test_output_failure(self):
        output = <Action><Entity>Output(
            entity=None,
            success=False,
            message="Operation failed"
        )
        
        assert output.success is False
        assert output.entity is None
        assert output.message == "Operation failed"
```

### Domain Service Tests
**Location**: `tests/unit/app/domain/services/test_<service>.py`

```python
import pytest
from unittest.mock import AsyncMock, Mock, call
from uuid import uuid4
from datetime import datetime

from domain.services.<service> import <Service>
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output
from domain.ports.<repo>_port import <Repo>Port
from domain.ports.<external>_port import <External>Port

class Test<Service>:
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock(spec=<Repo>Port)
    
    @pytest.fixture
    def mock_external(self):
        return AsyncMock(spec=<External>Port)
    
    @pytest.fixture
    def service(self, mock_repository, mock_external):
        return <Service>(mock_repository, mock_external)
    
    @pytest.fixture
    def sample_entity(self):
        return <Entity>Entity(
            id=uuid4(),
            field1="test_value",
            field2="optional_value",
            created_at=datetime.utcnow()
        )
    
    @pytest.fixture
    def sample_input(self):
        return <Action><Entity>Input(
            field1="test_value",
            field2="optional_value"
        )

    @pytest.mark.asyncio
    async def test_<action>_success(self, service, mock_repository, mock_external, sample_input, sample_entity):
        mock_repository.get_by_field.return_value = None
        mock_repository.create.return_value = <Action><Entity>Output(
            entity=sample_entity,
            success=True
        )
        
        result = await service.<action>(sample_input)
        
        assert result.success is True
        assert result.entity == sample_entity
        mock_repository.get_by_field.assert_called_once_with("field1", sample_input.field1)
        mock_repository.create.assert_called_once_with(sample_input)
        mock_external.publish_event.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_<action>_already_exists(self, service, mock_repository, mock_external, sample_input, sample_entity):
        mock_repository.get_by_field.return_value = sample_entity
        
        result = await service.<action>(sample_input)
        
        assert result.success is False
        assert "already exists" in result.message
        mock_repository.create.assert_not_called()
        mock_external.publish_event.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_<action>_repository_error(self, service, mock_repository, mock_external, sample_input):
        mock_repository.get_by_field.return_value = None
        mock_repository.create.side_effect = Exception("Database error")
        
        result = await service.<action>(sample_input)
        
        assert result.success is False
        assert "Internal error" in result.message
        mock_external.publish_event.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_by_id_success(self, service, mock_repository, sample_entity):
        mock_repository.get_by_id.return_value = sample_entity
        
        result = await service.get_by_id(str(sample_entity.id))
        
        assert result == sample_entity
        mock_repository.get_by_id.assert_called_once_with(str(sample_entity.id))
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None
        
        result = await service.get_by_id("non-existent-id")
        
        assert result is None
        mock_repository.get_by_id.assert_called_once_with("non-existent-id")
```

### Repository Adapter Tests
**Location**: `tests/unit/app/adapters/<type>/test_<name>_adapter.py`

```python
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime

from adapters.<type>.<name>_adapter import <Name>Adapter
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output
from infra.<type>.managers.<name>_manager import <Name>Manager

class Test<Name>Adapter:
    @pytest.fixture
    def mock_manager(self):
        return AsyncMock(spec=<Name>Manager)
    
    @pytest.fixture
    def adapter(self, mock_manager):
        return <Name>Adapter(mock_manager)
    
    @pytest.fixture
    def sample_entity_dict(self):
        return {
            "id": uuid4(),
            "field1": "test_value",
            "field2": "optional_value",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    @pytest.fixture
    def sample_input(self):
        return <Action><Entity>Input(
            field1="test_value",
            field2="optional_value"
        )

    @pytest.mark.asyncio
    async def test_create_success(self, adapter, mock_manager, sample_input, sample_entity_dict):
        mock_manager.create.return_value = Mock(**sample_entity_dict)
        
        result = await adapter.create(sample_input)
        
        assert result.success is True
        assert result.entity.field1 == "test_value"
        mock_manager.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_id_success(self, adapter, mock_manager, sample_entity_dict):
        mock_manager.get_by_id.return_value = Mock(**sample_entity_dict)
        
        result = await adapter.get_by_id(str(sample_entity_dict["id"]))
        
        assert result is not None
        assert result.field1 == "test_value"
        mock_manager.get_by_id.assert_called_once_with(str(sample_entity_dict["id"]))
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, adapter, mock_manager):
        mock_manager.get_by_id.return_value = None
        
        result = await adapter.get_by_id("non-existent-id")
        
        assert result is None
        mock_manager.get_by_id.assert_called_once_with("non-existent-id")
    
    @pytest.mark.asyncio
    async def test_update_success(self, adapter, mock_manager, sample_entity_dict):
        updated_dict = sample_entity_dict.copy()
        updated_dict["field1"] = "updated_value"
        mock_manager.update.return_value = Mock(**updated_dict)
        
        update_input = <Action><Entity>Input(
            id=sample_entity_dict["id"],
            field1="updated_value"
        )
        
        result = await adapter.update(update_input)
        
        assert result.success is True
        assert result.entity.field1 == "updated_value"
        mock_manager.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_success(self, adapter, mock_manager):
        mock_manager.delete.return_value = True
        
        result = await adapter.delete("entity-id")
        
        assert result is True
        mock_manager.delete.assert_called_once_with("entity-id")
    
    @pytest.mark.asyncio
    async def test_delete_failure(self, adapter, mock_manager):
        mock_manager.delete.return_value = False
        
        result = await adapter.delete("non-existent-id")
        
        assert result is False
        mock_manager.delete.assert_called_once_with("non-existent-id")
```

### API Handler Tests
**Location**: `tests/unit/app/infra/api/handlers/test_<handler>.py`

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from infra.api.handlers.<handler> import <Handler>
from domain.services.<service> import <Service>
from domain.entities.<entity> import <Action><Entity>Input, <Action><Entity>Output
from main import app

class Test<Handler>:
    @pytest.fixture
    def mock_service(self):
        return AsyncMock(spec=<Service>)
    
    @pytest.fixture
    def handler(self, mock_service):
        return <Handler>(mock_service)
    
    @pytest.fixture
    def client(self, handler):
        app.include_router(handler.router)
        return TestClient(app)
    
    @pytest.fixture
    def sample_input(self):
        return {
            "field1": "test_value",
            "field2": "optional_value"
        }
    
    @pytest.fixture
    def sample_entity(self):
        return {
            "id": str(uuid4()),
            "field1": "test_value",
            "field2": "optional_value",
            "created_at": "2024-01-01T00:00:00Z"
        }

    def test_create_endpoint_success(self, client, mock_service, sample_input, sample_entity):
        mock_service.<action>.return_value = <Action><Entity>Output(
            entity=sample_entity,
            success=True,
            message="Created successfully"
        )
        
        response = client.post("/<endpoint>/", json=sample_input)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["entity"]["field1"] == "test_value"
        mock_service.<action>.assert_called_once()
    
    def test_create_endpoint_validation_error(self, client, sample_input):
        invalid_input = sample_input.copy()
        invalid_input["field1"] = ""  # Invalid empty field
        
        response = client.post("/<endpoint>/", json=invalid_input)
        
        assert response.status_code == 422
    
    def test_create_endpoint_business_error(self, client, mock_service, sample_input):
        mock_service.<action>.return_value = <Action><Entity>Output(
            entity=None,
            success=False,
            message="Business rule violation"
        )
        
        response = client.post("/<endpoint>/", json=sample_input)
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "Business rule violation" in data["detail"]
    
    def test_get_by_id_success(self, client, mock_service, sample_entity):
        mock_service.get_by_id.return_value = sample_entity
        
        response = client.get(f"/<endpoint>/{sample_entity['id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["field1"] == "test_value"
        mock_service.get_by_id.assert_called_once_with(sample_entity["id"])
    
    def test_get_by_id_not_found(self, client, mock_service):
        mock_service.get_by_id.return_value = None
        
        response = client.get("/<endpoint>/non-existent-id")
        
        assert response.status_code == 404
    
    def test_update_endpoint_success(self, client, mock_service, sample_entity):
        update_data = {"field1": "updated_value"}
        updated_entity = sample_entity.copy()
        updated_entity["field1"] = "updated_value"
        
        mock_service.update.return_value = <Action><Entity>Output(
            entity=updated_entity,
            success=True
        )
        
        response = client.put(f"/<endpoint>/{sample_entity['id']}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["entity"]["field1"] == "updated_value"
    
    def test_delete_endpoint_success(self, client, mock_service):
        mock_service.delete.return_value = True
        
        response = client.delete("/<endpoint>/entity-id")
        
        assert response.status_code == 204
        mock_service.delete.assert_called_once_with("entity-id")
    
    def test_delete_endpoint_not_found(self, client, mock_service):
        mock_service.delete.return_value = False
        
        response = client.delete("/<endpoint>/non-existent-id")
        
        assert response.status_code == 404
```

### Integration Tests
**Location**: `tests/integration/<type>/test_<name>_integration.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from main import app
from adapters.database.<name>_repository_adapter import <Name>RepositoryAdapter
from infra.database.managers.<name>_manager import <Name>Manager

class Test<Name>Integration:
    @pytest.fixture
    def test_session(self):
        # Create test database session
        pass
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def repository(self, test_session):
        manager = <Name>Manager(test_session)
        return <Name>RepositoryAdapter(manager)

    @pytest.mark.asyncio
    async def test_complete_workflow(self, repository, client):
        # Test complete workflow from API to database
        input_data = {
            "field1": "integration_test",
            "field2": "optional_value"
        }
        
        # Create via API
        response = client.post("/<endpoint>/", json=input_data)
        assert response.status_code == 201
        
        created_data = response.json()
        entity_id = created_data["entity"]["id"]
        
        # Verify via repository
        entity = await repository.get_by_id(entity_id)
        assert entity is not None
        assert entity.field1 == "integration_test"
        
        # Update via API
        update_data = {"field1": "updated_integration_test"}
        response = client.put(f"/<endpoint>/{entity_id}", json=update_data)
        assert response.status_code == 200
        
        # Verify update
        updated_entity = await repository.get_by_id(entity_id)
        assert updated_entity.field1 == "updated_integration_test"
        
        # Delete via API
        response = client.delete(f"/<endpoint>/{entity_id}")
        assert response.status_code == 204
        
        # Verify deletion
        deleted_entity = await repository.get_by_id(entity_id)
        assert deleted_entity is None

    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, client):
        # Test error scenarios in integration
        invalid_data = {"field1": ""}  # Invalid data
        
        response = client.post("/<endpoint>/", json=invalid_data)
        assert response.status_code == 422
        
        # Test non-existent entity
        response = client.get("/<endpoint>/non-existent-id")
        assert response.status_code == 404
```

## Test Creation Steps

### Step 1: Identify Component Type
- Domain entity → Entity tests
- Domain service → Service tests
- Repository adapter → Adapter tests
- API handler → Handler tests
- Complete workflow → Integration tests

### Step 2: Create Test File Structure
1. Create appropriate directory structure
2. Name file following convention: `test_<component>.py`
3. Import necessary modules and fixtures

### Step 3: Implement Test Cases
1. **Success scenarios**: Normal operation
2. **Failure scenarios**: Error handling
3. **Edge cases**: Boundary conditions
4. **Integration points**: External dependencies

### Step 4: Add Fixtures and Mocks
1. Create reusable fixtures
2. Mock external dependencies
3. Set up test data

### Step 5: Validate Coverage
1. Run tests with coverage
2. Ensure 90%+ coverage requirement
3. Add missing test cases

## Running Tests

### Command Examples
```bash
# Run all tests
pytest tests/ --cov=src/app --cov-report=html

# Run specific component tests
pytest tests/unit/app/domain/entities/test_user.py -v

# Run integration tests
pytest tests/integration/ -v

# Run with specific markers
pytest tests/ -m "unit" -v
pytest tests/ -m "integration" -v

# Run performance tests
pytest tests/performance/ -v
```

## Validation Checklist
- [ ] Test file follows naming convention
- [ ] Test structure mirrors source structure
- [ ] All success scenarios covered
- [ ] All failure scenarios covered
- [ ] Edge cases tested
- [ ] Proper async testing with pytest.mark.asyncio
- [ ] Mocks configured correctly
- [ ] Architecture rules followed in tests
- [ ] Coverage requirements met
- [ ] Tests are independent and deterministic
