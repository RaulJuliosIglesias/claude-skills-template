# 📘 Guía de Integración - Template de Skills

## Cómo Cargar las Skills en Claude

### Método 1: Skills Personalizadas (Custom Skills)

Para usar estas skills como custom skills, necesitas:

1. **Estructura de Skills**: Cada skill debe estar en su propio directorio con `SKILL.md`
2. **Cargar en Claude**: Dependiendo de tu entorno, hay diferentes formas

#### En Claude Desktop

1. Abre Claude Desktop
2. Ve a Settings → Skills
3. Agrega el directorio `skills/` como fuente de skills
4. Las skills deberían aparecer automáticamente

#### En Claude API (Beta)

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Para custom skills, necesitas cargarlas primero
# Esto requiere que las skills estén en un formato que Claude pueda acceder
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    container={
        "skills": [
            {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
            # ... otras skills
        ]
    },
    # ...
)
```

### Método 2: Usar como Referencia en Prompts

Si no puedes cargar las skills directamente, puedes usar su contenido como contexto en tus prompts:

```python
# Leer el contenido de las skills
from pathlib import Path

def load_skill_content(skill_name):
    skill_path = Path(f"skills/{skill_name}/SKILL.md")
    return skill_path.read_text()

# Usar en el prompt
skill_content = load_skill_content("project_protocol")

messages = [{
    "role": "user",
    "content": f"""
{skill_content}

Ahora, siguiendo este protocolo, analiza y desarrolla: [tu requerimiento]
"""
}]
```

## Estructura de las Skills

Cada skill sigue esta estructura:

```
skill_name/
├── SKILL.md          # Documentación principal de la skill
└── scripts/          # Scripts de ayuda (opcional)
    └── helper.py
```

### SKILL.md - Formato

Cada `SKILL.md` debe tener:

1. **YAML Frontmatter**: Metadatos de la skill
2. **Documentación**: Instrucciones detalladas para Claude
3. **Metodología**: Cómo debe trabajar la skill
4. **Ejemplos**: Casos de uso

## Flujo de Trabajo con las Skills

### Paso 1: Análisis Inicial

Cuando el usuario hace una solicitud:

1. **requirements_analyzer** analiza qué necesita el usuario
2. **codebase_understanding** analiza el estado actual
3. **project_protocol** orquesta el proceso

### Paso 2: Planificación

1. **project_protocol** crea un plan basado en:
   - Requerimientos analizados
   - Estado actual del proyecto
   - Mejores prácticas

### Paso 3: Implementación

1. **implementation_protocol** guía la implementación
2. Sigue las convenciones del proyecto
3. Respeta la arquitectura existente

## Personalización de Skills

### Modificar una Skill Existente

1. Edita el archivo `SKILL.md` de la skill
2. Ajusta la metodología según tus necesidades
3. Agrega ejemplos específicos de tu dominio

### Crear una Nueva Skill

1. Crea un nuevo directorio en `skills/`
2. Crea `SKILL.md` con el formato correcto
3. Agrega scripts de ayuda si es necesario
4. Documenta su propósito y uso

### Ejemplo: Skill Personalizada

```markdown
---
name: My Custom Skill
description: |
  Descripción de lo que hace tu skill personalizada.
version: 1.0.0
---

# My Custom Skill

## Propósito
[Descripción detallada]

## Metodología
[Cómo funciona]

## Uso
[Ejemplos]
```

## Mejores Prácticas

### 1. Usar Todas las Skills Juntas

Para mejores resultados, carga todas las skills del template:

```python
skills = [
    {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
    {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
    {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
    {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
]
```

### 2. Proporcionar Contexto del Proyecto

Incluye información sobre tu proyecto en el prompt:

```python
messages = [{
    "role": "user",
    "content": f"""
Proyecto: {project_name}
Stack: {tech_stack}
Estructura: {project_structure}

Requerimiento: {user_requirement}
"""
}]
```

### 3. Iterar y Refinar

Las skills mejoran con el uso. Si algo no funciona como esperas:
- Revisa la documentación de la skill
- Ajusta los prompts
- Personaliza las skills según tus necesidades

## Troubleshooting

### Las Skills No Se Cargan

- Verifica que los archivos `SKILL.md` tengan el formato correcto
- Asegúrate de que el YAML frontmatter esté bien formateado
- Revisa que las rutas sean correctas

### Los Resultados No Son Consistentes

- Asegúrate de cargar todas las skills
- Proporciona contexto suficiente del proyecto
- Usa prompts claros y específicos

### La Implementación No Respeta el Proyecto

- Verifica que `codebase_understanding` tenga acceso al código
- Proporciona más contexto sobre la arquitectura
- Revisa que las convenciones estén documentadas

## Recursos Adicionales

- [Documentación de Skills de Anthropic](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Mejores Prácticas de Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Ejemplos de Skills](https://github.com/anthropics/claude-cookbooks)

## Siguiente Paso

1. Revisa cada skill individual en `skills/`
2. Personaliza según tus necesidades
3. Prueba con un proyecto real
4. Itera y mejora
