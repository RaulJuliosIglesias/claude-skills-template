# 🚀 Quick Start Guide

## Configuración Rápida

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 3. Cargar Skills en tu Proyecto

Las skills deben estar en un directorio accesible. Tienes dos opciones:

#### Opción A: Skills Locales (Recomendado para desarrollo)

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Las skills deben estar en un directorio que Claude pueda acceder
# Por ahora, usa las skills de Anthropic o crea las tuyas siguiendo la estructura
```

#### Opción B: Usar con Claude Desktop/Claude.ai

Si estás usando Claude Desktop o Claude.ai, puedes cargar las skills directamente desde el directorio `skills/`.

## Uso Básico

### Ejemplo Mínimo

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
        "content": "Necesito agregar autenticación al proyecto"
    }],
    betas=[
        "code-execution-2025-08-25",
        "files-api-2025-04-14",
        "skills-2025-10-02"
    ]
)

print(response.content[0].text)
```

## Flujo de Trabajo Recomendado

1. **Define tu requerimiento** de forma clara
2. **Ejecuta la consulta** con todas las skills cargadas
3. **Revisa el análisis** que Claude proporciona:
   - Análisis de requerimientos
   - Estado actual del proyecto
   - Plan de implementación
4. **Implementa** siguiendo el plan propuesto
5. **Valida** que cumple con los requerimientos

## Tips para Mejores Resultados

### ✅ Hacer

- **Sé específico**: Menciona detalles importantes
- **Proporciona contexto**: Si hay código relevante, compártelo
- **Menciona restricciones**: Tecnologías, frameworks, versiones
- **Sé claro sobre prioridades**: Qué es más importante

### ❌ Evitar

- Requerimientos muy vagos sin contexto
- Asumir que Claude conoce tu proyecto completo
- Saltarse el análisis del estado actual
- Ignorar las convenciones del proyecto

## Ejemplos de Prompts Efectivos

### ✅ Buen Prompt

```
Necesito agregar un sistema de autenticación al proyecto React que:
- Use JWT para tokens
- Integre con el AuthContext existente
- Siga la estructura de componentes del proyecto
- Use TypeScript como el resto del código
```

### ❌ Prompt Mejorable

```
Agregar login
```

## Personalización

Puedes personalizar las skills editando los archivos `SKILL.md` en cada directorio:

- `skills/project_protocol/SKILL.md` - Ajusta el protocolo principal
- `skills/requirements_analyzer/SKILL.md` - Personaliza el análisis de requerimientos
- `skills/codebase_understanding/SKILL.md` - Ajusta cómo se analiza el código
- `skills/implementation_protocol/SKILL.md` - Personaliza el protocolo de implementación

## Siguiente Paso

Lee el `README.md` completo para entender mejor cómo funciona cada skill y cómo personalizarlas para tus necesidades.
