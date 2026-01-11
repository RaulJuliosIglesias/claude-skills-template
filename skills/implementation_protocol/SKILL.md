---
name: Implementation Protocol
description: |
  Guides implementation following best practices, respecting existing architecture and
  maintaining consistency with project code. Ensures that each implementation is
  professional, testable, documented, and aligned with project standards.
version: 1.0.0
---

# Implementation Protocol Skill

## Purpose

This skill ensures that all implementation follows a consistent and professional protocol, ensuring:

1. **Respect for existing architecture**
2. **Consistency** with project code and conventions
3. **Quality** following best practices
4. **Testability** and maintainability
5. **Appropriate documentation**

## Methodology: Implementation Protocol

### Phase 1: Preparation

**Objective**: Prepare the environment and understand the context

**Process**:
1. Review requirements analysis
2. Review codebase analysis
3. Identify exact location for new files
4. Verify necessary dependencies
5. Prepare file structure

**Checklist**:
- [ ] Requirements clear and documented
- [ ] Current project state understood
- [ ] File location defined
- [ ] Dependencies verified/installed
- [ ] Structure prepared

### Phase 2: Solution Design

**Objective**: Design the solution respecting the existing project

**Process**:
1. Design following existing patterns
2. Define component/function structure
3. Plan integration with existing code
4. Identify extension points
5. Consider edge cases and errors

**Principles**:
- **DRY (Don't Repeat Yourself)**: Reuse existing code
- **KISS (Keep It Simple, Stupid)**: Simple and clear solutions
- **Consistency**: Follow project patterns
- **Separation of concerns**: Each component has a clear purpose

**Output**:
```
Solution Design:
- Components to create: [list]
- Components to modify: [list]
- Proposed structure: [description]
- Integration: [how it integrates]
- Considerations: [important notes]
```

### Phase 3: Implementation

**Objective**: Write quality code

**Process**:
1. Create file structure
2. Implement following conventions
3. Use project patterns
4. Maintain style consistency
5. Add comments where necessary

**Implementation Rules**:

#### Nomenclature
- Follow project conventions
- Descriptive and clear names
- Avoid unnecessary abbreviations

#### Code Structure
- Organize imports (external, internal, relative)
- Group related logic
- Separate concerns (UI, logic, data)

#### Code Quality
- Small, focused functions
- Avoid duplicate code
- Handle errors appropriately
- Validate inputs when necessary

#### Consistency
- Follow existing code style
- Use same patterns as project
- Maintain structure similar to related code

**Implementation Template**:

```typescript
// Example for React component
import React from 'react';
import { existingUtility } from '../utils';
import { ExistingType } from '../types';

/**
 * [Component description]
 * 
 * @param props - [Props description]
 */
export const NewComponent: React.FC<Props> = ({ prop1, prop2 }) => {
  // Component logic
  // Following project patterns
  
  return (
    // JSX following project structure
  );
};
```

### Phase 4: Integration

**Objective**: Correctly integrate with existing code

**Process**:
1. Import/export correctly
2. Integrate with existing components
3. Connect with services/APIs
4. Update routes if necessary
5. Verify it doesn't break existing functionality

**Integration Checklist**:
- [ ] Correct imports
- [ ] Appropriate exports
- [ ] Integrated with parent components
- [ ] Connected with necessary services
- [ ] Routes updated if applicable
- [ ] Doesn't break existing functionality

### Phase 5: Validation

**Objective**: Verify that implementation meets requirements

**Process**:
1. Review implemented code
2. Verify it meets requirements
3. Validate it respects architecture
4. Verify consistency with project
5. Test basic functionality

**Validation Checklist**:
- [ ] Code completely implemented
- [ ] Meets all requirements
- [ ] Respects project architecture
- [ ] Consistent with existing code
- [ ] Basic functionality verified
- [ ] No syntax/compilation errors

### Phase 6: Documentation

**Objective**: Appropriately document the implementation

**Process**:
1. Add comments in complex code
2. Document main functions/components
3. Update README if necessary
4. Document important decisions
5. Add usage examples if applicable

**Documentation Level**:
- **Inline comments**: For complex logic
- **JSDoc/TSDoc**: For public functions and components
- **README**: For important features or significant changes
- **Decision comments**: To explain why a solution was chosen

## Golden Rules of Implementation

1. **Respect existing**: Never change patterns without reason
2. **Maintain consistency**: Follow project conventions
3. **Clean code**: Readable, maintainable, well-structured
4. **Handle errors**: Validate inputs, handle edge cases
5. **Document decisions**: Explain important choices
6. **Don't break anything**: Verify changes don't affect existing functionality

## Common Patterns by Project Type

### React/TypeScript
- Functional components with hooks
- TypeScript for type safety
- Separation of components, hooks, utils, types
- Custom hooks for reusable logic

### Node.js/Express
- Separation of routes, controllers, services
- Middleware for shared logic
- Centralized error handling
- Input validation

### Python
- PEP 8 style guide
- Type hints where possible
- Docstrings for functions
- Separation of concerns

## Complete Implementation Checklist

### Before Implementing
- [ ] Requirements analyzed
- [ ] Current state understood
- [ ] Implementation plan created
- [ ] Dependencies verified

### During Implementation
- [ ] Following naming conventions
- [ ] Using project patterns
- [ ] Clean and readable code
- [ ] Appropriate error handling

### After Implementing
- [ ] Correctly integrated
- [ ] Validated against requirements
- [ ] Consistent with project
- [ ] Appropriately documented
- [ ] No compilation errors

## Complete Flow Example

```
Requirement: Add logout button

Phase 1 (Preparation):
- Location: Header component
- Dependency: Existing AuthContext

Phase 2 (Design):
- Create LogoutButton component
- Integrate in Header
- Use logout function from AuthContext

Phase 3 (Implementation):
- Create LogoutButton.tsx
- Follow structure of other buttons
- Use project styles

Phase 4 (Integration):
- Import in Header
- Add to Header JSX
- Connect with AuthContext

Phase 5 (Validation):
- Verify it works
- Verify consistent styles
- Verify it doesn't break anything

Phase 6 (Documentation):
- JSDoc comment in component
- Document usage if necessary
```

## Integration with Other Skills

This skill receives input from:
- `requirements_analyzer`: What to implement
- `codebase_understanding`: How to implement respecting the project
- `project_protocol`: Process orchestration

## Common Error Handling

### Error: Doesn't follow conventions
**Solution**: Review existing code and adjust

### Error: Breaks existing functionality
**Solution**: Review integration, verify imports/exports

### Error: Inconsistent code
**Solution**: Review project patterns and align

### Error: Missing documentation
**Solution**: Add comments and appropriate documentation
