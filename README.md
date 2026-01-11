# Claude Skills Template - Consistent Development Framework

A complete Skills system for Claude that guarantees methodology, protocol, and consistency in **any development project**, regardless of the technology stack.

## 🎯 Objective

This template provides a set of Skills that ensure:
- ✅ **Methodological consistency** across all projects
- ✅ **Clear protocols** for understanding and developing
- ✅ **Better results** with simple prompts
- ✅ **Complete understanding** of the current and future project state
- ✅ **Professional implementation** following best practices
- ✅ **Compatible with any stack** (React, Vue, Angular, Node.js, Python, etc.)
- ✅ **Works with multiple AIs** (Claude, ChatGPT, Gemini, etc.)

## 📦 Included Skills

### 1. **project_protocol** - Main Project Protocol
Master skill that orchestrates the entire development process, ensuring each step is followed correctly.

### 2. **requirements_analyzer** - Requirements Analyzer
Analyzes and structures user requirements, identifying:
- What the user wants
- Why they need it
- How it should work
- What constraints exist

### 3. **codebase_understanding** - Codebase Understanding
Analyzes the current project state:
- What currently exists
- Architecture and patterns used
- Dependencies and technologies
- File structure

### 4. **implementation_protocol** - Implementation Protocol
Guides implementation following:
- Project best practices
- Consistency with existing code
- Testing and validation
- Documentation

## 🚀 Quick Start

### Option 1: Use as GitHub Template
```bash
# Create new repository from template
# Or clone directly
git clone https://github.com/your-username/claude-skills-template.git my-project
cd my-project
./setup.sh  # Linux/Mac
# Or setup.bat on Windows
```

### Option 2: Manual Installation
```bash
# 1. Clone or download
git clone https://github.com/your-username/claude-skills-template.git
cd claude-skills-template

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

See **QUICK_START.md** for more details.

## 📁 Project Structure

```
claude-skills-template/
├── skills/                    # Template skills
│   ├── project_protocol/
│   ├── requirements_analyzer/
│   ├── codebase_understanding/
│   └── implementation_protocol/
├── examples/                  # Usage examples
├── outputs/                   # Generated files (gitignored)
├── .env.example              # Configuration template
├── requirements.txt          # Python dependencies
├── setup.sh / setup.bat      # Automatic setup scripts
├── .claude/                  # Claude Code IDE configuration (optional)
└── README.md                 # This file
```

## 🔧 Complete Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Step 3: Load the Skills
Follow the guide in **INTEGRATION_GUIDE.md** to load the skills in your environment.

### Step 4: Verify Configuration
```bash
python test_skills.py
```

### Step 5: Start Developing!
Review **GETTING_STARTED.md** for your first use or **QUICK_START.md** for more examples.

## 📚 Documentation

### Main Documentation
- **README.md** (this file) - Template overview
- **GETTING_STARTED.md** - 🚀 **START HERE** - Your first use step by step
- **QUICK_START.md** - Quick configuration and startup guide
- **INTEGRATION_GUIDE.md** - Detailed integration guide
- **CLAUDE_CODE_INTEGRATION.md** - Claude Code IDE integration (auto-activation)
- **GITHUB_TEMPLATE_GUIDE.md** - How to use as GitHub template
- **USAGE_WITH_OTHER_AI.md** - Adaptation for other AI systems
- **RESOURCES.md** - Additional resources and references
- **INDEX.md** - Complete file index

### Skills Documentation
Each skill includes complete documentation in its `SKILL.md` explaining:
- Purpose and scope
- Methodology it applies
- Usage examples
- Best practices

See `skills/README.md` for detailed documentation of each skill.

### Examples
- **examples/usage_example.py** - Basic usage example
- **examples/complete_example.py** - Complete example with use cases

## 🎓 Workflow

1. **Analysis**: `requirements_analyzer` understands what the user needs
2. **Understanding**: `codebase_understanding` analyzes the current state
3. **Planning**: `project_protocol` creates a coherent plan
4. **Implementation**: `implementation_protocol` executes following standards

## 🌟 Resources and References

### Official Claude Skills Resources
- [Claude Skills Quickstart](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) - Official getting started guide
- [Claude Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices) - Official best practices
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks) - Official examples and guides
- [How to Create Custom Skills](https://support.claude.com/en/articles/12599426-how-to-create-a-skill-with-claude-through-conversation) - Creation guide

### Community Resources
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Curated collection of community skills
- [Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase) - Auto-activation of skills with hooks (8.3k⭐)
- [Claude Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) - Complete documentation

### Articles and Tutorials
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Technical article on Skills
- [Teach Claude Your Way of Working](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills) - Customization guide

## 🤝 Contributing

This template is designed to be adapted to your specific needs. Modify the skills according to your preferred methodology.

**Want to contribute?** Review [CONTRIBUTING.md](CONTRIBUTING.md) to see how you can help:
- Improve documentation
- Add new skills
- Share usage examples
- Report issues or suggest improvements

## 📄 License

MIT License - Use freely in your projects.

## 🎯 Use Cases

This template is perfect for:
- ✅ **Starting new projects** - Guarantees quality from day 1
- ✅ **Development teams** - Methodological consistency
- ✅ **Multiple stacks** - Works with React, Vue, Node.js, Python, etc.
- ✅ **Different AIs** - Adaptable to Claude, ChatGPT, Gemini, etc.
- ✅ **Complex projects** - Structured methodology for any size
- ✅ **Claude Code IDE** - Auto-activation of skills with hooks (see CLAUDE_CODE_INTEGRATION.md)

---

**Ready to start?** 
1. 🚀 **GETTING_STARTED.md** - Your first use (recommended)
2. ⚡ **QUICK_START.md** - Quick configuration
3. 📦 **GITHUB_TEMPLATE_GUIDE.md** - Use as template
