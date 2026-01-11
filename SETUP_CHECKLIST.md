# ✅ Setup Checklist

Quick checklist to verify the template is correctly configured.

> **💡 Tip**: Run `python test_skills.py` for automatic verification  
> **📖 Instructions**: Consult `QUICK_START.md` or `GETTING_STARTED.md` for details

## 📋 Pre-Installation

### Initial Checks
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Git installed (if cloning)
- [ ] Internet access to download dependencies
- [ ] Anthropic API key (or other AI provider)

## 🔧 Installation

### Step 1: Get Template
- [ ] Cloned or downloaded repository
- [ ] Navigated to project directory

### Step 2: Environment Setup
- [ ] Ran `setup.sh` (Linux/Mac) or `setup.bat` (Windows)
  - Or manually:
  - [ ] Created virtual environment (`python -m venv venv`)
  - [ ] Activated virtual environment
  - [ ] Installed dependencies (`pip install -r requirements.txt`)

### Step 3: API Configuration
- [ ] Copied `.env.example` to `.env`
- [ ] Edited `.env` and added `ANTHROPIC_API_KEY`
- [ ] Verified `.env` is in `.gitignore`

### Step 4: Verification
- [ ] Tested with basic example (`python examples/usage_example.py`)
- [ ] Verified skills are in `skills/`
- [ ] Created `outputs/` directory (if it doesn't exist)

## 📚 Documentation (Optional)

- [ ] Read `README.md` (overview)
- [ ] Reviewed `QUICK_START.md` or `INTEGRATION_GUIDE.md` as needed

## 🎯 Skills Configuration

### For Claude Desktop
- [ ] Claude Desktop installed
- [ ] Opened Settings → Skills
- [ ] Added `skills/` directory as source
- [ ] Verified skills appear

### For Claude API
- [ ] Reviewed `INTEGRATION_GUIDE.md`
- [ ] Tested skill loading in code
- [ ] Verified it works with example

### For Other AIs
- [ ] Reviewed `USAGE_WITH_OTHER_AI.md`
- [ ] Adapted according to AI system
- [ ] Tested with example

## 🧪 Tests

### Basic Tests
- [ ] Ran `examples/usage_example.py` successfully
- [ ] Verified Claude response is generated
- [ ] Reviewed that analysis follows protocol

### Advanced Tests
- [ ] Ran `examples/complete_example.py`
- [ ] Tested with real requirement from your project
- [ ] Verified skills work correctly

## 🎨 Customization (Optional)

### Basic Adjustments
- [ ] Reviewed skills in `skills/`
- [ ] Understood how they work
- [ ] Decided if you need to customize them

### Advanced Customization
- [ ] Edited `SKILL.md` of some skill as needed
- [ ] Added domain-specific skills (optional)
- [ ] Documented customizations

## 🚀 Ready to Use

### Final Verification
- [ ] Everything installed correctly
- [ ] API key configured
- [ ] Skills loaded and working
- [ ] Examples tested successfully
- [ ] Documentation read

### Next Steps
- [ ] Start using in your project
- [ ] Make first prompts with skills
- [ ] Iterate and adjust according to results

## ❓ Troubleshooting

If something doesn't work:

1. **API Key doesn't work**
   - Verify it's correct in `.env`
   - Verify it doesn't have extra spaces
   - Try regenerating key at console.anthropic.com

2. **Skills don't load**
   - Verify `SKILL.md` files exist
   - Verify YAML frontmatter format
   - Review `INTEGRATION_GUIDE.md`

3. **Dependencies don't install**
   - Verify Python 3.8+
   - Update pip: `pip install --upgrade pip`
   - Try reinstalling: `pip install -r requirements.txt --force-reinstall`

4. **Examples don't work**
   - Verify `.env` is configured
   - Verify virtual environment is activated
   - Review console errors

## 📞 Help

- Consult `QUICK_START.md` for detailed instructions
- Review `INTEGRATION_GUIDE.md` for integration problems
- Consult `RESOURCES.md` for additional resources

---

**✅ Everything ready?** Consult `QUICK_START.md` to begin. 🚀
