---
description: Create a new API handler with self-contained router
---

## Workflow: Create API Handler

1. Create handler file in `infra/api/handlers/`
2. Define input/output dataclasses
3. Implement handler class with business logic
4. Create and initialize router within handler
5. Add handler to dependencies_container.py
6. Create API tests

Example structure:
```python
# infra/api/handlers/user_handler.py
from fastapi import APIRouter, Depends
from domain.services.user_service import UserService
from domain.entities.user import CreateUserInput, CreateUserOutput

class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.router = APIRouter(prefix="/users", tags=["users"])
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.post("/", response_model=CreateUserOutput)
        async def create_user(input_data: CreateUserInput):
            return await self.user_service.create_user(input_data)
```
