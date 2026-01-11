# 📚 Recursos y Referencias - Claude Skills Template

Recursos útiles para aprender más sobre Claude Skills y mejorar tu uso del template.

## 🎯 Recursos Oficiales

### Documentación Principal
- **[Claude Skills Overview](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)** - Introducción oficial a Claude Skills
- **[Claude Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)** - Mejores prácticas oficiales para crear skills
- **[Skills Cookbook](https://github.com/anthropics/claude-cookbooks)** - Ejemplos y guías oficiales de Anthropic
- **[API Documentation](https://docs.anthropic.com/en/api/messages)** - Documentación completa de la API

### Guías de Creación
- **[How to Create Custom Skills](https://support.claude.com/en/articles/12599426-how-to-create-a-skill-with-claude-through-conversation)** - Crear skills mediante conversación
- **[Create a Skill Through Conversation](https://support.claude.com/en/articles/12599426-how-to-create-a-skill-with-claude-through-conversation)** - Tutorial interactivo
- **[Teach Claude Your Way of Working](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)** - Personalizar Claude con tu workflow

### Artículos Técnicos
- **[Equipping Agents for the Real World with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)** - Deep dive técnico sobre Skills
- **[Claude Creates Files](https://www.anthropic.com/news/create-files)** - Cómo Skills habilitan creación de archivos

## 🌟 Recursos de la Comunidad

### Colecciones de Skills
- **[Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)** - Colección curada de skills oficiales y de la comunidad
  - Skills de creación de documentos (Excel, PowerPoint, PDF, Word)
  - Skills de desarrollo y testing
  - Skills de diseño y creatividad
  - Skills especializadas por dominio

### Infraestructura de Claude Code
- **[Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** (8.3k⭐) - **MUY RECOMENDADO**
  - Auto-activación de skills con hooks
  - skill-rules.json para mapeo de patrones
  - Agents especializados
  - Dev docs pattern
  - Probado en producción durante 6 meses
  - Resuelve el problema de "skills no se activan automáticamente"

### Skills de Desarrollo Recomendadas
Basadas en [awesome-claude-skills](https://github.com/VoltAgent/awesome-claude-skills):

#### Testing y Calidad
- **test-driven-development** - Escribir tests antes de implementar código
- **systematic-debugging** - Resolución metódica de problemas
- **testing-skills-with-subagents** - Enfoques colaborativos de testing

#### Git y GitHub
- **git-commit** - Conventional Commits
- **github-pr-creation** - Creación de Pull Requests
- **github-pr-review** - Revisión de código
- **finishing-a-development-branch** - Completar ramas de Git

#### Desarrollo
- **webapp-testing** - Testing de aplicaciones web con Playwright
- **mcp-builder** - Crear servidores MCP para integraciones
- **web-artifacts-builder** - Construir artefactos HTML complejos

### Artículos de la Comunidad
- **[Simon Willison: Claude Skills](https://simonwillison.net/)** - Introducción a Claude Skills
- **[Nick Nisi: Claude Skills](https://www.nicknisi.com/)** - Getting started con Claude Skills

## 📹 Videos y Tutoriales

### Tutoriales en Video
- **Claude Skills Just 10x'd My AI Agents** - Por Greg Isenberg
- **Claude Skills: Build Your Own AI Experts** - Tutorial completo
- **Agent Skills: Specialized capabilities you can customize** - Explicación oficial
- **Claude Skills—From TOY to TOOL** - Tutorial práctico
- **Stop Using MCP... Use NEW Claude Skills Instead** - Comparación con MCP

## 🛠️ Herramientas Relacionadas

### MCP (Model Context Protocol)
- **[MCP Registry](https://github.com/modelcontextprotocol/registry)** - Registro de servidores MCP
- **mcp-builder skill** - Crear servidores MCP con Claude

### Integraciones
- **Linear Claude Skill** - Gestión de issues y proyectos en Linear
- **n8n Automation Skills** - Automatización con n8n
- **AWS Skills** - Desarrollo con AWS

## 📖 Aprendizaje Progresivo

### Nivel 1: Principiante
1. Lee el **README.md** de este template
2. Revisa **QUICK_START.md**
3. Prueba los ejemplos en `examples/`
4. Lee la documentación oficial básica

### Nivel 2: Intermedio
1. Estudia cada skill individual en `skills/`
2. Revisa **INTEGRATION_GUIDE.md**
3. Explora [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)
4. Personaliza las skills según tus necesidades

### Nivel 3: Avanzado
1. Crea tus propias skills personalizadas
2. Contribuye al ecosistema de skills
3. Comparte tus skills con la comunidad
4. Optimiza para casos de uso específicos

## 🔗 Enlaces Rápidos

### Documentación
- [Claude API Docs](https://docs.anthropic.com/en/api/messages)
- [Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)

### Comunidad
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Lista curada
- [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks) - Ejemplos oficiales
- [Claude Support](https://support.claude.com) - Soporte oficial

### Herramientas
- [Anthropic Console](https://console.anthropic.com/) - Gestión de API keys
- [Claude Desktop](https://claude.ai/download) - Aplicación de escritorio

## 💡 Tips y Mejores Prácticas

### Basado en la Comunidad
1. **Usa nombres descriptivos** - Los nombres de skills deben ser claros
2. **Documenta bien** - Incluye ejemplos y casos de uso
3. **Sigue el formato estándar** - YAML frontmatter + markdown
4. **Comparte tus skills** - Contribuye a la comunidad
5. **Itera y mejora** - Las skills mejoran con el uso

### Del Template
1. **Usa todas las skills juntas** - Para mejores resultados
2. **Proporciona contexto** - Incluye información del proyecto
3. **Personaliza según necesidad** - Adapta las skills a tu dominio
4. **Documenta decisiones** - Explica por qué eliges ciertas soluciones

## 🎓 Casos de Uso Inspiradores

### Del Ecosistema
- **Document Creation** - Excel, PowerPoint, PDF, Word
- **Development** - Testing, debugging, code review
- **Design** - UI/UX, arte generativo, branding
- **Automation** - n8n, workflows, integraciones
- **Specialized** - Ciencia, seguridad, finanzas

### Con Este Template
- Desarrollo de features nuevas
- Refactorización de código
- Análisis de requerimientos
- Implementación consistente
- Documentación de proyectos

## 🤝 Contribuir a la Comunidad

### Cómo Contribuir
1. **Comparte tus skills** - Agrega a [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)
2. **Mejora este template** - Envía PRs con mejoras
3. **Documenta casos de uso** - Comparte ejemplos
4. **Ayuda a otros** - Responde preguntas en issues

### Recursos para Contribuir
- [CONTRIBUTING.md](https://github.com/VoltAgent/awesome-claude-skills/blob/main/CONTRIBUTING.md) - Guía de contribución
- [Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices) - Estándares oficiales

---

**¿Tienes un recurso que agregar?** Abre un issue o PR para sugerirlo.

**Última actualización**: Basado en [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) y recursos oficiales de Anthropic.
