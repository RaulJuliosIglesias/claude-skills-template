# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Template de Claude Skills!

## Cómo Contribuir

### Reportar Issues
- Usa el sistema de issues de GitHub
- Describe claramente el problema o sugerencia
- Incluye ejemplos cuando sea posible

### Mejorar Documentación
- Corrige errores tipográficos
- Mejora claridad de explicaciones
- Agrega ejemplos útiles
- Traduce a otros idiomas

### Agregar Nuevas Skills
1. Crea un nuevo directorio en `skills/`
2. Sigue la estructura estándar:
   - `SKILL.md` con YAML frontmatter
   - `scripts/` (opcional) para helpers
3. Documenta claramente:
   - Propósito de la skill
   - Metodología que aplica
   - Ejemplos de uso
   - Cómo se integra con otras skills

### Mejorar Skills Existentes
- Refina metodologías
- Agrega más ejemplos
- Mejora scripts de ayuda
- Optimiza para mejor rendimiento

### Compartir Ejemplos
- Agrega casos de uso reales
- Documenta problemas resueltos
- Comparte mejores prácticas descubiertas

## Estándares de Calidad

### Documentación
- Usa Markdown correctamente
- Incluye ejemplos prácticos
- Mantén consistencia de estilo
- Actualiza índices cuando agregues contenido

### Código
- Sigue PEP 8 para Python
- Comenta código complejo
- Incluye docstrings
- Mantén funciones pequeñas y enfocadas

### Skills
- Formato YAML frontmatter correcto
- Descripción clara y concisa
- Metodología bien definida
- Ejemplos relevantes

## Proceso de Contribución

1. **Fork** el repositorio
2. **Crea una rama** para tu contribución
   ```bash
   git checkout -b feature/mi-contribucion
   ```
3. **Haz tus cambios** siguiendo los estándares
4. **Prueba** que todo funciona correctamente
5. **Commit** con mensajes descriptivos
   ```bash
   git commit -m "feat: agregar nueva skill de testing"
   ```
6. **Push** a tu fork
   ```bash
   git push origin feature/mi-contribucion
   ```
7. **Abre un Pull Request** con descripción clara

## Convenciones de Commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, punto y coma faltante, etc.
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Cambios en build, dependencias, etc.

## Estructura de Pull Requests

### Título
- Descriptivo y claro
- Prefijo con tipo (feat, fix, docs, etc.)

### Descripción
- ¿Qué cambia?
- ¿Por qué es necesario?
- ¿Cómo funciona?
- ¿Ejemplos de uso?

### Checklist
- [ ] Código/documentación actualizado
- [ ] Tests pasan (si aplica)
- [ ] Documentación actualizada
- [ ] Ejemplos actualizados (si aplica)

## Áreas de Contribución Prioritarias

### Alta Prioridad
- Mejorar documentación de skills existentes
- Agregar más ejemplos de uso
- Optimizar metodologías de skills

### Media Prioridad
- Crear nuevas skills complementarias
- Mejorar scripts de ayuda
- Agregar casos de uso específicos

### Baja Prioridad
- Traducciones
- Mejoras de estilo
- Optimizaciones menores

## Preguntas Frecuentes

### ¿Necesito experiencia previa?
No, cualquier contribución es bienvenida. Si tienes dudas, abre un issue para discutir.

### ¿Cómo sé si mi contribución es valiosa?
Todas las contribuciones son valiosas. Incluso pequeñas mejoras de documentación ayudan.

### ¿Puedo contribuir skills de otros proyectos?
Sí, siempre que respetes las licencias y des crédito apropiado.

### ¿Hay un código de conducta?
Sí, mantén un ambiente respetuoso y colaborativo.

## Recursos Útiles

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Claude Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Inspiración

## Contacto

- Abre un issue para preguntas
- Usa discussions para ideas generales
- Pull requests para contribuciones concretas

---

**¡Gracias por contribuir!** Cada contribución hace este template mejor para toda la comunidad. 🎉
