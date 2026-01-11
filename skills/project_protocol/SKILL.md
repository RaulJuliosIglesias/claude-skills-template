---
name: Project Management Protocol
description: |
  Skill maestro que garantiza un proceso de desarrollo consistente y metodológico.
  Orquesta el análisis de requerimientos, comprensión del código base, y protocolo de implementación
  para asegurar resultados profesionales en cualquier proyecto. Esta skill asegura que cada paso
  del desarrollo siga un protocolo claro: entender al usuario, analizar el estado actual,
  planificar la solución, e implementar siguiendo mejores prácticas.
version: 1.0.0
---

# Project Management Protocol Skill

## Propósito

Esta skill actúa como orquestador principal que garantiza que todo desarrollo siga un protocolo consistente y metodológico, asegurando:

1. **Comprensión completa** del requerimiento del usuario
2. **Análisis del estado actual** del proyecto
3. **Planificación coherente** de la solución
4. **Implementación profesional** siguiendo estándares

## Metodología: Protocolo de 4 Fases

### Fase 1: Análisis de Requerimientos (Requirements Analysis)
**Objetivo**: Entender completamente qué necesita el usuario

**Proceso**:
1. Identificar el requerimiento principal
2. Extraer requisitos funcionales y no funcionales
3. Identificar restricciones y dependencias
4. Validar comprensión con el usuario si es necesario
5. Documentar el requerimiento de forma estructurada

**Output esperado**:
- Requerimiento principal claramente definido
- Lista de funcionalidades requeridas
- Restricciones identificadas
- Criterios de aceptación

### Fase 2: Comprensión del Estado Actual (Codebase Understanding)
**Objetivo**: Entender qué existe actualmente en el proyecto

**Proceso**:
1. Analizar la estructura del proyecto
2. Identificar tecnologías y frameworks usados
3. Revisar patrones arquitectónicos existentes
4. Identificar código relacionado o similar
5. Documentar el estado actual

**Output esperado**:
- Arquitectura del proyecto documentada
- Tecnologías y dependencias identificadas
- Patrones y convenciones usados
- Código existente relevante identificado

### Fase 3: Planificación de la Solución (Solution Planning)
**Objetivo**: Crear un plan coherente que respete el estado actual

**Proceso**:
1. Diseñar solución que respete arquitectura existente
2. Identificar componentes a crear/modificar
3. Planificar integración con código existente
4. Definir orden de implementación
5. Identificar posibles riesgos o consideraciones

**Output esperado**:
- Plan de implementación paso a paso
- Componentes a crear/modificar
- Estrategia de integración
- Consideraciones técnicas

### Fase 4: Implementación (Implementation)
**Objetivo**: Ejecutar el plan siguiendo mejores prácticas

**Proceso**:
1. Implementar siguiendo el plan
2. Respetar convenciones del proyecto
3. Mantener consistencia con código existente
4. Validar que cumple requerimientos
5. Documentar cambios realizados

**Output esperado**:
- Código implementado y funcional
- Consistente con el proyecto existente
- Documentado apropiadamente
- Validado contra requerimientos

## Reglas de Oro

1. **Nunca asumir**: Siempre analizar el código base antes de implementar
2. **Respetar lo existente**: Mantener consistencia con patrones y convenciones actuales
3. **Validar comprensión**: Si hay dudas sobre el requerimiento, preguntar antes de implementar
4. **Documentar decisiones**: Explicar por qué se eligió una solución específica
5. **Iterar si es necesario**: Si el plan inicial no funciona, ajustar y documentar

## Uso con Otras Skills

Esta skill debe trabajar en conjunto con:
- `requirements_analyzer`: Para análisis profundo de requerimientos
- `codebase_understanding`: Para comprensión del estado actual
- `implementation_protocol`: Para guía de implementación

## Ejemplo de Flujo

```
Usuario: "Necesito agregar autenticación al proyecto"

Fase 1 (Análisis):
- Requerimiento: Sistema de autenticación
- Funcionalidades: Login, registro, sesiones
- Restricciones: Debe usar JWT, compatible con React

Fase 2 (Comprensión):
- Proyecto usa React + TypeScript
- Ya existe estructura de rutas
- No hay sistema de auth actual
- Usa Context API para estado

Fase 3 (Planificación):
- Crear AuthContext
- Crear componentes Login/Register
- Integrar con rutas existentes
- Usar localStorage para tokens

Fase 4 (Implementación):
- Implementar según plan
- Seguir convenciones React del proyecto
- Validar funcionamiento
```

## Checklist de Validación

Antes de considerar completada una tarea, verificar:

- [ ] Requerimiento completamente entendido
- [ ] Estado actual del proyecto analizado
- [ ] Plan de implementación creado
- [ ] Solución respeta arquitectura existente
- [ ] Código implementado y funcional
- [ ] Consistente con convenciones del proyecto
- [ ] Documentación actualizada si es necesario
