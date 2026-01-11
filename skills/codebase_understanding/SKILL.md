---
name: Codebase Understanding Protocol
description: |
  Systematically analyzes the current project state to understand architecture, technologies,
  patterns, and conventions. Ensures that any implementation respects and correctly integrates
  with existing code, maintaining project consistency and quality.
version: 1.0.0
---

# Codebase Understanding Protocol Skill

## Purpose

This skill ensures complete understanding of the current project state before any implementation, ensuring:

1. **Knowledge of current architecture**
2. **Identification of technologies** and frameworks used
3. **Recognition of patterns** and conventions
4. **Location of relevant existing code**
5. **Respect for project structure** and organization

## Methodology: Systematic Analysis

### Step 1: Project Structure Analysis

**Objective**: Understand file and directory organization

**Process**:
1. Examine root directory structure
2. Identify main directories (src, components, utils, etc.)
3. Recognize organization patterns
4. Map folder structure

**Output**:
```
Project Structure:
├── [main directory]
│   ├── [subdirectory]
│   └── ...
├── [main directory]
└── ...

Identified Patterns:
- Organization by: [feature/type/layer]
- Naming conventions: [camelCase/PascalCase/kebab-case]
```

### Step 2: Technology Identification

**Objective**: List all technologies, frameworks, and libraries **that exist in the project**

**Important**: This skill **detects** technologies, it does **not** require pre-existing knowledge of them. It analyzes what exists and adapts.

**Process**:
1. Review package.json / requirements.txt / pom.xml / Cargo.toml / etc.
2. Identify main framework (React, Vue, Angular, etc.) **from dependencies**
3. List main libraries **from dependency files**
4. Identify build tools **from configuration files**
5. Recognize testing systems **from test files or config**

**Output**:
```
Technology Stack:
- Framework: [Detected from package.json/dependencies]
- Language: [Detected from file extensions/config]
- Build Tool: [Detected from config files]
- Testing: [Detected from test files/config]
- Main libraries:
  * [library 1] - [from dependencies]
  * [library 2] - [from dependencies]
  ...
```

**Note**: If a technology is not detected automatically, it will be identified during code analysis when patterns are recognized.

### Step 3: Architecture Analysis

**Objective**: Understand how the code is structured

**Process**:
1. Identify architectural pattern (MVC, Component-based, etc.)
2. Recognize main layers or modules
3. Identify data flow
4. Recognize state system (Redux, Context, etc.)
5. Identify routing system

**Output**:
```
Architecture:
- Pattern: [MVC/Component-based/etc.]
- Main layers:
  * [Layer 1]: [responsibility]
  * [Layer 2]: [responsibility]
- State management: [Redux/Context/Zustand/etc.]
- Routing: [React Router/Vue Router/etc.]
- Data flow: [description]
```

### Step 4: Pattern and Convention Identification

**Objective**: Recognize code patterns and conventions used

**Process**:
1. Analyze existing code examples
2. Identify design patterns used
3. Recognize naming conventions
4. Identify code styles (ESLint, Prettier configs)
5. Recognize component/function patterns

**Output**:
```
Patterns and Conventions:
- Nomenclature:
  * Components: [PascalCase/camelCase]
  * Functions: [camelCase]
  * Files: [convention]
- Design patterns:
  * [Pattern 1]: used in [context]
  * [Pattern 2]: used in [context]
- Code style: [ESLint/Prettier configuration]
- Component structure: [description]
```

### Step 5: Relevant Code Location

**Objective**: Find existing code related to the requirement

**Process**:
1. Search for similar components/functions
2. Identify code to reuse
3. Locate code that needs modification
4. Identify related services/APIs
5. Find relevant existing utilities

**Output**:
```
Relevant Code:
- Similar components:
  * [path/component] - [purpose]
- Functions/Utilities:
  * [path/function] - [purpose]
- Services/APIs:
  * [path/service] - [purpose]
- Code to modify:
  * [path/file] - [reason]
```

### Step 6: Dependencies and Configuration Analysis

**Objective**: Understand project configuration and dependencies

**Process**:
1. Review configuration files
2. Identify environment variables
3. Recognize build configuration
4. Identify available scripts
5. Review tool configuration

**Output**:
```
Configuration:
- Environment variables: [list]
- Available scripts: [npm/yarn scripts]
- Build configuration: [details]
- Configured tools: [ESLint, Prettier, etc.]
```

## Analysis Template

Use this template to document the analysis:

```markdown
## Current Project State Analysis

### Project Structure
[Organization description]

### Technology Stack
- Framework: ...
- Language: ...
- Main libraries: ...

### Architecture
- Pattern: ...
- Layers: ...
- State management: ...

### Patterns and Conventions
- Nomenclature: ...
- Design patterns: ...
- Code style: ...

### Relevant Code
- Similar components: ...
- Utilities: ...
- Code to modify: ...

### Configuration
- Environment variables: ...
- Scripts: ...
```

## Analysis Rules

1. **Be exhaustive**: Don't assume, verify in code
2. **Look for patterns**: Identify how things are done in the project
3. **Respect conventions**: Follow existing patterns
4. **Document findings**: Record everything found
5. **Identify reusable code**: Don't reinvent the wheel

## Search Strategies

### To find similar code:
- Search by related keywords
- Review related directories
- Search for similar imports/exports
- Review tests to understand usage

### To understand architecture:
- Review main configuration files
- Analyze import structure
- Review entry files (index.js, main.js, App.js)
- Examine main component structure

### To identify patterns:
- Review multiple code examples
- Look for repeated patterns
- Analyze naming conventions
- Review tool configuration

## Examples

### Example 1: React Project

**Analysis**:
- Structure: src/components, src/utils, src/services
- Stack: React 18, TypeScript, Vite
- Architecture: Component-based, Context API for state
- Patterns: Functional components, hooks, custom hooks
- Conventions: PascalCase for components, camelCase for functions

### Example 2: Project with Backend

**Analysis**:
- Structure: frontend/, backend/, shared/
- Stack: React frontend, Node.js backend, PostgreSQL
- Architecture: Frontend/backend separation, REST API
- Patterns: MVC in backend, Component-based in frontend
- Conventions: kebab-case for files, camelCase for code

## Integration with Other Skills

This skill feeds:
- `project_protocol`: Provides current state context
- `requirements_analyzer`: Identifies what to look for in code
- `implementation_protocol`: Defines how to implement respecting existing code

## Validation Checklist

Before considering the analysis complete:

- [ ] Project structure mapped
- [ ] Technology stack identified
- [ ] Architecture understood
- [ ] Patterns and conventions recognized
- [ ] Relevant code located
- [ ] Configuration reviewed
- [ ] Analysis documented
