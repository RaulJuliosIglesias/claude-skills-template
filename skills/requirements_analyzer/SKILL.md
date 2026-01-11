---
name: Requirements Analysis Protocol
description: |
  Analiza y estructura requerimientos del usuario de forma sistemática. Identifica funcionalidades,
  restricciones, dependencias y criterios de aceptación. Garantiza comprensión completa antes de
  cualquier implementación, evitando malentendidos y asegurando que la solución cumpla exactamente
  con lo que el usuario necesita.
version: 1.0.0
---

# Requirements Analysis Protocol Skill

## Propósito

Esta skill garantiza que todos los requerimientos del usuario sean analizados de forma sistemática y completa antes de cualquier implementación, asegurando:

1. **Comprensión precisa** de lo que el usuario necesita
2. **Identificación completa** de funcionalidades requeridas
3. **Detección temprana** de ambigüedades o inconsistencias
4. **Documentación estructurada** de requerimientos

## Metodología: Análisis Estructurado

### Paso 1: Extracción del Requerimiento Principal

**Objetivo**: Identificar el objetivo central del usuario

**Proceso**:
- Leer el mensaje completo del usuario
- Identificar el verbo de acción principal (crear, modificar, agregar, eliminar, etc.)
- Extraer el objeto principal (qué se quiere crear/modificar)
- Formular el requerimiento principal en una frase clara

**Output**:
```
Requerimiento Principal: [Acción] + [Objeto] + [Contexto]
Ejemplo: "Agregar sistema de autenticación con JWT al proyecto React"
```

### Paso 2: Identificación de Funcionalidades

**Objetivo**: Listar todas las funcionalidades necesarias

**Proceso**:
- Descomponer el requerimiento principal en funcionalidades específicas
- Identificar funcionalidades explícitas mencionadas
- Inferir funcionalidades implícitas necesarias
- Organizar por prioridad o dependencias

**Output**:
```
Funcionalidades:
1. [Funcionalidad principal]
2. [Funcionalidad secundaria]
3. [Funcionalidad de soporte]
...
```

### Paso 3: Identificación de Restricciones

**Objetivo**: Detectar limitaciones y requisitos técnicos

**Proceso**:
- Identificar tecnologías mencionadas o requeridas
- Detectar restricciones de diseño o UX
- Identificar limitaciones de rendimiento
- Notar restricciones de seguridad o privacidad
- Identificar restricciones de compatibilidad

**Output**:
```
Restricciones:
- Tecnológicas: [frameworks, librerías, versiones]
- De diseño: [UI/UX requirements]
- De rendimiento: [performance requirements]
- De seguridad: [security requirements]
- De compatibilidad: [browser, platform requirements]
```

### Paso 4: Identificación de Dependencias

**Objetivo**: Reconocer relaciones con otros componentes

**Proceso**:
- Identificar componentes existentes que se usarán
- Detectar nuevas dependencias necesarias
- Identificar servicios externos requeridos
- Notar dependencias de datos o APIs

**Output**:
```
Dependencias:
- Internas: [componentes del proyecto]
- Externas: [librerías, servicios]
- APIs: [endpoints, servicios]
- Datos: [estructuras de datos, modelos]
```

### Paso 5: Definición de Criterios de Aceptación

**Objetivo**: Establecer cómo validar que la solución es correcta

**Proceso**:
- Definir casos de uso principales
- Identificar escenarios de éxito
- Detectar casos edge o límites
- Establecer métricas de validación

**Output**:
```
Criterios de Aceptación:
1. [Criterio específico y medible]
2. [Criterio específico y medible]
...
```

### Paso 6: Detección de Ambigüedades

**Objetivo**: Identificar puntos que necesitan clarificación

**Proceso**:
- Revisar requerimiento en busca de términos vagos
- Identificar opciones de implementación no especificadas
- Detectar posibles interpretaciones diferentes
- Listar preguntas para clarificar

**Output**:
```
Ambigüedades Detectadas:
- [Punto ambiguo] → Pregunta sugerida: [¿...?]
...
```

## Template de Análisis

Usar este template para estructurar el análisis:

```markdown
## Análisis de Requerimientos

### Requerimiento Principal
[Descripción clara y concisa]

### Funcionalidades Requeridas
1. [Funcionalidad 1]
2. [Funcionalidad 2]
...

### Restricciones
- Tecnológicas: ...
- De diseño: ...
- De rendimiento: ...
- De seguridad: ...

### Dependencias
- Internas: ...
- Externas: ...
- APIs: ...
- Datos: ...

### Criterios de Aceptación
1. [Criterio 1]
2. [Criterio 2]
...

### Ambigüedades (si las hay)
- [Ambigüedad] → ¿[Pregunta]?
```

## Reglas de Análisis

1. **No asumir**: Si algo no está claro, preguntar
2. **Ser exhaustivo**: Analizar todos los aspectos del requerimiento
3. **Ser específico**: Evitar generalidades, ser concreto
4. **Validar comprensión**: Confirmar entendimiento antes de proceder
5. **Documentar todo**: Registrar todas las decisiones y razonamientos

## Ejemplos

### Ejemplo 1: Requerimiento Simple

**Usuario**: "Agregar un botón de logout"

**Análisis**:
- Requerimiento Principal: Agregar funcionalidad de logout al sistema
- Funcionalidades: Botón UI, función de logout, limpieza de sesión
- Restricciones: Debe estar en el header, estilo consistente
- Dependencias: Sistema de autenticación existente
- Criterios: Al hacer click, usuario es deslogueado y redirigido

### Ejemplo 2: Requerimiento Complejo

**Usuario**: "Necesito un dashboard con gráficos de ventas mensuales"

**Análisis**:
- Requerimiento Principal: Crear dashboard con visualización de datos de ventas
- Funcionalidades: Dashboard UI, gráficos mensuales, filtros de fecha, carga de datos
- Restricciones: Debe ser responsive, usar librería de gráficos compatible
- Dependencias: API de ventas, librería de gráficos, sistema de autenticación
- Criterios: Muestra datos correctos, gráficos interactivos, carga rápida
- Ambigüedades: ¿Qué tipo de gráfico? → Preguntar preferencia

## Integración con Otras Skills

Esta skill alimenta:
- `project_protocol`: Proporciona requerimientos estructurados
- `codebase_understanding`: Identifica qué buscar en el código
- `implementation_protocol`: Define qué implementar

## Checklist de Validación

Antes de considerar el análisis completo:

- [ ] Requerimiento principal claramente identificado
- [ ] Todas las funcionalidades listadas
- [ ] Restricciones identificadas
- [ ] Dependencias mapeadas
- [ ] Criterios de aceptación definidos
- [ ] Ambigüedades identificadas y resueltas (o preguntadas)
- [ ] Análisis documentado de forma estructurada
