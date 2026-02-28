---
description: Load architecture context and enforce rules
---

# Architecture Context Loading

1. Read `.windsurf/architecture-rules.yml` for project structure
2. Apply hexagonal architecture principles strictly
3. Enforce all forbidden patterns
4. Follow dependency injection pattern
5. Use async-first approach
6. No comments or docstrings allowed
7. All documentation in English only
8. No plain text credentials in defaults

# Structure Rules

- Domain: Pure business logic, no external deps
- Adapters: Implement ports, handle external integrations  
- Infra: Database models, API handlers, framework code
- Settings: Environment variables, secure defaults

# Forbidden Patterns

- Comments (#)
- Docstrings ("""...""")
- Business logic in adapters
- Framework code in domain
- Plain text credentials
- Non-English documentation

# Implementation Guidelines

- Use dataclasses for all entities
- Async methods for I/O operations
- Dependency injection via container
- Port-adapter pattern for integrations
- Settings class for configuration
