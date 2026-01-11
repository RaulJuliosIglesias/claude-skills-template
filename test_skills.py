"""
Quick verification script to validate that the template is correctly configured
"""

import os
import sys
from pathlib import Path

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

def print_success(message):
    print(f"{GREEN}✅{NC} {message}")

def print_error(message):
    print(f"{RED}❌{NC} {message}")

def print_warning(message):
    print(f"{YELLOW}⚠️{NC} {message}")

def check_python_version():
    """Verifies Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Python 3.8+ required")
        return False

def check_dependencies():
    """Verifies that dependencies are installed"""
    try:
        import anthropic
        print_success("anthropic installed")
    except ImportError:
        print_error("anthropic not installed - Run: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        print_success("python-dotenv installed")
    except ImportError:
        print_error("python-dotenv not installed - Run: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Verifies that .env exists and has API key"""
    env_path = Path(".env")
    if not env_path.exists():
        print_warning(".env does not exist - Copy it from .env.example")
        return False
    
    load_dotenv = __import__('dotenv').load_dotenv
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print_warning(".env exists but ANTHROPIC_API_KEY is not configured")
        return False
    
    if api_key.startswith("sk-ant-api03-") or api_key.startswith("sk-ant-"):
        print_success("ANTHROPIC_API_KEY configured")
        return True
    else:
        print_warning("ANTHROPIC_API_KEY seems to have incorrect format")
        return False

def check_skills_structure():
    """Verifies that skills are present"""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        print_error("skills/ directory does not exist")
        return False
    
    required_skills = [
        "project_protocol",
        "requirements_analyzer",
        "codebase_understanding",
        "implementation_protocol"
    ]
    
    all_present = True
    for skill in required_skills:
        skill_path = skills_dir / skill / "SKILL.md"
        if skill_path.exists():
            print_success(f"Skill {skill} present")
        else:
            print_error(f"Skill {skill} not found")
            all_present = False
    
    return all_present

def check_examples():
    """Verifies that examples exist"""
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print_warning("examples/ directory does not exist")
        return False
    
    examples = ["usage_example.py", "complete_example.py"]
    all_present = True
    
    for example in examples:
        example_path = examples_dir / example
        if example_path.exists():
            print_success(f"Example {example} present")
        else:
            print_warning(f"Example {example} not found")
            all_present = False
    
    return all_present

def test_api_connection():
    """Tests API connection (optional)"""
    try:
        from anthropic import Anthropic
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            print_warning("Cannot test API - ANTHROPIC_API_KEY not configured")
            return None
        
        client = Anthropic(api_key=api_key)
        
        # Simple test (doesn't consume many tokens)
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": "Respond only 'OK'"
            }]
        )
        
        if response.content[0].text.strip().upper() == "OK":
            print_success("API connection working")
            return True
        else:
            print_warning("API responded but with unexpected response")
            return None
            
    except Exception as e:
        print_warning(f"Could not test API: {str(e)}")
        return None

def main():
    """Runs all verifications"""
    print("=" * 60)
    print("🔍 Verifying Template Configuration")
    print("=" * 60)
    print()
    
    checks = {
        "Python": check_python_version(),
        "Dependencies": check_dependencies(),
        ".env File": check_env_file(),
        "Skills Structure": check_skills_structure(),
        "Examples": check_examples(),
    }
    
    print()
    print("-" * 60)
    
    # Try API test (optional)
    api_test = test_api_connection()
    if api_test is not None:
        checks["API Connection"] = api_test
    
    print()
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for check_name, result in checks.items():
        status = f"{GREEN}✅{NC}" if result else f"{RED}❌{NC}"
        print(f"{status} {check_name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print()
        print(f"{GREEN}🎉 Everything is configured correctly!{NC}")
        print()
        print("Next steps:")
        print("1. Read GETTING_STARTED.md for your first use")
        print("2. Run: python examples/usage_example.py")
        print("3. Start developing with the skills!")
        return 0
    else:
        print()
        print(f"{YELLOW}⚠️  Some checks failed{NC}")
        print()
        print("Follow these steps:")
        print("1. Review the errors above")
        print("2. Consult QUICK_START.md for help")
        print("3. Run setup.sh or setup.bat if you haven't")
        return 1

if __name__ == "__main__":
    sys.exit(main())
