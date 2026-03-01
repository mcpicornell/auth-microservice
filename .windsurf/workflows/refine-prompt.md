---
description: Generate comprehensive implementation prompt based on application context
---

# Flow: Refine Prompt

## Overview
Analyzes the entire application context and generates a detailed, implementation-ready prompt instead of executing the implementation directly.

## Prerequisites
- Read `/rules/architecture.yml` for complete architecture rules
- Read all relevant skills in `/skills/`
- Read `/contexts/architecture-context.md` for patterns
- Read `/contexts/test-structure.md` for testing patterns
- Complete understanding of existing codebase

## Interactive Requirements Gathering

Before generating the prompt, I'll ask up to 4 clarifying questions with 3 options each to ensure the prompt covers exactly what you need.

### Question Template Pattern:
1. **Question about implementation scope**
   - Option A: Single component implementation
   - Option B: Feature-level implementation
   - Option C: Multi-feature system implementation

2. **Question about detail level**
   - Option A: High-level architecture guidance
   - Option B: Detailed implementation steps
   - Option C: Complete code-ready specifications

3. **Question about focus areas**
   - Option A: Domain and business logic focus
   - Option B: Infrastructure and API focus
   - Option C: Full-stack comprehensive focus

4. **Question about deliverable format**
   - Option A: Technical specification document
   - Option B: Step-by-step implementation guide
   - Option C: Ready-to-execute prompt with code examples

## Context Analysis Process

### Step 1: Application Architecture Analysis
**Timeline**: 15 minutes
**Analysis Areas**:
- Current hexagonal architecture implementation
- Existing domain entities and services
- Adapter patterns in use
- Infrastructure configurations
- Dependency injection setup

### Step 2: Feature Integration Assessment
**Timeline**: 10 minutes
**Assessment Areas**:
- Existing entities and relationships
- Current API endpoints and patterns
- Database schema and models
- Security implementations
- Testing patterns and coverage

### Step 3: Technical Requirements Gathering
**Timeline**: 15 minutes
**Requirements Areas**:
- Performance considerations
- Security requirements
- Scalability needs
- Integration points
- Compliance requirements

### Step 4: Prompt Generation
**Timeline**: 20 minutes
**Generation Process**:
1. **Context Summary**: Brief overview of current application state
2. **Architecture Alignment**: Ensure compliance with existing patterns
3. **Implementation Strategy**: Detailed step-by-step approach
4. **Code Specifications**: Exact code structures and patterns
5. **Testing Requirements**: Comprehensive test specifications
6. **Integration Guidelines**: How to integrate with existing code
7. **Validation Criteria**: Success metrics and validation steps

## Generated Prompt Structure

### Section 1: Context Overview
```markdown
## Application Context
- Architecture: Hexagonal with clear separation of concerns
- Current Domain: [List existing entities and services]
- Current Infrastructure: [API patterns, database setup]
- Testing Strategy: [Current testing patterns and coverage]
```

### Section 2: Implementation Requirements
```markdown
## Feature Requirements
### Functional Requirements
- [Detailed functional specifications]

### Non-Functional Requirements
- Performance: [Specific requirements]
- Security: [Security considerations]
- Scalability: [Scalability requirements]

### Integration Requirements
- [How this integrates with existing code]
```

### Section 3: Architecture Specifications
```markdown
## Architecture Implementation
### Domain Layer
- Entity specifications with exact dataclass structures
- Service interfaces and business logic patterns
- Port definitions for external dependencies

### Adapter Layer
- Repository adapter implementations
- Security adapter patterns
- Messaging adapter specifications

### Infrastructure Layer
- API handler patterns and routing
- Database integration specifications
- Configuration and settings
```

### Section 4: Implementation Steps
```markdown
## Step-by-Step Implementation
### Phase 1: Domain Implementation
1. Create entity: [Exact code structure]
2. Implement service: [Business logic patterns]
3. Define ports: [Interface specifications]

### Phase 2: Adapter Implementation
1. Database adapter: [Implementation patterns]
2. Security integration: [Security patterns]
3. Error handling: [Error management]

### Phase 3: Infrastructure Implementation
1. API endpoints: [Routing and handler patterns]
2. Dependency injection: [Wiring specifications]
3. Configuration: [Settings management]
```

### Section 5: Testing Specifications
```markdown
## Testing Requirements
### Unit Tests
- Domain entity tests: [Test patterns]
- Service tests: [Mock and test patterns]
- Adapter tests: [Integration test patterns]

### Integration Tests
- API integration: [End-to-end test patterns]
- Database integration: [Data validation patterns]

### Performance Tests
- Load testing: [Performance criteria]
- Security testing: [Security validation]
```

### Section 6: Validation and Deployment
```markdown
## Validation Criteria
- Architecture compliance checks
- Test coverage requirements (90%+)
- Performance benchmarks
- Security validations
- Integration verification

## Deployment Considerations
- Database migrations
- Configuration updates
- API versioning
- Monitoring setup
```

## Prompt Generation Examples

### Example 1: Simple Entity Creation
```markdown
Create a User entity following the existing hexagonal architecture pattern:

## Context
Current app has User, Session, Permission entities in domain/entities/
Uses FastAPI with SQLAlchemy, JWT authentication, PostgreSQL database

## Requirements
Create a Profile entity linked to User with:
- Basic profile information (bio, avatar_url, preferences)
- Privacy settings
- Profile completion tracking

## Implementation
1. Domain Entity: ProfileEntity dataclass in domain/entities/profile.py
2. Repository Port: ProfileRepositoryPort in domain/ports/profile_repository_port.py
3. Service: ProfileService in domain/services/profile_service.py
4. Database Adapter: ProfileRepositoryAdapter in adapters/database/profile_repository_adapter.py
5. API Handler: ProfileHandler in infra/api/handlers/profile_handler.py

## Testing
- Unit tests for all components
- Integration tests for API endpoints
- Test coverage 90%+

## Integration
- Link to existing User entity
- Follow existing dependency injection pattern
- Use existing error handling patterns
```

### Example 2: Complex Feature Implementation
```markdown
Implement a Notification System following hexagonal architecture:

## Context
Auth microservice with User, Session entities
FastAPI, PostgreSQL, Redis for caching
JWT authentication, role-based permissions

## Requirements
Multi-channel notification system:
- Email notifications
- In-app notifications
- Push notifications
- Notification preferences per user
- Notification history and tracking

## Implementation
### Domain Layer
- NotificationEntity, NotificationPreferenceEntity
- NotificationService with business rules
- Ports: EmailPort, PushPort, InAppPort

### Adapter Layer
- EmailAdapter (SMTP integration)
- PushAdapter (Firebase/APNS integration)
- InAppAdapter (Database storage)
- NotificationRepositoryAdapter

### Infrastructure Layer
- NotificationHandler with multiple endpoints
- Background job processing
- Rate limiting and throttling

### Testing
- Unit tests for all components
- Integration tests with external services
- Performance tests for high-volume scenarios
```

## Usage Instructions

### When to Use This Flow
- Complex features requiring detailed planning
- When you want to review implementation approach before coding
- For team collaboration on implementation strategy
- When creating documentation for future development

### Expected Output
A comprehensive, ready-to-execute prompt that includes:
- Complete context understanding
- Detailed implementation specifications
- Step-by-step coding instructions
- Comprehensive testing requirements
- Integration guidelines
- Validation criteria

### Next Steps After Prompt Generation
1. Review the generated prompt for completeness
2. Adjust any specifications based on feedback
3. Use the prompt with an AI assistant for implementation
4. Follow the step-by-step implementation guide
5. Validate against the provided criteria

## Success Criteria
- [ ] Prompt covers all implementation aspects
- [ ] Context accurately reflects current application state
- [ ] Implementation steps are clear and actionable
- [ ] Testing requirements are comprehensive
- [ ] Integration guidelines are precise
- [ ] Validation criteria are measurable
- [ ] Prompt is ready for immediate execution
