# 🤖 Usage with Other AI Systems

This template is designed primarily for Claude, but the methodologies and protocols can be adapted to work with other AI systems.

## 🎯 Template Adaptation

### Fundamental Principle

**Skills** are essentially **structured instructions** that can be adapted to different AI systems. The value of the template is not in Claude's specific technical implementation, but in the **methodology and protocols** that guarantee consistent development.

## 🔄 Adaptation for Different AIs

### For ChatGPT / GPT-4

#### Option 1: Use as System Prompts

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Load skill content
def load_skill_as_prompt(skill_name):
    with open(f"skills/{skill_name}/SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        # Extract only content after YAML frontmatter
        if "---" in content:
            content = content.split("---", 2)[2].strip()
        return content

# Build system prompt with all skills
system_prompt = f"""
You are an expert development assistant. Follow these protocols:

{load_skill_as_prompt('project_protocol')}

{load_skill_as_prompt('requirements_analyzer')}

{load_skill_as_prompt('codebase_understanding')}

{load_skill_as_prompt('implementation_protocol')}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I need to add authentication to the project"}
    ]
)
```

#### Option 2: Use Function Calling

You can convert methodologies into functions that GPT can call:

```python
functions = [
    {
        "name": "analyze_requirements",
        "description": "Analyzes user requirements following the protocol",
        "parameters": {
            "type": "object",
            "properties": {
                "requirement": {"type": "string"},
                "functionalities": {"type": "array"},
                "constraints": {"type": "object"}
            }
        }
    },
    # ... more functions based on skills
]
```

### For Gemini / Google AI

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

# Load skills as context
def build_context():
    skills_content = []
    for skill in ['project_protocol', 'requirements_analyzer', 
                  'codebase_understanding', 'implementation_protocol']:
        with open(f"skills/{skill}/SKILL.md", "r") as f:
            content = f.read()
            if "---" in content:
                content = content.split("---", 2)[2].strip()
            skills_content.append(content)
    return "\n\n".join(skills_content)

model = genai.GenerativeModel('gemini-pro')

# Use skills as context
prompt = f"""
Follow these development protocols:

{build_context()}

User: I need to add authentication to the project
"""

response = model.generate_content(prompt)
```

### For Llama / Ollama (Local)

```python
from ollama import Client

client = Client(host='http://localhost:11434')

# Load skills
def load_all_skills():
    skills = {}
    for skill_name in ['project_protocol', 'requirements_analyzer', 
                       'codebase_understanding', 'implementation_protocol']:
        with open(f"skills/{skill_name}/SKILL.md", "r") as f:
            content = f.read()
            if "---" in content:
                content = content.split("---", 2)[2].strip()
            skills[skill_name] = content
    return skills

skills_content = load_all_skills()

system_prompt = f"""
You are a development assistant. Follow these protocols:

{skills_content['project_protocol']}

{skills_content['requirements_analyzer']}

{skills_content['codebase_understanding']}

{skills_content['implementation_protocol']}
"""

response = client.chat(
    model='llama2',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'I need to add authentication'}
    ]
)
```

## 🛠️ Adaptation Tool

### Helper Script for Any AI

```python
"""
Helper to adapt skills to any AI system
"""

from pathlib import Path
from typing import Dict

class SkillsAdapter:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills = {}
        self.load_all_skills()
    
    def load_all_skills(self):
        """Loads all template skills"""
        skill_names = [
            'project_protocol',
            'requirements_analyzer',
            'codebase_understanding',
            'implementation_protocol'
        ]
        
        for skill_name in skill_names:
            skill_path = self.skills_dir / skill_name / "SKILL.md"
            if skill_path.exists():
                content = skill_path.read_text(encoding="utf-8")
                # Remove YAML frontmatter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                self.skills[skill_name] = content
    
    def get_system_prompt(self) -> str:
        """Generates a system prompt with all skills"""
        prompts = []
        prompts.append("You are an expert development assistant. Follow these protocols:\n")
        
        for skill_name, content in self.skills.items():
            prompts.append(f"## {skill_name.replace('_', ' ').title()}\n")
            prompts.append(content)
            prompts.append("\n")
        
        return "\n".join(prompts)
    
    def get_skill(self, skill_name: str) -> str:
        """Gets content of a specific skill"""
        return self.skills.get(skill_name, "")
    
    def get_methodology_summary(self) -> str:
        """Generates a summary of methodologies"""
        summary = """
# Development Methodology

This system follows a 4-phase protocol:

1. **Requirements Analysis**: Completely understand what the user needs
2. **Codebase Understanding**: Analyze the current project state
3. **Planning**: Create a coherent plan that respects existing project
4. **Implementation**: Execute following best practices and standards

Each phase has checklists and validations to ensure quality.
"""
        return summary

# Usage
adapter = SkillsAdapter()
system_prompt = adapter.get_system_prompt()

# Use with any AI
# response = your_ai_client.chat(system=system_prompt, user="your requirement")
```

## 📋 Adaptation Checklist

To adapt this template to another AI system:

- [ ] Identify how the system handles "system prompts" or context
- [ ] Load skill content (remove YAML frontmatter)
- [ ] Combine skills in appropriate prompt/context
- [ ] Adjust format according to system requirements
- [ ] Test with real examples
- [ ] Document specific adaptation

## 🎯 Methodology Advantages

Regardless of the AI system you use, the template methodologies provide:

1. **Structure**: Clear and defined process
2. **Consistency**: Same steps in each project
3. **Quality**: Validations and checklists
4. **Documentation**: Everything is documented
5. **Reproducibility**: Predictable results

## 💡 Recommendations

### For Better Results

1. **Load all skills**: Don't use just one, the power is in the combination
2. **Provide context**: Include project information
3. **Iterate**: Adjust methodologies according to your needs
4. **Document**: Record what works best with your specific AI

### Customization

- Edit `SKILL.md` files to adjust methodologies
- Add domain-specific skills
- Create custom adapters for your stack

## 🔗 Resources

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

---

**Note**: This template is optimized for Claude, but the methodologies are universal and can be adapted to any AI system that supports structured context.
