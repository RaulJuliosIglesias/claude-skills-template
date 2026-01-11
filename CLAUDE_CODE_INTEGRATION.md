# 🔌 Integración con Claude Code (IDE)

Esta guía explica cómo integrar este template con **Claude Code** (el IDE de Anthropic) para habilitar **auto-activación de skills** y otras funcionalidades avanzadas.

> **Referencia**: Este documento está inspirado en [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase), que resuelve el problema de que las skills no se activan automáticamente.

## 🎯 ¿Qué es Claude Code?

Claude Code es el IDE de Anthropic que permite usar Claude directamente en tu editor. Una de sus características más poderosas es el sistema de **hooks** que puede activar skills automáticamente.

## 🚀 Problema que Resuelve

**Antes**: Las skills no se activan automáticamente - tienes que recordar cuál usar.

**Después**: Las skills se sugieren y activan automáticamente basándose en el contexto.

## 📦 Componentes Necesarios

### 1. Hooks de Claude Code

Los hooks son scripts que se ejecutan en momentos específicos del flujo de trabajo de Claude Code.

#### Hook Esencial: Auto-Activación de Skills

**Ubicación**: `.claude/hooks/user-prompt-submit/`

Este hook se ejecuta cada vez que envías un prompt y puede sugerir skills relevantes.

### 2. skill-rules.json

Archivo que mapea patrones (palabras clave, rutas de archivos, etc.) a skills específicas.

**Ubicación**: `.claude/skill-rules.json`

## 🔧 Configuración Paso a Paso

### Paso 1: Crear Estructura de Directorios

```bash
mkdir -p .claude/hooks/user-prompt-submit
mkdir -p .claude/skills
```

### Paso 2: Copiar Skills al Directorio de Claude Code

```bash
# Copiar skills al directorio .claude
cp -r skills/* .claude/skills/
```

### Paso 3: Crear skill-rules.json

Crea `.claude/skill-rules.json`:

```json
{
  "rules": [
    {
      "skill": "project_protocol",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["desarrollar", "implementar", "crear", "agregar", "nuevo proyecto", "desarrollo"]
        },
        {
          "type": "file_path",
          "patterns": ["**/src/**", "**/components/**", "**/services/**"]
        }
      ]
    },
    {
      "skill": "requirements_analyzer",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["necesito", "quiero", "requiero", "requerimiento", "funcionalidad", "feature"]
        }
      ]
    },
    {
      "skill": "codebase_understanding",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["entender", "analizar", "revisar código", "código existente", "arquitectura"]
        },
        {
          "type": "file_path",
          "patterns": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.py"]
        }
      ]
    },
    {
      "skill": "implementation_protocol",
      "triggers": [
        {
          "type": "keyword",
          "patterns": ["implementar", "código", "escribir", "crear archivo", "modificar"]
        },
        {
          "type": "file_path",
          "patterns": ["**/src/**", "**/components/**", "**/utils/**"]
        }
      ]
    }
  ]
}
```

### Paso 4: Crear Hook de Auto-Activación

Crea `.claude/hooks/user-prompt-submit/skill-activation-prompt.sh`:

```bash
#!/bin/bash

# Hook para auto-activar skills basándose en skill-rules.json
# Se ejecuta cada vez que el usuario envía un prompt

SKILL_RULES_FILE=".claude/skill-rules.json"
USER_PROMPT="$1"

if [ ! -f "$SKILL_RULES_FILE" ]; then
    exit 0
fi

# Leer skill-rules.json y buscar matches
# Este es un ejemplo simplificado - en producción usarías jq o similar

# Extraer keywords del prompt
PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

# Verificar cada regla
while IFS= read -r line; do
    # Buscar patrones en el prompt
    # Si hay match, sugerir la skill
    echo "💡 Skill sugerida: [skill_name] basada en tu prompt"
done < <(cat "$SKILL_RULES_FILE" | jq -r '.rules[] | @json')

exit 0
```

**Nota**: Este es un ejemplo básico. Para una implementación completa, consulta [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase).

## 🎨 Patrón de Progressive Disclosure

Las skills grandes pueden exceder límites de contexto. El repositorio de referencia usa un patrón de **500 líneas máximo** por archivo.

### Estructura Modular

```
skill_name/
├── SKILL.md              # <500 líneas (overview + navegación)
└── resources/            # Archivos adicionales
    ├── routing.md        # <500 líneas
    ├── controllers.md    # <500 líneas
    ├── services.md       # <500 líneas
    └── ...
```

### Ejemplo: Modificar Nuestra Skill

Para `codebase_understanding`, podrías estructurarla así:

```
codebase_understanding/
├── SKILL.md              # Overview y navegación
└── resources/
    ├── structure-analysis.md
    ├── technology-identification.md
    ├── pattern-recognition.md
    └── code-location.md
```

## 🤖 Agents Especializados (Opcional)

Además de skills, puedes crear **agents** para tareas complejas específicas.

### Ejemplo: Agent de Revisión de Arquitectura

Crea `.claude/agents/code-architecture-reviewer.md`:

```markdown
# Code Architecture Reviewer Agent

## Purpose
Review code for architectural consistency and best practices.

## When to Use
- After major refactoring
- Before merging large PRs
- When reviewing code structure

## Process
1. Analyze current architecture
2. Compare with project standards
3. Identify inconsistencies
4. Suggest improvements

## Output
- Architecture review report
- List of inconsistencies
- Recommendations
```

## 📝 Dev Docs Pattern

Sistema de documentación que sobrevive a resets de contexto.

### Estructura de 3 Archivos

Para cada tarea compleja, crea:

1. `[task]-plan.md` - Plan estratégico
2. `[task]-context.md` - Decisiones clave y archivos
3. `[task]-tasks.md` - Checklist de tareas

**Ubicación**: `.claude/dev-docs/` o `dev/active/`

## 🔗 Integración Completa

### Estructura Final Recomendada

```
proyecto/
├── .claude/
│   ├── skills/              # Skills del template
│   │   ├── project_protocol/
│   │   ├── requirements_analyzer/
│   │   ├── codebase_understanding/
│   │   └── implementation_protocol/
│   ├── hooks/
│   │   └── user-prompt-submit/
│   │       └── skill-activation-prompt.sh
│   ├── agents/              # Agents opcionales
│   ├── skill-rules.json     # Reglas de auto-activación
│   └── settings.json        # Configuración de Claude Code
└── skills/                   # Skills originales (backup)
```

## 📚 Recursos Adicionales

### Repositorio de Referencia

**[claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** - Implementación completa y probada en producción:

- ✅ Hooks funcionales para auto-activación
- ✅ skill-rules.json completo
- ✅ Agents especializados
- ✅ Dev docs pattern
- ✅ Ejemplos reales de uso

### Documentación Oficial

- [Claude Code Documentation](https://docs.anthropic.com/en/claude-code) - Documentación oficial
- [Claude Code Hooks](https://docs.anthropic.com/en/claude-code/hooks) - Guía de hooks

## ⚠️ Notas Importantes

### Diferencias con Claude API

- **Claude Code** usa hooks y auto-activación
- **Claude API** requiere cargar skills manualmente
- Este template funciona con ambos, pero la auto-activación solo funciona en Claude Code

### Personalización Requerida

- `skill-rules.json` debe personalizarse según tu proyecto
- Los hooks pueden necesitar ajustes según tu estructura
- Los agents son opcionales y específicos de dominio

## 🚀 Quick Start para Claude Code

1. **Copiar skills a .claude/skills/**
2. **Crear skill-rules.json** con tus patrones
3. **Crear hook básico** (o usar el del repositorio de referencia)
4. **Probar** enviando un prompt - la skill debería sugerirse

## 💡 Tips

- Empieza simple: solo auto-activación básica
- Itera: agrega más reglas según veas qué funciona
- Usa el repositorio de referencia como guía
- Personaliza según tu flujo de trabajo

---

**¿Necesitas más detalles?** Consulta el [repositorio de referencia](https://github.com/diet103/claude-code-infrastructure-showcase) para implementación completa y probada en producción.
