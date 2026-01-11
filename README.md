<div align="center">

# 🚀 Claude Skills Template

### **Consistent Development Framework for Any Project**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Claude Skills](https://img.shields.io/badge/Claude-Skills-FF6B35?logo=anthropic)](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
[![Template](https://img.shields.io/badge/GitHub-Template-181717?logo=github)](https://github.com)

**A complete Skills system that guarantees methodology, protocol, and consistency in any development project, regardless of technology stack.**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## ✨ Features

<div align="center">

| 🎯 **Methodology** | 🔧 **Flexibility** | 🚀 **Efficiency** | 📚 **Documentation** |
|:---:|:---:|:---:|:---:|
| 4-phase structured protocol | Works with any tech stack | Setup in 5 minutes | Complete guides & examples |
| Systematic requirements analysis | Compatible with multiple AIs | Auto-configuration scripts | Step-by-step tutorials |
| Codebase understanding | Adaptable to your workflow | Quick verification tools | Real-world examples |

</div>

### 🎯 What This Template Provides

- ✅ **Methodological Consistency** - Same process for every project
- ✅ **Clear Protocols** - Structured approach to development
- ✅ **Better Results** - Professional code with simple prompts
- ✅ **Complete Understanding** - Full analysis of current and future state
- ✅ **Best Practices** - Industry-standard implementation
- ✅ **Guaranteed Security Checks** - Mandatory security checklist (46+ items) for every implementation
- ✅ **Guaranteed Database Checks** - Mandatory database validation (RLS, transactions, constraints)
- ✅ **Guaranteed Quality Checks** - Mandatory QA checklist (testing, performance, documentation)
- ✅ **Technology-Agnostic** - Works with any technology stack through methodology
- ✅ **Multi-AI Support** - Claude, ChatGPT, Gemini, and more

---

## 📦 Included Skills

### 🎯 Core Skills System

<details>
<summary><b>1. 🎯 project_protocol</b> - Master Development Protocol</summary>

The orchestrator skill that coordinates the entire development process through 4 phases:
- **Requirements Analysis** → Understanding what's needed
- **Codebase Understanding** → Analyzing current state
- **Solution Planning** → Creating coherent implementation plan
- **Implementation** → Executing with quality standards

</details>

<details>
<summary><b>2. 📋 requirements_analyzer</b> - Structured Requirements Analysis</summary>

Systematically analyzes and structures user requirements:
- Main requirement extraction
- Functionality identification
- Constraint detection
- Dependency mapping
- Acceptance criteria definition
- Ambiguity resolution

</details>

<details>
<summary><b>3. 🔍 codebase_understanding</b> - Complete Codebase Analysis</summary>

Deep analysis of the current project state:
- Project structure mapping
- Technology stack identification
- Architecture pattern recognition
- Code patterns and conventions
- Relevant code location
- Configuration analysis

</details>

<details>
<summary><b>4. ⚙️ implementation_protocol</b> - Quality Implementation Guide</summary>

Ensures professional implementation:
- Respects existing architecture
- Follows project conventions
- Maintains code consistency
- **MANDATORY Security Checklist** (46+ security checks)
- **MANDATORY Database Checklist** (RLS, transactions, constraints)
- **MANDATORY Quality Assurance Checklist** (testing, performance, documentation)
- Complete documentation

**Guarantees**: Every implementation must pass security, database, and quality checks before completion.

</details>

---

## 🚀 Quick Start

### ⚡ 5-Minute Setup

```bash
# 1. Clone the template
git clone https://github.com/your-username/claude-skills-template.git my-project
cd my-project

# 2. Run automatic setup
./setup.sh        # Linux/Mac
# or
setup.bat         # Windows

# 3. Configure your API key
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-api03-...

# 4. Verify everything works
python test_skills.py

# 5. Start developing! 🎉
```

> 📖 **New to this?** Check out [GETTING_STARTED.md](GETTING_STARTED.md) for a detailed step-by-step guide.

### 🎨 Use as GitHub Template

1. Click **"Use this template"** on GitHub
2. Create your new repository
3. Follow the setup steps above

> 📚 See [docs/GITHUB_TEMPLATE_GUIDE.md](docs/GITHUB_TEMPLATE_GUIDE.md) for complete instructions.

---

## 📁 Project Structure

```
claude-skills-template/
├── 📁 skills/                      # Core Skills System
│   ├── project_protocol/          # Master orchestrator
│   ├── requirements_analyzer/    # Requirements analysis
│   ├── codebase_understanding/    # Codebase analysis
│   └── implementation_protocol/   # Implementation guide
│
├── 📁 examples/                    # Usage Examples
│   ├── usage_example.py           # Basic example
│   └── complete_example.py        # Advanced scenarios
│
├── 📁 .claude/                     # Claude Code IDE Config (Optional)
│   ├── skills/                    # Skills for auto-activation
│   ├── hooks/                     # Auto-activation hooks
│   └── skill-rules.json           # Pattern matching rules
│
├── ⚙️ Configuration Files
│   ├── .env.example               # Environment template
│   ├── requirements.txt           # Python dependencies
│   ├── setup.sh / setup.bat       # Auto-setup scripts
│   └── test_skills.py             # Verification tool
│
└── 📚 Documentation
    ├── GETTING_STARTED.md         # 🚀 Start here!
    ├── INTEGRATION_GUIDE.md       # Integration details
    └── docs/                       # Additional documentation
        ├── INDEX.md                # Complete file index
        └── ... (see docs/INDEX.md for complete list)
```

---

## 🎓 How It Works

<div align="center">

```mermaid
graph LR
    A[User Request] --> B[Requirements Analysis]
    B --> C[Codebase Understanding]
    C --> D[Solution Planning]
    D --> E[Implementation]
    E --> F[Quality Code]
    
    style A fill:#FF6B35
    style F fill:#4ECDC4
```

</div>

### 🔄 Development Workflow

1. **📋 Analysis Phase**
   - `requirements_analyzer` extracts and structures requirements
   - Identifies functionalities, constraints, and dependencies
   - Defines acceptance criteria

2. **🔍 Understanding Phase**
   - `codebase_understanding` analyzes current project state
   - Maps architecture, patterns, and technologies
   - Locates relevant existing code

3. **📐 Planning Phase**
   - `project_protocol` creates coherent implementation plan
   - Designs solution respecting existing architecture
   - Identifies components to create/modify

4. **⚙️ Implementation Phase**
   - `implementation_protocol` guides code writing
   - Follows project conventions and best practices
   - Ensures consistency and quality

---

## 📚 Documentation

### 🚀 Getting Started

| Document | Description | When to Use |
|:---------|:------------|:------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 🎯 **START HERE** - Complete first-use guide with setup checklist | First time using the template |

### 🔧 Integration Guides

| Document | Description | When to Use |
|:---------|:------------|:------------|
| **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** | Complete integration guide | Setting up skills |
| **[docs/CLAUDE_CODE_INTEGRATION.md](docs/CLAUDE_CODE_INTEGRATION.md)** | Claude Code IDE auto-activation | Using Claude Code IDE |
| **[docs/USAGE_WITH_OTHER_AI.md](docs/USAGE_WITH_OTHER_AI.md)** | Adapt for other AIs | Using ChatGPT, Gemini, etc. |

### 📖 Reference & Advanced

| Document | Description |
|:---------|:------------|
| **[docs/INDEX.md](docs/INDEX.md)** | Complete file index and navigation |
| **[docs/RESOURCES.md](docs/RESOURCES.md)** | Additional resources and references |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | How to contribute |
| **[docs/GITHUB_TEMPLATE_GUIDE.md](docs/GITHUB_TEMPLATE_GUIDE.md)** | Using as GitHub template |

> 📑 **Can't find what you need?** Check [docs/INDEX.md](docs/INDEX.md) for complete navigation.

---

## 💡 Usage Examples

### Example 1: Simple Feature

```python
from anthropic import Anthropic
from examples.usage_example import create_development_request

# Simple requirement
requirement = "Add a logout button to the header"

response = create_development_request(requirement)
# Skills automatically analyze, plan, and implement!
```

### Example 2: Complex Feature

```python
requirement = """
I need a complete authentication system with:
- Email/password login
- User registration
- Password recovery
- JWT session management
- Protected routes
"""

response = create_development_request(requirement, project_path="./my-project")
# Complete analysis and implementation plan generated!
```

> 📖 See [examples/](examples/) for complete working examples.

---

## 🌟 Key Benefits

<div align="center">

### 🎯 **For Developers**
- **Consistency** - Same methodology across all projects
- **Quality** - Best practices enforced automatically
- **Speed** - Faster development with structured approach
- **Confidence** - Clear protocols reduce errors

### 🏢 **For Teams**
- **Standardization** - Everyone follows the same process
- **Onboarding** - New members understand quickly
- **Collaboration** - Shared methodology improves teamwork
- **Scalability** - Works for projects of any size

### 🚀 **For Projects**
- **Quality from Day 1** - Best practices from the start
- **Maintainability** - Consistent code is easier to maintain
- **Documentation** - Everything is well documented
- **Flexibility** - Adapts to any technology stack

</div>

---

## 🔗 Resources & Community

### 📚 Official Resources

- [Claude Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) - Official guide
- [Claude Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices) - Best practices
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks) - Official examples

### 🌟 Community Resources

- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Curated skill collection
- [Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase) - Auto-activation patterns (8.3k⭐)

> 📖 See [docs/RESOURCES.md](docs/RESOURCES.md) for complete resource list.

---

## 🤝 Contributing

We welcome contributions! This template is designed to grow with the community.

### How to Contribute

- 🐛 **Report Issues** - Found a bug? Let us know!
- 📝 **Improve Documentation** - Help others understand better
- ✨ **Add Features** - New skills or improvements
- 💡 **Share Examples** - Real-world use cases
- 🌍 **Translate** - Help reach more developers

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Use Cases

<div align="center">

| Use Case | Description | Perfect For |
|:---------|:------------|:------------|
| 🆕 **New Projects** | Start with quality from day 1 | Fresh development |
| 🔄 **Refactoring** | Understand and improve existing code | Code maintenance |
| 🎯 **Feature Development** | Add features consistently | Product development |
| 👥 **Team Projects** | Standardize methodology | Team collaboration |
| 📚 **Learning** | Understand best practices | Education |
| 🚀 **Rapid Prototyping** | Fast, quality prototypes | MVP development |

</div>

---

## 🎯 Technology-Agnostic Methodology

<div align="center">

### ⚡ **How It Works**

This template uses a **methodology-first approach** that works with **any technology stack**. The skills don't require specific technology knowledge—they analyze what exists and adapt accordingly.

**What We Guarantee:**
- ✅ **Universal Methodology** - Same 4-phase process works everywhere
- ✅ **Automatic Detection** - Analyzes your existing stack automatically
- ✅ **Respect for Conventions** - Follows your project's patterns
- ✅ **Best Practices** - Applies industry standards to your stack
- ✅ **Mandatory Security Checks** - 46+ security checklist items enforced on every implementation
- ✅ **Mandatory Database Checks** - RLS, transactions, constraints validated when applicable
- ✅ **Mandatory Quality Checks** - Testing, performance, documentation validated

**What We Don't Guarantee:**
- ❌ Specific knowledge of every technology
- ❌ Pre-configured templates for each stack
- ❌ Technology-specific optimizations

**What We DO Guarantee:**
- ✅ **Security is never optional** - Every implementation must complete security checklist
- ✅ **Database best practices enforced** - RLS, transactions, validation required when applicable
- ✅ **Quality gates passed** - Testing, error handling, documentation required

</div>

### 🔍 How Technology Detection Works

The skills automatically:

1. **Analyze your project structure** - Understands your file organization
2. **Detect technologies** - Reads `package.json`, `requirements.txt`, etc.
3. **Identify patterns** - Recognizes naming conventions and architecture
4. **Adapt methodology** - Applies the protocol to your specific stack

### 📋 Common Technology Examples

The methodology has been tested with (but not limited to):

<div align="center">

#### Frontend
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![Vue](https://img.shields.io/badge/Vue-35495E?logo=vue.js&logoColor=4FC08D)
![Angular](https://img.shields.io/badge/Angular-DD0031?logo=angular&logoColor=white)
![Svelte](https://img.shields.io/badge/Svelte-FF3E00?logo=svelte&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)

#### Backend
![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?logo=express&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)

#### Databases
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)

#### AI Systems
![Claude](https://img.shields.io/badge/Claude-FF6B35?logo=anthropic)
![ChatGPT](https://img.shields.io/badge/ChatGPT-74AA9C?logo=openai)
![Gemini](https://img.shields.io/badge/Gemini-4285F4?logo=google)

</div>

> 💡 **Important**: These are examples of technologies the methodology has been used with. The skills work by **analyzing your project** and **adapting to what you have**, not by having pre-built knowledge of every technology.

### 🎯 The Key Difference

**Traditional approach**: "I know React, so I'll use React patterns"  
**This template**: "I see you're using React, so I'll analyze your React patterns and follow them"

The skills are **reactive** (they adapt to what exists) rather than **prescriptive** (they don't force specific technologies).

### ✅ What This Means for You

- **Works with any stack** - If you can describe it, the methodology applies
- **No technology lock-in** - Switch stacks? The methodology still works
- **Automatic adaptation** - Skills learn your conventions automatically
- **Future-proof** - New technologies? The methodology adapts

---

**Bottom line**: The template provides a **universal development methodology** that adapts to your technology stack, not a collection of technology-specific templates.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use in commercial projects
- ✅ Modify and adapt
- ✅ Distribute
- ✅ Private use

---

## ⭐ Show Your Support

If this template helps you, please consider:

- ⭐ **Starring** this repository
- 🍴 **Forking** for your own use
- 📢 **Sharing** with your team
- 🐛 **Reporting** issues
- 💡 **Suggesting** improvements

---

<div align="center">

## 🚀 Ready to Get Started?

**[📖 GETTING_STARTED.md](GETTING_STARTED.md)** • **[🔧 INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** • **[📦 Use Template](https://github.com/your-username/claude-skills-template/generate)**

---

**Made with ❤️ for the developer community**

[Report Bug](https://github.com/your-username/claude-skills-template/issues) • [Request Feature](https://github.com/your-username/claude-skills-template/issues) • [View Documentation](docs/INDEX.md)

</div>
