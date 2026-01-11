---
name: Codebase Understanding Protocol
description: |
  Analiza sistemáticamente el estado actual del proyecto para entender arquitectura, tecnologías,
  patrones y convenciones. Garantiza que cualquier implementación respete y se integre correctamente
  con el código existente, manteniendo consistencia y calidad del proyecto.
version: 1.0.0
---

# Codebase Understanding Protocol Skill

## Propósito

Esta skill garantiza una comprensión completa del estado actual del proyecto antes de cualquier implementación, asegurando:

1. **Conocimiento de la arquitectura** actual
2. **Identificación de tecnologías** y frameworks usados
3. **Reconocimiento de patrones** y convenciones
4. **Localización de código relevante** existente
5. **Respeto por la estructura** y organización del proyecto

## Metodología: Análisis Sistemático

### Paso 1: Análisis de Estructura del Proyecto

**Objetivo**: Entender la organización de archivos y directorios

**Proceso**:
1. Examinar estructura de directorios raíz
2. Identificar directorios principales (src, components, utils, etc.)
3. Reconocer patrones de organización
4. Mapear estructura de carpetas

**Output**:
```
Estructura del Proyecto:
├── [directorio principal]
│   ├── [subdirectorio]
│   └── ...
├── [directorio principal]
└── ...

Patrones identificados:
- Organización por: [feature/type/layer]
- Convenciones de nombres: [camelCase/PascalCase/kebab-case]
```

### Paso 2: Identificación de Tecnologías

**Objetivo**: Listar todas las tecnologías, frameworks y librerías

**Proceso**:
1. Revisar package.json / requirements.txt / etc.
2. Identificar framework principal (React, Vue, Angular, etc.)
3. Listar librerías principales
4. Identificar herramientas de build
5. Reconocer sistemas de testing

**Output**:
```
Stack Tecnológico:
- Framework: [React/Vue/etc.]
- Lenguaje: [TypeScript/JavaScript/Python/etc.]
- Build Tool: [Vite/Webpack/etc.]
- Testing: [Jest/Vitest/etc.]
- Librerías principales:
  * [librería 1] - [propósito]
  * [librería 2] - [propósito]
  ...
```

### Paso 3: Análisis de Arquitectura

**Objetivo**: Entender cómo está estructurado el código

**Proceso**:
1. Identificar patrón arquitectónico (MVC, Component-based, etc.)
2. Reconocer capas o módulos principales
3. Identificar flujo de datos
4. Reconocer sistema de estado (Redux, Context, etc.)
5. Identificar sistema de routing

**Output**:
```
Arquitectura:
- Patrón: [MVC/Component-based/etc.]
- Capas principales:
  * [Capa 1]: [responsabilidad]
  * [Capa 2]: [responsabilidad]
- Gestión de estado: [Redux/Context/Zustand/etc.]
- Routing: [React Router/Vue Router/etc.]
- Flujo de datos: [descripción]
```

### Paso 4: Identificación de Patrones y Convenciones

**Objetivo**: Reconocer patrones de código y convenciones usadas

**Proceso**:
1. Analizar ejemplos de código existente
2. Identificar patrones de diseño usados
3. Reconocer convenciones de nombres
4. Identificar estilos de código (ESLint, Prettier configs)
5. Reconocer patrones de componentes/funciones

**Output**:
```
Patrones y Convenciones:
- Nomenclatura:
  * Componentes: [PascalCase/camelCase]
  * Funciones: [camelCase]
  * Archivos: [convención]
- Patrones de diseño:
  * [Patrón 1]: usado en [contexto]
  * [Patrón 2]: usado en [contexto]
- Estilo de código: [configuración ESLint/Prettier]
- Estructura de componentes: [descripción]
```

### Paso 5: Localización de Código Relevante

**Objetivo**: Encontrar código existente relacionado con el requerimiento

**Proceso**:
1. Buscar componentes/funciones similares
2. Identificar código que se reutilizará
3. Localizar código que necesita modificación
4. Identificar servicios/APIs relacionadas
5. Encontrar utilidades existentes relevantes

**Output**:
```
Código Relevante:
- Componentes similares:
  * [ruta/componente] - [propósito]
- Funciones/Utilidades:
  * [ruta/función] - [propósito]
- Servicios/APIs:
  * [ruta/servicio] - [propósito]
- Código a modificar:
  * [ruta/archivo] - [razón]
```

### Paso 6: Análisis de Dependencias y Configuración

**Objetivo**: Entender configuración y dependencias del proyecto

**Proceso**:
1. Revisar archivos de configuración
2. Identificar variables de entorno
3. Reconocer configuración de build
4. Identificar scripts disponibles
5. Revisar configuración de herramientas

**Output**:
```
Configuración:
- Variables de entorno: [lista]
- Scripts disponibles: [npm/yarn scripts]
- Configuración de build: [detalles]
- Herramientas configuradas: [ESLint, Prettier, etc.]
```

## Template de Análisis

Usar este template para documentar el análisis:

```markdown
## Análisis del Estado Actual del Proyecto

### Estructura del Proyecto
[Descripción de organización]

### Stack Tecnológico
- Framework: ...
- Lenguaje: ...
- Librerías principales: ...

### Arquitectura
- Patrón: ...
- Capas: ...
- Gestión de estado: ...

### Patrones y Convenciones
- Nomenclatura: ...
- Patrones de diseño: ...
- Estilo de código: ...

### Código Relevante
- Componentes similares: ...
- Utilidades: ...
- Código a modificar: ...

### Configuración
- Variables de entorno: ...
- Scripts: ...
```

## Reglas de Análisis

1. **Ser exhaustivo**: No asumir, verificar en el código
2. **Buscar patrones**: Identificar cómo se hacen las cosas en el proyecto
3. **Respetar convenciones**: Seguir los patrones existentes
4. **Documentar hallazgos**: Registrar todo lo encontrado
5. **Identificar código reutilizable**: No reinventar la rueda

## Estrategias de Búsqueda

### Para encontrar código similar:
- Buscar por palabras clave relacionadas
- Revisar directorios relacionados
- Buscar imports/exports similares
- Revisar tests para entender uso

### Para entender arquitectura:
- Revisar archivos de configuración principales
- Analizar estructura de imports
- Revisar archivos de entrada (index.js, main.js, App.js)
- Examinar estructura de componentes principales

### Para identificar patrones:
- Revisar múltiples ejemplos de código
- Buscar patrones repetidos
- Analizar convenciones de nombres
- Revisar configuración de herramientas

## Ejemplos

### Ejemplo 1: Proyecto React

**Análisis**:
- Estructura: src/components, src/utils, src/services
- Stack: React 18, TypeScript, Vite
- Arquitectura: Component-based, Context API para estado
- Patrones: Functional components, hooks, custom hooks
- Convenciones: PascalCase para componentes, camelCase para funciones

### Ejemplo 2: Proyecto con Backend

**Análisis**:
- Estructura: frontend/, backend/, shared/
- Stack: React frontend, Node.js backend, PostgreSQL
- Arquitectura: Separación frontend/backend, REST API
- Patrones: MVC en backend, Component-based en frontend
- Convenciones: kebab-case para archivos, camelCase para código

## Integración con Otras Skills

Esta skill alimenta:
- `project_protocol`: Proporciona contexto del estado actual
- `requirements_analyzer`: Identifica qué buscar en el código
- `implementation_protocol`: Define cómo implementar respetando lo existente

## Checklist de Validación

Antes de considerar el análisis completo:

- [ ] Estructura del proyecto mapeada
- [ ] Stack tecnológico identificado
- [ ] Arquitectura entendida
- [ ] Patrones y convenciones reconocidos
- [ ] Código relevante localizado
- [ ] Configuración revisada
- [ ] Análisis documentado
