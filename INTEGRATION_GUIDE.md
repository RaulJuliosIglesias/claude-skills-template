# 📘 Integration Guide - Skills Template

## How to Load Skills in Claude

### Method 1: Custom Skills

To use these skills as custom skills, you need:

1. **Skills Structure**: Each skill must be in its own directory with `SKILL.md`
2. **Load in Claude**: Depending on your environment, there are different ways

#### In Claude Desktop

1. Open Claude Desktop
2. Go to Settings → Skills
3. Add the `skills/` directory as a skills source
4. Skills should appear automatically

#### In Claude API (Beta)

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# For custom skills, you need to load them first
# This requires skills to be in a format that Claude can access
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    container={
        "skills": [
            {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
            # ... other skills
        ]
    },
    # ...
)
```

### Method 2: Use as Reference in Prompts

If you can't load skills directly, you can use their content as context in your prompts:

```python
# Read skill content
from pathlib import Path

def load_skill_content(skill_name):
    skill_path = Path(f"skills/{skill_name}/SKILL.md")
    return skill_path.read_text()

# Use in prompt
skill_content = load_skill_content("project_protocol")

messages = [{
    "role": "user",
    "content": f"""
{skill_content}

Now, following this protocol, analyze and develop: [your requirement]
"""
}]
```

## Skills Structure

Each skill follows this structure:

```
skill_name/
├── SKILL.md          # Main skill documentation
└── scripts/          # Helper scripts (optional)
    └── helper.py
```

### SKILL.md - Format

Each `SKILL.md` must have:

1. **YAML Frontmatter**: Skill metadata
2. **Documentation**: Detailed instructions for Claude
3. **Methodology**: How the skill should work
4. **Examples**: Use cases

## Workflow with Skills

### Step 1: Initial Analysis

When the user makes a request:

1. **requirements_analyzer** analyzes what the user needs
2. **codebase_understanding** analyzes the current state
3. **project_protocol** orchestrates the process

### Step 2: Planning

1. **project_protocol** creates a plan based on:
   - Analyzed requirements
   - Current project state
   - Best practices

### Step 3: Implementation

1. **implementation_protocol** guides implementation
2. Follows project conventions
3. Respects existing architecture

## Skills Customization

### Modify an Existing Skill

1. Edit the skill's `SKILL.md` file
2. Adjust methodology according to your needs
3. Add examples specific to your domain

### Create a New Skill

1. Create a new directory in `skills/`
2. Create `SKILL.md` with the correct format
3. Add helper scripts if necessary
4. Document its purpose and usage

### Example: Custom Skill

```markdown
---
name: My Custom Skill
description: |
  Description of what your custom skill does.
version: 1.0.0
---

# My Custom Skill

## Purpose
[Detailed description]

## Methodology
[How it works]

## Usage
[Examples]
```

## Best Practices

### 1. Use All Skills Together

For best results, load all template skills:

```python
skills = [
    {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
    {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
    {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
    {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
]
```

### 2. Provide Project Context

Include information about your project in the prompt:

```python
messages = [{
    "role": "user",
    "content": f"""
Project: {project_name}
Stack: {tech_stack}
Structure: {project_structure}

Requirement: {user_requirement}
"""
}]
```

### 3. Iterate and Refine

Skills improve with use. If something doesn't work as expected:
- Review the skill documentation
- Adjust prompts
- Customize skills according to your needs

## Troubleshooting

### Skills Don't Load

- Verify that `SKILL.md` files have the correct format
- Make sure YAML frontmatter is well formatted
- Check that paths are correct

### Results Are Not Consistent

- Make sure to load all skills
- Provide sufficient project context
- Use clear and specific prompts

### Implementation Doesn't Respect Project

- Verify that `codebase_understanding` has access to code
- Provide more context about architecture
- Review that conventions are documented

## Additional Resources

- [Anthropic Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Skills Examples](https://github.com/anthropics/claude-cookbooks)

## Next Step

1. Review each individual skill in `skills/`
2. Customize according to your needs
3. Test with a real project
4. Iterate and improve
