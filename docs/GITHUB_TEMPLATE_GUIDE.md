# 📦 Guide: Using This Template on GitHub

This guide explains how to use this repository as a base template for new projects.

## 🎯 Purpose

This template is designed to be **downloaded/cloned before starting any project** to guarantee:
- ✅ Consistent and methodological development
- ✅ Better code quality from the start
- ✅ Clear protocols for any technology stack
- ✅ Professional results with simple prompts

## 🚀 Option 1: Use as GitHub Template

### Configure as Template

1. **In your GitHub repository:**
   - Go to Settings → General
   - Scroll to "Template repository"
   - Activate "Template repository"
   - Save changes

2. **Use the template:**
   - When creating a new repository, select "Use this template"
   - Or use: `https://github.com/your-username/claude-skills-template/generate`

### Advantages
- ✅ GitHub maintains the structure
- ✅ Easy to share with your team
- ✅ Clean history from the start

## 🔄 Option 2: Clone for Each Project

### Recommended Process

```bash
# 1. Clone the template
git clone https://github.com/your-username/claude-skills-template.git my-new-project
cd my-new-project

# 2. Configure
./setup.sh  # Linux/Mac
# Or
setup.bat   # Windows

# 3. Configure .env
# Edit .env and add your API key

# 4. Initialize as new project
rm -rf .git
git init
git add .
git commit -m "Initial commit: Skills template configured"

# 5. Add your project code
# Now you can start developing with skills active
```

## 📋 Project Startup Checklist

When starting a new project with this template:

### Phase 1: Initial Configuration
- [ ] Clone/download template
- [ ] Run `setup.sh` or `setup.bat`
- [ ] Configure `.env` with your API key
- [ ] Verify dependencies are installed
- [ ] Test with a simple example

### Phase 2: Customization
- [ ] Review skills and adjust according to your stack
- [ ] Customize methodologies if necessary
- [ ] Add domain-specific skills (optional)
- [ ] Configure your project structure

### Phase 3: Integration
- [ ] Load skills in your environment (Claude Desktop/API)
- [ ] Test with a real requirement
- [ ] Adjust according to results
- [ ] Document project-specific decisions

## 🎨 Customization by Project Type

### For React/TypeScript Projects

```bash
# After cloning template
npx create-react-app . --template typescript
# Or
npm create vite@latest . -- --template react-ts

# Skills are ready to use
```

### For Node.js/Express Projects

```bash
# After cloning template
npm init -y
npm install express
# ... other dependencies

# Skills work the same
```

### For Python Projects

```bash
# After cloning template
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt  # from template
# Add your own dependencies

# Skills are stack-independent
```

## 📁 Recommended Structure

After cloning, your project should look like this:

```
my-project/
├── skills/              # Template skills (keep)
├── examples/            # Examples (optional, you can delete)
├── outputs/             # Generated files (gitignored)
├── src/                 # Your project code
├── .env                 # Configuration (gitignored)
├── .env.example         # Configuration template
├── README.md            # Update with your project info
├── requirements.txt     # Python dependencies (if applicable)
└── ...                  # Your project files
```

## 🔧 Integration with Your Workflow

### With Claude Desktop

1. **Load skills:**
   - Open Claude Desktop
   - Settings → Skills
   - Add your project's `skills/` directory
   - Skills will be available automatically

2. **Use in development:**
   - Open Claude Desktop
   - Skills load automatically
   - Make your prompts normally
   - Skills guarantee consistency

### With Claude API

```python
# In your project code
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Skills are in the skills/ directory
# Load them according to INTEGRATION_GUIDE.md
```

### With Other AIs

See **docs/USAGE_WITH_OTHER_AI.md** to adapt to ChatGPT, Gemini, etc.

## 📝 Update Project README

After cloning, update README with:

```markdown
# My Project

[Description of your project]

## Development with Skills

This project uses the [Claude Skills Template](link-to-template) to guarantee consistent development.

Skills are in `skills/` and load automatically when working with Claude.

## Usage

[Your project-specific instructions]
```

## 🎯 Recommended Workflow

1. **Project start:**
   ```bash
   git clone template my-project
   cd my-project
   ./setup.sh
   # Configure .env
   ```

2. **During development:**
   - Use Claude with skills loaded
   - Make simple prompts, skills guarantee quality
   - Skills analyze, plan, and implement consistently

3. **Maintenance:**
   - Update skills according to best practices
   - Customize according to project needs
   - Share improvements with community

## 🔄 Update Template

If you improve the template:

1. **In template repository:**
   ```bash
   git add .
   git commit -m "feat: skill improvement"
   git push
   ```

2. **In existing projects:**
   ```bash
   # Option 1: Manual merge
   git remote add template https://github.com/your-username/claude-skills-template.git
   git fetch template
   git merge template/main --allow-unrelated-histories
   
   # Option 2: Copy changes manually
   # Copy only updated skills/
   ```

## 💡 Tips

### Keep Skills Updated
- Periodically review template improvements
- Update skills according to best practices
- Document specific customizations

### Share with Team
- Everyone uses the same template
- Consistency in methodology
- Easy onboarding of new members

### For Multiple Projects
- Keep template centralized
- Clone for each new project
- Customize according to specific needs

## 🚨 Important

### Don't Commit
- `.env` (contains API keys)
- `outputs/` (generated files)
- `venv/` or `node_modules/` (dependencies)

### Do Commit
- `skills/` (skills are part of the project)
- `.env.example` (template without secrets)
- Project configuration

## 📚 Additional Resources

- **GETTING_STARTED.md** - Quick start and setup
- **INTEGRATION_GUIDE.md** - Detailed integration
- **docs/USAGE_WITH_OTHER_AI.md** - Use with other AIs
- **docs/RESOURCES.md** - Resources and references

---

**Ready to start!** Clone the template and begin your project with guaranteed methodology and quality. 🚀
