# 🚀 Quick Start Guide

## Quick Configuration

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 3. Load Skills in Your Project

Skills must be in an accessible directory. You have two options:

#### Option A: Local Skills (Recommended for development)

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Skills must be in a directory that Claude can access
# For now, use Anthropic's skills or create your own following the structure
```

#### Option B: Use with Claude Desktop/Claude.ai

If you're using Claude Desktop or Claude.ai, you can load skills directly from the `skills/` directory.

## Basic Usage

### Minimal Example

```python
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
            {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
            {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
            {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "I need to add authentication to the project"
    }],
    betas=[
        "code-execution-2025-08-25",
        "files-api-2025-04-14",
        "skills-2025-10-02"
    ]
)

print(response.content[0].text)
```

## Recommended Workflow

1. **Define your requirement** clearly
2. **Execute the query** with all skills loaded
3. **Review the analysis** that Claude provides:
   - Requirements analysis
   - Current project state
   - Implementation plan
4. **Implement** following the proposed plan
5. **Validate** that it meets the requirements

## Tips for Better Results

### ✅ Do

- **Be specific**: Mention important details
- **Provide context**: If there's relevant code, share it
- **Mention constraints**: Technologies, frameworks, versions
- **Be clear about priorities**: What's most important

### ❌ Avoid

- Very vague requirements without context
- Assuming Claude knows your complete project
- Skipping current state analysis
- Ignoring project conventions

## Examples of Effective Prompts

### ✅ Good Prompt

```
I need to add an authentication system to the React project that:
- Uses JWT for tokens
- Integrates with the existing AuthContext
- Follows the project's component structure
- Uses TypeScript like the rest of the code
```

### ❌ Improvable Prompt

```
Add login
```

## Customization

You can customize skills by editing the `SKILL.md` files in each directory:

- `skills/project_protocol/SKILL.md` - Adjust the main protocol
- `skills/requirements_analyzer/SKILL.md` - Customize requirements analysis
- `skills/codebase_understanding/SKILL.md` - Adjust how code is analyzed
- `skills/implementation_protocol/SKILL.md` - Customize implementation protocol

## Next Step

Read the complete `README.md` to better understand how each skill works and how to customize them for your needs.
