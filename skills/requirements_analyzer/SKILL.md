---
name: Requirements Analysis Protocol
description: |
  Systematically analyzes and structures user requirements. Identifies functionalities,
  constraints, dependencies, and acceptance criteria. Guarantees complete understanding before
  any implementation, avoiding misunderstandings and ensuring the solution exactly meets
  what the user needs.
version: 1.0.0
---

# Requirements Analysis Protocol Skill

## Purpose

This skill ensures that all user requirements are analyzed systematically and completely before any implementation, ensuring:

1. **Precise understanding** of what the user needs
2. **Complete identification** of required functionalities
3. **Early detection** of ambiguities or inconsistencies
4. **Structured documentation** of requirements

## Methodology: Structured Analysis

### Step 1: Main Requirement Extraction

**Objective**: Identify the user's central goal

**Process**:
- Read the user's complete message
- Identify the main action verb (create, modify, add, delete, etc.)
- Extract the main object (what to create/modify)
- Formulate the main requirement in a clear sentence

**Output**:
```
Main Requirement: [Action] + [Object] + [Context]
Example: "Add JWT authentication system to React project"
```

### Step 2: Functionality Identification

**Objective**: List all necessary functionalities

**Process**:
- Break down the main requirement into specific functionalities
- Identify explicitly mentioned functionalities
- Infer implicitly necessary functionalities
- Organize by priority or dependencies

**Output**:
```
Functionalities:
1. [Main functionality]
2. [Secondary functionality]
3. [Support functionality]
...
```

### Step 3: Constraint Identification

**Objective**: Detect limitations and technical requirements

**Process**:
- Identify mentioned or required technologies
- Detect design or UX constraints
- Identify performance limitations
- Note security or privacy constraints
- Identify compatibility constraints

**Output**:
```
Constraints:
- Technological: [frameworks, libraries, versions]
- Design: [UI/UX requirements]
- Performance: [performance requirements]
- Security: [security requirements]
- Compatibility: [browser, platform requirements]
```

### Step 4: Dependency Identification

**Objective**: Recognize relationships with other components

**Process**:
- Identify existing components that will be used
- Detect new necessary dependencies
- Identify required external services
- Note data or API dependencies

**Output**:
```
Dependencies:
- Internal: [project components]
- External: [libraries, services]
- APIs: [endpoints, services]
- Data: [data structures, models]
```

### Step 5: Acceptance Criteria Definition

**Objective**: Establish how to validate that the solution is correct

**Process**:
- Define main use cases
- Identify success scenarios
- Detect edge cases or limits
- Establish validation metrics

**Output**:
```
Acceptance Criteria:
1. [Specific and measurable criterion]
2. [Specific and measurable criterion]
...
```

### Step 6: Ambiguity Detection

**Objective**: Identify points that need clarification

**Process**:
- Review requirement for vague terms
- Identify unspecified implementation options
- Detect possible different interpretations
- List questions to clarify

**Output**:
```
Detected Ambiguities:
- [Ambiguous point] → Suggested question: [¿...?]
...
```

## Analysis Template

Use this template to structure the analysis:

```markdown
## Requirements Analysis

### Main Requirement
[Clear and concise description]

### Required Functionalities
1. [Functionality 1]
2. [Functionality 2]
...

### Constraints
- Technological: ...
- Design: ...
- Performance: ...
- Security: ...

### Dependencies
- Internal: ...
- External: ...
- APIs: ...
- Data: ...

### Acceptance Criteria
1. [Criterion 1]
2. [Criterion 2]
...

### Ambiguities (if any)
- [Ambiguity] → ¿[Question]?
```

## Analysis Rules

1. **Don't assume**: If something is unclear, ask
2. **Be exhaustive**: Analyze all aspects of the requirement
3. **Be specific**: Avoid generalities, be concrete
4. **Validate understanding**: Confirm understanding before proceeding
5. **Document everything**: Record all decisions and reasoning

## Examples

### Example 1: Simple Requirement

**User**: "Add a logout button"

**Analysis**:
- Main Requirement: Add logout functionality to the system
- Functionalities: UI button, logout function, session cleanup
- Constraints: Must be in header, consistent style
- Dependencies: Existing authentication system
- Criteria: On click, user is logged out and redirected

### Example 2: Complex Requirement

**User**: "I need a dashboard with monthly sales charts"

**Analysis**:
- Main Requirement: Create dashboard with sales data visualization
- Functionalities: Dashboard UI, monthly charts, date filters, data loading
- Constraints: Must be responsive, use compatible chart library
- Dependencies: Sales API, chart library, authentication system
- Criteria: Shows correct data, interactive charts, fast loading
- Ambiguities: What type of chart? → Ask preference

## Integration with Other Skills

This skill feeds:
- `project_protocol`: Provides structured requirements
- `codebase_understanding`: Identifies what to look for in code
- `implementation_protocol`: Defines what to implement

## Validation Checklist

Before considering the analysis complete:

- [ ] Main requirement clearly identified
- [ ] All functionalities listed
- [ ] Constraints identified
- [ ] Dependencies mapped
- [ ] Acceptance criteria defined
- [ ] Ambiguities identified and resolved (or asked)
- [ ] Analysis documented in structured way
