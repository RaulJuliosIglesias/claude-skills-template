# Template Skills - Documentation

This directory contains the 4 main skills of the template that guarantee consistent and methodological development.

## 📦 Included Skills

### 1. `project_protocol/` - Main Protocol

**Purpose**: Orchestrate the entire development process following a consistent protocol.

**When to use**: Always. This is the master skill that coordinates the others.

**Methodology**: 4-phase protocol:
- Requirements Analysis
- Current State Understanding
- Solution Planning
- Implementation

### 2. `requirements_analyzer/` - Requirements Analyzer

**Purpose**: Systematically analyze and structure user requirements.

**When to use**: At the start of any task to completely understand what the user needs.

**Methodology**: Structured analysis in 6 steps:
1. Main requirement extraction
2. Functionality identification
3. Constraint identification
4. Dependency identification
5. Acceptance criteria definition
6. Ambiguity detection

### 3. `codebase_understanding/` - Codebase Understanding

**Purpose**: Systematically analyze the current project state.

**When to use**: Before implementing any change to respect existing architecture.

**Methodology**: Systematic analysis in 6 steps:
1. Project structure analysis
2. Technology identification
3. Architecture analysis
4. Pattern and convention identification
5. Relevant code location
6. Dependencies and configuration analysis

### 4. `implementation_protocol/` - Implementation Protocol

**Purpose**: Guide implementation following best practices and respecting the project.

**When to use**: During the implementation phase to ensure quality and consistency.

**Methodology**: Implementation protocol in 6 phases:
1. Preparation
2. Solution design
3. Implementation
4. Integration
5. Validation
6. Documentation

## 🔄 Workflow

```
User makes request
    ↓
project_protocol orchestrates
    ↓
requirements_analyzer → Analyzes what is needed
    ↓
codebase_understanding → Analyzes current state
    ↓
project_protocol → Creates coherent plan
    ↓
implementation_protocol → Implements following standards
    ↓
Result: Consistent and professional code
```

## 📝 Each Skill Structure

Each skill follows this structure:

```
skill_name/
├── SKILL.md          # Main documentation (required)
└── scripts/          # Helper scripts (optional)
    └── helper.py
```

### SKILL.md

Each `SKILL.md` contains:
- **YAML Frontmatter**: Metadata (name, description, version)
- **Purpose**: What the skill does
- **Methodology**: How it works
- **Rules**: Principles to follow
- **Examples**: Use cases
- **Checklist**: Completeness validation

### Scripts

Scripts in `scripts/` are helper tools that Claude can use, but are not required. They include:
- Parsers to structure information
- Validators to verify completeness
- Report generators

## 🎯 Recommended Usage

### Load All Skills

For best results, load all skills together:

```python
skills = [
    {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
    {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
    {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
    {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
]
```

### Priority Order

If you can only load some skills, prioritize in this order:
1. `project_protocol` - Essential for orchestration
2. `requirements_analyzer` - Critical to understand the user
3. `codebase_understanding` - Important to respect the project
4. `implementation_protocol` - Useful to guide implementation

## 🔧 Customization

Each skill can be customized by editing its `SKILL.md`:

1. **Adjust methodology**: Modify steps according to your needs
2. **Add examples**: Include examples specific to your domain
3. **Modify rules**: Adjust rules according to your standards
4. **Extend checklists**: Add additional validations

## 📚 Resources

- See `INTEGRATION_GUIDE.md` for how to load skills
- See `QUICK_START.md` for quick start
- See main `README.md` for overview

## 🤝 Contributing

If you improve a skill:
1. Document the changes
2. Update examples if necessary
3. Maintain compatibility with other skills
4. Update this documentation
