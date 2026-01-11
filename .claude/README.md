# 📁 Directorio .claude

Este directorio contiene la configuración para **Claude Code IDE** (el IDE de Anthropic).

## 🎯 ¿Qué es esto?

Claude Code permite usar hooks y auto-activación de skills. Este directorio contiene la configuración necesaria.

## 📦 Contenido

### skills/
Copia de las skills del template para uso en Claude Code.

### hooks/
Hooks que se ejecutan en momentos específicos del flujo de trabajo.

### skill-rules.json
Archivo que mapea patrones (keywords, file paths) a skills para auto-activación.

## 🚀 Setup Rápido

1. **Copiar skills:**
   ```bash
   cp -r skills/* .claude/skills/
   ```

2. **Configurar skill-rules.json:**
   ```bash
   cp .claude/skill-rules.json.example .claude/skill-rules.json
   # Editar según tus necesidades
   ```

3. **Crear hooks (opcional):**
   Ver `CLAUDE_CODE_INTEGRATION.md` para detalles.

## 📚 Documentación

- **CLAUDE_CODE_INTEGRATION.md** - Guía completa de integración
- **[claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** - Referencia completa

## ⚠️ Nota

Este directorio es **opcional**. Solo es necesario si usas **Claude Code IDE**.

Para uso con Claude API o otros IAs, las skills en `skills/` son suficientes.
