---
name: Implementation Protocol
description: |
  Guía la implementación siguiendo mejores prácticas, respetando la arquitectura existente y
  manteniendo consistencia con el código del proyecto. Asegura que cada implementación sea
  profesional, testeable, documentada y alineada con los estándares del proyecto.
version: 1.0.0
---

# Implementation Protocol Skill

## Propósito

Esta skill garantiza que toda implementación siga un protocolo consistente y profesional, asegurando:

1. **Respeto por la arquitectura** existente
2. **Consistencia** con código y convenciones del proyecto
3. **Calidad** siguiendo mejores prácticas
4. **Testeabilidad** y mantenibilidad
5. **Documentación** apropiada

## Metodología: Protocolo de Implementación

### Fase 1: Preparación (Preparation)

**Objetivo**: Preparar el entorno y entender el contexto

**Proceso**:
1. Revisar análisis de requerimientos
2. Revisar análisis del código base
3. Identificar ubicación exacta para nuevos archivos
4. Verificar dependencias necesarias
5. Preparar estructura de archivos

**Checklist**:
- [ ] Requerimientos claros y documentados
- [ ] Estado actual del proyecto entendido
- [ ] Ubicación de archivos definida
- [ ] Dependencias verificadas/instaladas
- [ ] Estructura preparada

### Fase 2: Diseño de la Solución (Solution Design)

**Objetivo**: Diseñar la solución respetando el proyecto existente

**Proceso**:
1. Diseñar siguiendo patrones existentes
2. Definir estructura de componentes/funciones
3. Planificar integración con código existente
4. Identificar puntos de extensión
5. Considerar casos edge y errores

**Principios**:
- **DRY (Don't Repeat Yourself)**: Reutilizar código existente
- **KISS (Keep It Simple, Stupid)**: Soluciones simples y claras
- **Consistencia**: Seguir patrones del proyecto
- **Separación de responsabilidades**: Cada componente tiene un propósito claro

**Output**:
```
Diseño de Solución:
- Componentes a crear: [lista]
- Componentes a modificar: [lista]
- Estructura propuesta: [descripción]
- Integración: [cómo se integra]
- Consideraciones: [notas importantes]
```

### Fase 3: Implementación (Implementation)

**Objetivo**: Escribir código de calidad

**Proceso**:
1. Crear estructura de archivos
2. Implementar siguiendo convenciones
3. Usar patrones del proyecto
4. Mantener consistencia de estilo
5. Agregar comentarios donde sea necesario

**Reglas de Implementación**:

#### Nomenclatura
- Seguir convenciones del proyecto
- Nombres descriptivos y claros
- Evitar abreviaciones innecesarias

#### Estructura de Código
- Organizar imports (externos, internos, relativos)
- Agrupar lógica relacionada
- Separar concerns (UI, lógica, datos)

#### Calidad de Código
- Funciones pequeñas y enfocadas
- Evitar código duplicado
- Manejar errores apropiadamente
- Validar inputs cuando sea necesario

#### Consistencia
- Seguir estilo de código existente
- Usar mismos patrones que el proyecto
- Mantener estructura similar a código relacionado

**Template de Implementación**:

```typescript
// Ejemplo para componente React
import React from 'react';
import { existingUtility } from '../utils';
import { ExistingType } from '../types';

/**
 * [Descripción del componente]
 * 
 * @param props - [Descripción de props]
 */
export const NewComponent: React.FC<Props> = ({ prop1, prop2 }) => {
  // Lógica del componente
  // Siguiendo patrones del proyecto
  
  return (
    // JSX siguiendo estructura del proyecto
  );
};
```

### Fase 4: Integración (Integration)

**Objetivo**: Integrar correctamente con el código existente

**Proceso**:
1. Importar/exportar correctamente
2. Integrar con componentes existentes
3. Conectar con servicios/APIs
4. Actualizar rutas si es necesario
5. Verificar que no rompe funcionalidad existente

**Checklist de Integración**:
- [ ] Imports correctos
- [ ] Exports apropiados
- [ ] Integrado con componentes padre
- [ ] Conectado con servicios necesarios
- [ ] Rutas actualizadas si aplica
- [ ] No rompe funcionalidad existente

### Fase 5: Validación (Validation)

**Objetivo**: Verificar que la implementación cumple requerimientos

**Proceso**:
1. Revisar código implementado
2. Verificar que cumple requerimientos
3. Validar que respeta arquitectura
4. Verificar consistencia con proyecto
5. Probar funcionalidad básica

**Checklist de Validación**:
- [ ] Código implementado completamente
- [ ] Cumple todos los requerimientos
- [ ] Respeta arquitectura del proyecto
- [ ] Consistente con código existente
- [ ] Funcionalidad básica verificada
- [ ] Sin errores de sintaxis/compilación

### Fase 6: Documentación (Documentation)

**Objetivo**: Documentar la implementación apropiadamente

**Proceso**:
1. Agregar comentarios en código complejo
2. Documentar funciones/componentes principales
3. Actualizar README si es necesario
4. Documentar decisiones importantes
5. Agregar ejemplos de uso si aplica

**Nivel de Documentación**:
- **Comentarios inline**: Para lógica compleja
- **JSDoc/TSDoc**: Para funciones y componentes públicos
- **README**: Para features importantes o cambios significativos
- **Comentarios de decisión**: Para explicar por qué se eligió una solución

## Reglas de Oro de Implementación

1. **Respetar lo existente**: Nunca cambiar patrones sin razón
2. **Mantener consistencia**: Seguir convenciones del proyecto
3. **Código limpio**: Legible, mantenible, bien estructurado
4. **Manejar errores**: Validar inputs, manejar casos edge
5. **Documentar decisiones**: Explicar elecciones importantes
6. **No romper nada**: Verificar que cambios no afecten funcionalidad existente

## Patrones Comunes por Tipo de Proyecto

### React/TypeScript
- Functional components con hooks
- TypeScript para type safety
- Separación de componentes, hooks, utils, types
- Custom hooks para lógica reutilizable

### Node.js/Express
- Separación de routes, controllers, services
- Middleware para lógica compartida
- Error handling centralizado
- Validación de inputs

### Python
- PEP 8 style guide
- Type hints donde sea posible
- Docstrings para funciones
- Separación de concerns

## Checklist Completo de Implementación

### Antes de Implementar
- [ ] Requerimientos analizados
- [ ] Estado actual entendido
- [ ] Plan de implementación creado
- [ ] Dependencias verificadas

### Durante la Implementación
- [ ] Siguiendo convenciones de nombres
- [ ] Usando patrones del proyecto
- [ ] Código limpio y legible
- [ ] Manejo de errores apropiado

### Después de Implementar
- [ ] Integrado correctamente
- [ ] Validado contra requerimientos
- [ ] Consistente con proyecto
- [ ] Documentado apropiadamente
- [ ] Sin errores de compilación

## Ejemplo de Flujo Completo

```
Requerimiento: Agregar botón de logout

Fase 1 (Preparación):
- Ubicación: Header component
- Dependencia: AuthContext existente

Fase 2 (Diseño):
- Crear componente LogoutButton
- Integrar en Header
- Usar función logout de AuthContext

Fase 3 (Implementación):
- Crear LogoutButton.tsx
- Seguir estructura de otros botones
- Usar estilos del proyecto

Fase 4 (Integración):
- Importar en Header
- Agregar al JSX del Header
- Conectar con AuthContext

Fase 5 (Validación):
- Verificar que funciona
- Verificar estilos consistentes
- Verificar que no rompe nada

Fase 6 (Documentación):
- Comentario JSDoc en componente
- Documentar uso si es necesario
```

## Integración con Otras Skills

Esta skill recibe input de:
- `requirements_analyzer`: Qué implementar
- `codebase_understanding`: Cómo implementar respetando el proyecto
- `project_protocol`: Orquestación del proceso

## Manejo de Errores Comunes

### Error: No sigue convenciones
**Solución**: Revisar código existente y ajustar

### Error: Rompe funcionalidad existente
**Solución**: Revisar integración, verificar imports/exports

### Error: Código inconsistente
**Solución**: Revisar patrones del proyecto y alinear

### Error: Falta documentación
**Solución**: Agregar comentarios y documentación apropiada
