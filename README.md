# Claude Skills Template - Framework de Desarrollo Consistente

Un sistema completo de Skills para Claude que garantiza metodología, protocolo y consistencia en **cualquier proyecto de desarrollo**, independientemente del stack tecnológico.

## 🎯 Objetivo

Este template proporciona un conjunto de Skills que aseguran:
- ✅ **Consistencia metodológica** en todos los proyectos
- ✅ **Protocolos claros** para entender y desarrollar
- ✅ **Mejores resultados** con prompts sencillos
- ✅ **Comprensión completa** del estado actual y futuro del proyecto
- ✅ **Implementación profesional** siguiendo mejores prácticas
- ✅ **Compatible con cualquier stack** (React, Vue, Angular, Node.js, Python, etc.)
- ✅ **Funciona con múltiples IAs** (Claude, ChatGPT, Gemini, etc.)

## 📦 Skills Incluidas

### 1. **project_protocol** - Protocolo Principal de Proyecto
Skill maestro que orquesta todo el proceso de desarrollo, asegurando que cada paso se siga correctamente.

### 2. **requirements_analyzer** - Analizador de Requerimientos
Analiza y estructura los requerimientos del usuario, identificando:
- Qué quiere el usuario
- Por qué lo necesita
- Cómo debe funcionar
- Qué restricciones existen

### 3. **codebase_understanding** - Comprensión del Código Base
Analiza el estado actual del proyecto:
- Qué existe actualmente
- Arquitectura y patrones usados
- Dependencias y tecnologías
- Estructura de archivos

### 4. **implementation_protocol** - Protocolo de Implementación
Guía la implementación siguiendo:
- Mejores prácticas del proyecto
- Consistencia con código existente
- Testing y validación
- Documentación

## 🚀 Inicio Rápido

### Opción 1: Usar como Template de GitHub
```bash
# Crear nuevo repositorio desde template
# O clonar directamente
git clone https://github.com/tu-usuario/claude-skills-template.git mi-proyecto
cd mi-proyecto
./setup.sh  # Linux/Mac
# O setup.bat en Windows
```

### Opción 2: Instalación Manual
```bash
# 1. Clonar o descargar
git clone https://github.com/tu-usuario/claude-skills-template.git
cd claude-skills-template

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar
cp .env.example .env
# Editar .env y agregar tu ANTHROPIC_API_KEY
```

Ver **QUICK_START.md** para más detalles.

## 📁 Estructura del Proyecto

```
claude-skills-template/
├── skills/                    # Skills del template
│   ├── project_protocol/
│   ├── requirements_analyzer/
│   ├── codebase_understanding/
│   └── implementation_protocol/
├── examples/                  # Ejemplos de uso
├── outputs/                   # Archivos generados (gitignored)
├── .env.example              # Template de configuración
├── requirements.txt          # Dependencias Python
├── setup.sh / setup.bat      # Scripts de configuración automática
├── .claude/                  # Configuración Claude Code IDE (opcional)
└── README.md                 # Este archivo
```

## 🔧 Instalación Completa

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar API Key
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Paso 3: Cargar las Skills
Sigue la guía en **INTEGRATION_GUIDE.md** para cargar las skills en tu entorno.

### Paso 4: Verificar Configuración
```bash
python test_skills.py
```

### Paso 5: ¡Empezar a Desarrollar!
Revisa **GETTING_STARTED.md** para tu primer uso o **QUICK_START.md** para más ejemplos.

## 📚 Documentación

### Documentación Principal
- **README.md** (este archivo) - Visión general del template
- **GETTING_STARTED.md** - 🚀 **EMPIEZA AQUÍ** - Tu primer uso paso a paso
- **QUICK_START.md** - Guía rápida de configuración e inicio
- **INTEGRATION_GUIDE.md** - Guía detallada de integración
- **CLAUDE_CODE_INTEGRATION.md** - Integración con Claude Code IDE (auto-activación)
- **GITHUB_TEMPLATE_GUIDE.md** - Cómo usar como template de GitHub
- **USAGE_WITH_OTHER_AI.md** - Adaptación para otros sistemas de IA
- **RESOURCES.md** - Recursos y referencias adicionales
- **INDEX.md** - Índice completo de archivos

### Documentación de Skills
Cada skill incluye documentación completa en su `SKILL.md` explicando:
- Propósito y alcance
- Metodología que aplica
- Ejemplos de uso
- Mejores prácticas

Ver `skills/README.md` para documentación detallada de cada skill.

### Ejemplos
- **examples/usage_example.py** - Ejemplo básico de uso
- **examples/complete_example.py** - Ejemplo completo con casos de uso

## 🎓 Flujo de Trabajo

1. **Análisis**: `requirements_analyzer` entiende qué necesita el usuario
2. **Comprensión**: `codebase_understanding` analiza el estado actual
3. **Planificación**: `project_protocol` crea un plan coherente
4. **Implementación**: `implementation_protocol` ejecuta siguiendo estándares

## 🌟 Recursos y Referencias

### Recursos Oficiales de Claude Skills
- [Claude Skills Quickstart](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) - Guía oficial de inicio
- [Claude Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices) - Mejores prácticas oficiales
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks) - Ejemplos y guías oficiales
- [How to Create Custom Skills](https://support.claude.com/en/articles/12599426-how-to-create-a-skill-with-claude-through-conversation) - Guía de creación

### Recursos de la Comunidad
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Colección curada de skills de la comunidad
- [Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase) - Auto-activación de skills con hooks (8.3k⭐)
- [Claude Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) - Documentación completa

### Artículos y Tutoriales
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Artículo técnico sobre Skills
- [Teach Claude Your Way of Working](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills) - Guía de personalización

## 🤝 Contribuir

Este template está diseñado para ser adaptado a tus necesidades específicas. Modifica las skills según tu metodología preferida.

**¿Quieres contribuir?** Revisa [CONTRIBUTING.md](CONTRIBUTING.md) para ver cómo puedes ayudar:
- Mejorar documentación
- Agregar nuevas skills
- Compartir ejemplos de uso
- Reportar issues o sugerir mejoras

## 📄 Licencia

MIT License - Úsalo libremente en tus proyectos.

## 🎯 Casos de Uso

Este template es perfecto para:
- ✅ **Inicio de nuevos proyectos** - Garantiza calidad desde el día 1
- ✅ **Equipos de desarrollo** - Consistencia metodológica
- ✅ **Múltiples stacks** - Funciona con React, Vue, Node.js, Python, etc.
- ✅ **Diferentes IAs** - Adaptable a Claude, ChatGPT, Gemini, etc.
- ✅ **Proyectos complejos** - Metodología estructurada para cualquier tamaño
- ✅ **Claude Code IDE** - Auto-activación de skills con hooks (ver CLAUDE_CODE_INTEGRATION.md)

---

**¿Listo para empezar?** 
1. 🚀 **GETTING_STARTED.md** - Tu primer uso (recomendado)
2. ⚡ **QUICK_START.md** - Configuración rápida
3. 📦 **GITHUB_TEMPLATE_GUIDE.md** - Usar como template
