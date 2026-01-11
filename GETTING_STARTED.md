# 🚀 Getting Started - Your First Use

Step-by-step guide to using the template for the first time.

## ⚡ Quick Start (5 minutes)

### Step 1: Download and Configure

```bash
# Clone or download the template
git clone https://github.com/your-username/claude-skills-template.git my-project
cd my-project

# Configure automatically
./setup.sh  # Linux/Mac
# Or
setup.bat   # Windows
```

### Step 2: Configure API Key

```bash
# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

Get your API key at: https://console.anthropic.com/

### Step 3: Verify It Works

```bash
# Run verification test
python test_skills.py
```

If you see "✅ Everything is working correctly", you're ready!

---

## ✅ Setup Checklist

Quick checklist to verify the template is correctly configured.

> **💡 Tip**: Run `python test_skills.py` for automatic verification

### 📋 Pre-Installation

**Initial Checks**
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Git installed (if cloning)
- [ ] Internet access to download dependencies
- [ ] Anthropic API key (or other AI provider)

### 🔧 Installation

**Step 1: Get Template**
- [ ] Cloned or downloaded repository
- [ ] Navigated to project directory

**Step 2: Environment Setup**
- [ ] Ran `setup.sh` (Linux/Mac) or `setup.bat` (Windows)
  - Or manually:
  - [ ] Created virtual environment (`python -m venv venv`)
  - [ ] Activated virtual environment
  - [ ] Installed dependencies (`pip install -r requirements.txt`)

**Step 3: API Configuration**
- [ ] Copied `.env.example` to `.env`
- [ ] Edited `.env` and added `ANTHROPIC_API_KEY`
- [ ] Verified `.env` is in `.gitignore`

**Step 4: Verification**
- [ ] Tested with basic example (`python examples/usage_example.py`)
- [ ] Verified skills are in `skills/`
- [ ] Created `outputs/` directory (if it doesn't exist)

### 🎯 Skills Configuration

**For Claude Desktop**
- [ ] Claude Desktop installed
- [ ] Opened Settings → Skills
- [ ] Added `skills/` directory as source
- [ ] Verified skills appear

**For Claude API**
- [ ] Reviewed `INTEGRATION_GUIDE.md`
- [ ] Tested skill loading in code
- [ ] Verified it works with example

**For Other AIs**
- [ ] Reviewed `docs/USAGE_WITH_OTHER_AI.md`
- [ ] Adapted according to AI system
- [ ] Tested with example

### 🚀 Ready to Use

**Final Verification**
- [ ] Everything installed correctly
- [ ] API key configured
- [ ] Skills loaded and working
- [ ] Examples tested successfully
- [ ] Documentation read

---

## 🎯 Your First Prompt with Skills

### Minimal Example (Copy and Paste)

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
        "content": "I need to add a logout button to the header"
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

print(response.content[0].text)
```

### Or Use the Helper

```python
# Use the included example
python examples/usage_example.py
```

---

## 💡 Tips for Better Results

### ✅ Do
- **Be specific**: Mention your technology stack
- **Provide context**: Share project structure if relevant
- **Mention constraints**: Versions, frameworks, conventions
- **Iterate**: Start simple, then add complexity

### ❌ Avoid
- Very vague prompts ("do something")
- Assuming Claude knows your complete project
- Skipping current state analysis
- Ignoring project conventions

### Examples of Effective Prompts

**✅ Good Prompt**
```
I need to add an authentication system to the React project that:
- Uses JWT for tokens
- Integrates with the existing AuthContext
- Follows the project's component structure
- Uses TypeScript like the rest of the code
```

**❌ Improvable Prompt**
```
Add login
```

---

## 🎯 Common Use Cases

### Case 1: New Project from Scratch

```python
# Suggested prompt
"I need to create a React project with TypeScript that includes:
- Authentication system
- Routing with React Router
- Global state with Context API
- Modular component structure"
```

### Case 2: Add Feature to Existing Project

```python
# Suggested prompt
"I need to add a comment system to the existing project.
The project uses React + TypeScript and already has authentication configured."
```

### Case 3: Refactor Code

```python
# Suggested prompt
"I need to refactor the authentication module to:
- Separate logic from UI
- Improve error handling
- Maintain compatibility with existing code"
```

---

## 🔧 Quick Customization

### Adjust Skills for Your Stack

1. **Edit skills/[skill_name]/SKILL.md**
2. **Add examples specific to your stack**
3. **Adjust methodology if necessary**

### Add Custom Skills

1. **Create skills/my_skill/SKILL.md**
2. **Follow the format of existing skills**
3. **Add to your skills list when using**

---

## 📖 Recommended Learning Flow

### Day 1: Setup (15 min)
1. ✅ Run setup
2. ✅ Configure .env
3. ✅ Run test_skills.py
4. ✅ Read README.md

### Day 2: First Use (30 min)
1. ✅ Run examples/usage_example.py
2. ✅ Make your first real prompt
3. ✅ Understand the skills workflow

### Day 3: Deep Dive (1 hour)
1. ✅ Read skills/README.md
2. ✅ Review INTEGRATION_GUIDE.md
3. ✅ Customize for your stack
4. ✅ Create your first complex prompt

### Day 4+: Optimization
1. ✅ Review docs/RESOURCES.md
2. ✅ Explore docs/CLAUDE_CODE_INTEGRATION.md (if using Claude Code IDE)
3. ✅ Customize skills according to your needs
4. ✅ Share improvements with the community

---

## 📚 Next Steps

- **INTEGRATION_GUIDE.md** - Advanced integration
- **skills/README.md** - Understand each skill
- **docs/RESOURCES.md** - Additional resources
- **docs/INDEX.md** - Complete file index

---

## ❓ Troubleshooting

### API Key doesn't work
- Verify it's correct in `.env`
- Verify it doesn't have extra spaces
- Try regenerating key at console.anthropic.com

### Skills don't load
- Verify `SKILL.md` files exist
- Verify YAML frontmatter format
- Review `INTEGRATION_GUIDE.md`

### Dependencies don't install
- Verify Python 3.8+
- Update pip: `pip install --upgrade pip`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

### Examples don't work
- Verify `.env` is configured
- Verify virtual environment is activated
- Review console errors

---

**Ready to start!** 🚀

Run `python test_skills.py` to verify everything works, then make your first prompt.
