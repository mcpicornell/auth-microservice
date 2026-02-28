---
description: Create a new adapter with input/output dataclasses
---

## Workflow: Create New Adapter

1. Create port interface in `domain/ports/`
2. Create input/output dataclasses in `domain/entities/`
3. Implement adapter in `adapters/`
4. Add adapter to dependencies_container.py
5. Create unit tests for adapter
6. Create integration tests

Example:
```bash
# Create port
echo "from abc import ABC, abstractmethod
from typing import List
from domain.entities.user import UserEntity

class UserRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user_data: UserCreateInput) -> UserEntity:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity:
        pass" > domain/ports/user_repository.py
```
