# Skills del Template - Documentación

Este directorio contiene las 4 skills principales del template que garantizan desarrollo consistente y metodológico.

## 📦 Skills Incluidas

### 1. `project_protocol/` - Protocolo Principal

**Propósito**: Orquestar todo el proceso de desarrollo siguiendo un protocolo consistente.

**Cuándo usar**: Siempre. Esta es la skill maestra que coordina las demás.

**Metodología**: Protocolo de 4 fases:
- Análisis de Requerimientos
- Comprensión del Estado Actual
- Planificación de la Solución
- Implementación

### 2. `requirements_analyzer/` - Analizador de Requerimientos

**Propósito**: Analizar y estructurar requerimientos del usuario de forma sistemática.

**Cuándo usar**: Al inicio de cualquier tarea para entender completamente qué necesita el usuario.

**Metodología**: Análisis estructurado en 6 pasos:
1. Extracción del requerimiento principal
2. Identificación de funcionalidades
3. Identificación de restricciones
4. Identificación de dependencias
5. Definición de criterios de aceptación
6. Detección de ambigüedades

### 3. `codebase_understanding/` - Comprensión del Código Base

**Propósito**: Analizar sistemáticamente el estado actual del proyecto.

**Cuándo usar**: Antes de implementar cualquier cambio para respetar la arquitectura existente.

**Metodología**: Análisis sistemático en 6 pasos:
1. Análisis de estructura del proyecto
2. Identificación de tecnologías
3. Análisis de arquitectura
4. Identificación de patrones y convenciones
5. Localización de código relevante
6. Análisis de dependencias y configuración

### 4. `implementation_protocol/` - Protocolo de Implementación

**Propósito**: Guiar la implementación siguiendo mejores prácticas y respetando el proyecto.

**Cuándo usar**: Durante la fase de implementación para asegurar calidad y consistencia.

**Metodología**: Protocolo de implementación en 6 fases:
1. Preparación
2. Diseño de la solución
3. Implementación
4. Integración
5. Validación
6. Documentación

## 🔄 Flujo de Trabajo

```
Usuario hace solicitud
    ↓
project_protocol orquesta
    ↓
requirements_analyzer → Analiza qué necesita
    ↓
codebase_understanding → Analiza estado actual
    ↓
project_protocol → Crea plan coherente
    ↓
implementation_protocol → Implementa siguiendo estándares
    ↓
Resultado: Código consistente y profesional
```

## 📝 Estructura de Cada Skill

Cada skill sigue esta estructura:

```
skill_name/
├── SKILL.md          # Documentación principal (requerido)
└── scripts/          # Scripts de ayuda (opcional)
    └── helper.py
```

### SKILL.md

Cada `SKILL.md` contiene:
- **YAML Frontmatter**: Metadatos (name, description, version)
- **Propósito**: Qué hace la skill
- **Metodología**: Cómo funciona
- **Reglas**: Principios a seguir
- **Ejemplos**: Casos de uso
- **Checklist**: Validación de completitud

### Scripts

Los scripts en `scripts/` son herramientas de ayuda que Claude puede usar, pero no son requeridos. Incluyen:
- Parsers para estructurar información
- Validadores para verificar completitud
- Generadores de reportes

## 🎯 Uso Recomendado

### Cargar Todas las Skills

Para mejores resultados, carga todas las skills juntas:

```python
skills = [
    {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
    {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
    {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
    {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
]
```

### Orden de Prioridad

Si solo puedes cargar algunas skills, prioriza en este orden:
1. `project_protocol` - Esencial para orquestación
2. `requirements_analyzer` - Crítico para entender al usuario
3. `codebase_understanding` - Importante para respetar el proyecto
4. `implementation_protocol` - Útil para guiar implementación

## 🔧 Personalización

Cada skill puede ser personalizada editando su `SKILL.md`:

1. **Ajustar metodología**: Modifica los pasos según tus necesidades
2. **Agregar ejemplos**: Incluye ejemplos específicos de tu dominio
3. **Modificar reglas**: Ajusta las reglas según tus estándares
4. **Extender checklists**: Agrega validaciones adicionales

## 📚 Recursos

- Ver `INTEGRATION_GUIDE.md` para cómo cargar las skills
- Ver `QUICK_START.md` para inicio rápido
- Ver `README.md` principal para visión general

## 🤝 Contribuir

Si mejoras una skill:
1. Documenta los cambios
2. Actualiza ejemplos si es necesario
3. Mantén compatibilidad con otras skills
4. Actualiza esta documentación
