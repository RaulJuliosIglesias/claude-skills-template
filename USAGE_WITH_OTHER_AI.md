# 🤖 Uso con Otros Sistemas de IA

Este template está diseñado principalmente para Claude, pero las metodologías y protocolos pueden adaptarse para trabajar con otros sistemas de IA.

## 🎯 Adaptación del Template

### Principio Fundamental

Las **Skills** son esencialmente **instrucciones estructuradas** que pueden adaptarse a diferentes sistemas de IA. El valor del template no está en la implementación técnica específica de Claude, sino en la **metodología y protocolos** que garantizan desarrollo consistente.

## 🔄 Adaptación para Diferentes IAs

### Para ChatGPT / GPT-4

#### Opción 1: Usar como System Prompts

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Cargar contenido de las skills
def load_skill_as_prompt(skill_name):
    with open(f"skills/{skill_name}/SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        # Extraer solo el contenido después del YAML frontmatter
        if "---" in content:
            content = content.split("---", 2)[2].strip()
        return content

# Construir system prompt con todas las skills
system_prompt = f"""
Eres un asistente de desarrollo experto. Sigue estos protocolos:

{load_skill_as_prompt('project_protocol')}

{load_skill_as_prompt('requirements_analyzer')}

{load_skill_as_prompt('codebase_understanding')}

{load_skill_as_prompt('implementation_protocol')}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Necesito agregar autenticación al proyecto"}
    ]
)
```

#### Opción 2: Usar Function Calling

Puedes convertir las metodologías en funciones que GPT puede llamar:

```python
functions = [
    {
        "name": "analyze_requirements",
        "description": "Analiza requerimientos del usuario siguiendo el protocolo",
        "parameters": {
            "type": "object",
            "properties": {
                "requirement": {"type": "string"},
                "functionalities": {"type": "array"},
                "constraints": {"type": "object"}
            }
        }
    },
    # ... más funciones basadas en las skills
]
```

### Para Gemini / Google AI

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

# Cargar skills como contexto
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

# Usar las skills como contexto
prompt = f"""
Sigue estos protocolos de desarrollo:

{build_context()}

Usuario: Necesito agregar autenticación al proyecto
"""

response = model.generate_content(prompt)
```

### Para Llama / Ollama (Local)

```python
from ollama import Client

client = Client(host='http://localhost:11434')

# Cargar skills
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
Eres un asistente de desarrollo. Sigue estos protocolos:

{skills_content['project_protocol']}

{skills_content['requirements_analyzer']}

{skills_content['codebase_understanding']}

{skills_content['implementation_protocol']}
"""

response = client.chat(
    model='llama2',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'Necesito agregar autenticación'}
    ]
)
```

## 🛠️ Herramienta de Adaptación

### Script Helper para Cualquier IA

```python
"""
Helper para adaptar las skills a cualquier sistema de IA
"""

from pathlib import Path
from typing import Dict

class SkillsAdapter:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills = {}
        self.load_all_skills()
    
    def load_all_skills(self):
        """Carga todas las skills del template"""
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
                # Remover YAML frontmatter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                self.skills[skill_name] = content
    
    def get_system_prompt(self) -> str:
        """Genera un system prompt con todas las skills"""
        prompts = []
        prompts.append("Eres un asistente de desarrollo experto. Sigue estos protocolos:\n")
        
        for skill_name, content in self.skills.items():
            prompts.append(f"## {skill_name.replace('_', ' ').title()}\n")
            prompts.append(content)
            prompts.append("\n")
        
        return "\n".join(prompts)
    
    def get_skill(self, skill_name: str) -> str:
        """Obtiene el contenido de una skill específica"""
        return self.skills.get(skill_name, "")
    
    def get_methodology_summary(self) -> str:
        """Genera un resumen de las metodologías"""
        summary = """
# Metodología de Desarrollo

Este sistema sigue un protocolo de 4 fases:

1. **Análisis de Requerimientos**: Entender completamente qué necesita el usuario
2. **Comprensión del Código Base**: Analizar el estado actual del proyecto
3. **Planificación**: Crear un plan coherente que respete el proyecto existente
4. **Implementación**: Ejecutar siguiendo mejores prácticas y estándares

Cada fase tiene checklists y validaciones para asegurar calidad.
"""
        return summary

# Uso
adapter = SkillsAdapter()
system_prompt = adapter.get_system_prompt()

# Usar con cualquier IA
# response = your_ai_client.chat(system=system_prompt, user="tu requerimiento")
```

## 📋 Checklist de Adaptación

Para adaptar este template a otro sistema de IA:

- [ ] Identificar cómo el sistema maneja "system prompts" o contexto
- [ ] Cargar contenido de las skills (remover YAML frontmatter)
- [ ] Combinar skills en un prompt/contexto apropiado
- [ ] Ajustar formato según requerimientos del sistema
- [ ] Probar con ejemplos reales
- [ ] Documentar adaptación específica

## 🎯 Ventajas de la Metodología

Independientemente del sistema de IA que uses, las metodologías del template proporcionan:

1. **Estructura**: Proceso claro y definido
2. **Consistencia**: Mismos pasos en cada proyecto
3. **Calidad**: Validaciones y checklists
4. **Documentación**: Todo está documentado
5. **Reproducibilidad**: Resultados predecibles

## 💡 Recomendaciones

### Para Mejores Resultados

1. **Carga todas las skills**: No uses solo una, el poder está en la combinación
2. **Proporciona contexto**: Incluye información del proyecto
3. **Itera**: Ajusta las metodologías según tus necesidades
4. **Documenta**: Registra qué funciona mejor con tu IA específica

### Personalización

- Edita los archivos `SKILL.md` para ajustar metodologías
- Agrega skills específicas para tu dominio
- Crea adaptadores personalizados para tu stack

## 🔗 Recursos

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

---

**Nota**: Este template está optimizado para Claude, pero las metodologías son universales y pueden adaptarse a cualquier sistema de IA que soporte contexto estructurado.
