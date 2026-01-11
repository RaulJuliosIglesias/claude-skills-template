---
name: Project Management Protocol
description: |
  Master skill that guarantees a consistent and methodological development process.
  Orchestrates requirements analysis, codebase understanding, and implementation protocol
  to ensure professional results in any project. This skill ensures that each step
  of development follows a clear protocol: understand the user, analyze the current state,
  plan the solution, and implement following best practices.
version: 1.0.0
---

# Project Management Protocol Skill

## Purpose

This skill acts as the main orchestrator that ensures all development follows a consistent and methodological protocol, ensuring:

1. **Complete understanding** of the user's requirement
2. **Analysis of the current state** of the project
3. **Coherent planning** of the solution
4. **Professional implementation** following standards

## Methodology: 4-Phase Protocol

### Phase 1: Requirements Analysis
**Objective**: Completely understand what the user needs

**Process**:
1. Identify the main requirement
2. Extract functional and non-functional requirements
3. Identify constraints and dependencies
4. Validate understanding with the user if necessary
5. Document the requirement in a structured way

**Expected Output**:
- Main requirement clearly defined
- List of required functionalities
- Constraints identified
- Acceptance criteria

### Phase 2: Current State Understanding (Codebase Understanding)
**Objective**: Understand what currently exists in the project

**Process**:
1. Analyze the project structure
2. Identify technologies and frameworks used
3. Review existing architectural patterns
4. Identify related or similar code
5. Document the current state

**Expected Output**:
- Project architecture documented
- Technologies and dependencies identified
- Patterns and conventions used
- Relevant existing code identified

### Phase 3: Solution Planning
**Objective**: Create a coherent plan that respects the current state

**Process**:
1. Design solution that respects existing architecture
2. Identify components to create/modify
3. Plan integration with existing code
4. Define implementation order
5. Identify possible risks or considerations

**Expected Output**:
- Step-by-step implementation plan
- Components to create/modify
- Integration strategy
- Technical considerations

### Phase 4: Implementation
**Objective**: Execute the plan following best practices

**Process**:
1. Implement following the plan
2. Respect project conventions
3. Maintain consistency with existing code
4. Validate that it meets requirements
5. Document changes made

**Expected Output**:
- Implemented and functional code
- Consistent with existing project
- Appropriately documented
- Validated against requirements

## Golden Rules

1. **Never assume**: Always analyze the codebase before implementing
2. **Respect existing**: Maintain consistency with current patterns and conventions
3. **Validate understanding**: If there are doubts about the requirement, ask before implementing
4. **Document decisions**: Explain why a specific solution was chosen
5. **Iterate if necessary**: If the initial plan doesn't work, adjust and document

## Usage with Other Skills

This skill must work together with:
- `requirements_analyzer`: For deep requirements analysis
- `codebase_understanding`: For understanding the current state
- `implementation_protocol`: For implementation guidance

## Example Flow

```
User: "I need to add authentication to the project"

Phase 1 (Analysis):
- Requirement: Authentication system
- Functionalities: Login, registration, sessions
- Constraints: Must use JWT, compatible with React

Phase 2 (Understanding):
- Project uses React + TypeScript
- Route structure already exists
- No current auth system
- Uses Context API for state

Phase 3 (Planning):
- Create AuthContext
- Create Login/Register components
- Integrate with existing routes
- Use localStorage for tokens

Phase 4 (Implementation):
- Implement according to plan
- Follow project's React conventions
- Validate functionality
```

## Validation Checklist

Before considering a task complete, verify:

- [ ] Requirement completely understood
- [ ] Current project state analyzed
- [ ] Implementation plan created
- [ ] Solution respects existing architecture
- [ ] Code implemented and functional
- [ ] Consistent with project conventions
- [ ] Documentation updated if necessary
