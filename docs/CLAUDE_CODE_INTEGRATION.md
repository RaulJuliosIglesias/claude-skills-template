# 🔌 Integration with Claude Code (IDE)

This guide explains how to integrate this template with **Claude Code** (Anthropic's IDE) to enable **skill auto-activation** and other advanced features.

> **Reference**: This document is inspired by [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase), which solves the problem of skills not activating automatically.

## 🎯 What is Claude Code?

Claude Code is Anthropic's IDE that allows you to use Claude directly in your editor. One of its most powerful features is the **hooks** system that can activate skills automatically.

## 🚀 Problem It Solves

**Before**: Skills don't activate automatically - you have to remember which one to use.

**After**: Skills are suggested and activated automatically based on context.

## 📦 Required Components

### 1. Claude Code Hooks

Hooks are scripts that run at specific moments in Claude Code's workflow.

#### Essential Hook: Skill Auto-Activation

**Location**: `.claude/hooks/user-prompt-submit/`

This hook runs every time you submit a prompt and can suggest relevant skills.

### 2. skill-rules.json

File that maps patterns (keywords, file paths, etc.) to specific skills.

**Location**: `.claude/skill-rules.json`

## 🔧 Step-by-Step Configuration

### Step 1: Create Directory Structure

```bash
mkdir -p .claude/hooks/user-prompt-submit
mkdir -p .claude/skills
```

### Step 2: Copy Skills to Claude Code Directory

```bash
# Copy skills to .claude directory
cp -r skills/* .claude/skills/
```

### Step 3: Create skill-rules.json

Create `.claude/skill-rules.json`:

```json
{
  "rules": [
    {
      "skill": "project_protocol",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["develop", "implement", "create", "add", "new project", "development"]
        },
        {
          "type": "file_path",
          "patterns": ["**/src/**", "**/components/**", "**/services/**"]
        }
      ]
    },
    {
      "skill": "requirements_analyzer",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["need", "want", "require", "requirement", "functionality", "feature"]
        }
      ]
    },
    {
      "skill": "codebase_understanding",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["understand", "analyze", "review code", "existing code", "architecture"]
        },
        {
          "type": "file_path",
          "patterns": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.py"]
        }
      ]
    },
    {
      "skill": "implementation_protocol",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["implement", "code", "write", "create file", "modify"]
        },
        {
          "type": "file_path",
          "patterns": ["**/src/**", "**/components/**", "**/utils/**"]
        }
      ]
    }
  ]
}
```

### Step 4: Create Auto-Activation Hook

Create `.claude/hooks/user-prompt-submit/skill-activation-prompt.sh`:

```bash
#!/bin/bash

# Hook to auto-activate skills based on skill-rules.json
# Runs every time the user submits a prompt

SKILL_RULES_FILE=".claude/skill-rules.json"
USER_PROMPT="$1"

if [ ! -f "$SKILL_RULES_FILE" ]; then
    exit 0
fi

# Read skill-rules.json and search for matches
# This is a simplified example - in production you'd use jq or similar

# Extract keywords from prompt
PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

# Check each rule
while IFS= read -r line; do
    # Search for patterns in prompt
    # If there's a match, suggest the skill
    echo "💡 Suggested skill: [skill_name] based on your prompt"
done < <(cat "$SKILL_RULES_FILE" | jq -r '.rules[] | @json')

exit 0
```

**Note**: This is a basic example. For a complete implementation, consult [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase).

## 🎨 Progressive Disclosure Pattern

Large skills can exceed context limits. The reference repository uses a pattern of **500 lines maximum** per file.

### Modular Structure

```
skill_name/
├── SKILL.md              # <500 lines (overview + navigation)
└── resources/            # Additional files
    ├── routing.md        # <500 lines
    ├── controllers.md    # <500 lines
    ├── services.md       # <500 lines
    └── ...
```

### Example: Modify Our Skill

For `codebase_understanding`, you could structure it like this:

```
codebase_understanding/
├── SKILL.md              # Overview and navigation
└── resources/
    ├── structure-analysis.md
    ├── technology-identification.md
    ├── pattern-recognition.md
    └── code-location.md
```

## 🤖 Specialized Agents (Optional)

In addition to skills, you can create **agents** for specific complex tasks.

### Example: Architecture Review Agent

Create `.claude/agents/code-architecture-reviewer.md`:

```markdown
# Code Architecture Reviewer Agent

## Purpose
Review code for architectural consistency and best practices.

## When to Use
- After major refactoring
- Before merging large PRs
- When reviewing code structure

## Process
1. Analyze current architecture
2. Compare with project standards
3. Identify inconsistencies
4. Suggest improvements

## Output
- Architecture review report
- List of inconsistencies
- Recommendations
```

## 📝 Dev Docs Pattern

Documentation system that survives context resets.

### 3-File Structure

For each complex task, create:

1. `[task]-plan.md` - Strategic plan
2. `[task]-context.md` - Key decisions and files
3. `[task]-tasks.md` - Task checklist

**Location**: `.claude/dev-docs/` or `dev/active/`

## 🔗 Complete Integration

### Recommended Final Structure

```
project/
├── .claude/
│   ├── skills/              # Template skills
│   │   ├── project_protocol/
│   │   ├── requirements_analyzer/
│   │   ├── codebase_understanding/
│   │   └── implementation_protocol/
│   ├── hooks/
│   │   └── user-prompt-submit/
│   │       └── skill-activation-prompt.sh
│   ├── agents/              # Optional agents
│   ├── skill-rules.json     # Auto-activation rules
│   └── settings.json        # Claude Code configuration
└── skills/                   # Original skills (backup)
```

## 📚 Additional Resources

### Reference Repository

**[claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** - Complete implementation tested in production:

- ✅ Functional hooks for auto-activation
- ✅ Complete skill-rules.json
- ✅ Specialized agents
- ✅ Dev docs pattern
- ✅ Real usage examples

### Official Documentation

- [Claude Code Documentation](https://docs.anthropic.com/en/claude-code) - Official documentation
- [Claude Code Hooks](https://docs.anthropic.com/en/claude-code/hooks) - Hooks guide

## ⚠️ Important Notes

### Differences with Claude API

- **Claude Code** uses hooks and auto-activation
- **Claude API** requires manually loading skills
- This template works with both, but auto-activation only works in Claude Code

### Required Customization

- `skill-rules.json` must be customized according to your project
- Hooks may need adjustments according to your structure
- Agents are optional and domain-specific

## 🚀 Quick Start for Claude Code

1. **Copy skills to .claude/skills/**
2. **Create skill-rules.json** with your patterns
3. **Create basic hook** (or use the one from reference repository)
4. **Test** by sending a prompt - the skill should be suggested

## 💡 Tips

- Start simple: only basic auto-activation
- Iterate: add more rules as you see what works
- Use the reference repository as a guide
- Customize according to your workflow

---

**Need more details?** Consult the [reference repository](https://github.com/diet103/claude-code-infrastructure-showcase) for complete implementation tested in production.
