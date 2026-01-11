# 📁 .claude Directory

This directory contains configuration for **Claude Code IDE** (Anthropic's IDE).

## 🎯 What is this?

Claude Code allows using hooks and skill auto-activation. This directory contains the necessary configuration.

## 📦 Content

### skills/
Copy of template skills for use in Claude Code.

### hooks/
Hooks that run at specific moments in the workflow.

### skill-rules.json
File that maps patterns (keywords, file paths) to skills for auto-activation.

## 🚀 Quick Setup

1. **Copy skills:**
   ```bash
   cp -r skills/* .claude/skills/
   ```

2. **Configure skill-rules.json:**
   ```bash
   cp .claude/skill-rules.json.example .claude/skill-rules.json
   # Edit according to your needs
   ```

3. **Create hooks (optional):**
   See `CLAUDE_CODE_INTEGRATION.md` for details.

## 📚 Documentation

- **CLAUDE_CODE_INTEGRATION.md** - Complete integration guide
- **[claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** - Complete reference

## ⚠️ Note

This directory is **optional**. Only necessary if you use **Claude Code IDE**.

For use with Claude API or other AIs, the skills in `skills/` are sufficient.
