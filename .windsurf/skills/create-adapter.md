---
description: Create a new adapter with input/output dataclasses
---

# Skill: Create Adapter

## Overview
Creates a complete adapter following hexagonal architecture patterns with proper port implementation, dataclasses, and dependency injection.

## Prerequisites
- Read `/rules/architecture.yml` for structure guidelines
- Read `/contexts/architecture-context.md` for implementation patterns
- Identify adapter type: database, security, or messaging

## Steps

### 1. Create Port Interface
**Location**: `src/app/domain/ports/<name>_port.py`
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output

class <Name>Port(ABC):
    @abstractmethod
    async def <method>(self, input_data: <Action><Entity>Input) -> <Action><Entity>Output:
        pass
```

### 2. Create Input/Output Dataclasses
**Location**: `src/app/domain/entities/<entity>.py`
```python
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class <Action><Entity>Input:
    field1: str
    field2: Optional[str] = None

@dataclass
class <Action><Entity>Output:
    entity: <Entity>Entity
    success: bool
    message: Optional[str] = None
```

### 3. Implement Adapter
**Location**: `src/app/adapters/<type>/<name>_adapter.py`
```python
from typing import List
from domain.ports.<name>_port import <Name>Port
from domain.entities.<entity> import <Entity>Entity, <Action><Entity>Input, <Action><Entity>Output
from infra.<type>.<manager> import <Manager>

class <Name>Adapter(<Name>Port):
    def __init__(self, manager: <Manager>):
        self.manager = manager
    
    async def <method>(self, input_data: <Action><Entity>Input) -> <Action><Entity>Output:
        result = await self.manager.<operation>(input_data)
        return <Action><Entity>Output(entity=result, success=True)
```

### 4. Add to Dependencies Container
**Location**: `src/app/dependencies_container.py`
```python
from adapters.<type>.<name>_adapter import <Name>Adapter

class DependenciesContainer:
    def __init__(self):
        # Existing dependencies...
        self.<name>_adapter = <Name>Adapter(self.<manager>)
```

### 5. Create Unit Tests
**Location**: `tests/app/adapters/<type>/test_<name>_adapter.py`
```python
import pytest
from unittest.mock import AsyncMock, Mock
from adapters.<type>.<name>_adapter import <Name>Adapter

@pytest.mark.asyncio
async def test_<method>():
    mock_manager = AsyncMock()
    adapter = <Name>Adapter(mock_manager)
    input_data = <Action><Entity>Input(field1="test")
    
    result = await adapter.<method>(input_data)
    
    assert result.success is True
    mock_manager.<operation>.assert_called_once_with(input_data)
```

### 6. Create Integration Tests
**Location**: `tests/integration/<type>/test_<name>_integration.py`
```python
import pytest
from adapters.<type>.<name>_adapter import <Name>Adapter
from infra.<type>.<manager> import <Manager>

@pytest.mark.asyncio
async def test_<method>_integration():
    manager = <Manager>(test_config)
    adapter = <Name>Adapter(manager)
    input_data = <Action><Entity>Input(field1="test")
    
    result = await adapter.<method>(input_data)
    
    assert result.success is True
    assert result.entity.field1 == "test"
```

## Validation
- [ ] Port follows interface pattern
- [ ] Dataclasses used for all I/O
- [ ] Adapter implements port correctly
- [ ] Dependency injection configured
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] No business logic in adapter
- [ ] Proper error handling
