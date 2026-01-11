# 🚀 Getting Started - Tu Primer Uso

Guía paso a paso para usar el template por primera vez.

## ⚡ Inicio Rápido (5 minutos)

### Paso 1: Descargar y Configurar

```bash
# Clonar o descargar el template
git clone https://github.com/tu-usuario/claude-skills-template.git mi-proyecto
cd mi-proyecto

# Configurar automáticamente
./setup.sh  # Linux/Mac
# O
setup.bat   # Windows
```

### Paso 2: Configurar API Key

```bash
# Editar .env y agregar tu API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

Obtén tu API key en: https://console.anthropic.com/

### Paso 3: Verificar que Funciona

```bash
# Ejecutar test de verificación
python test_skills.py
```

Si ves "✅ Todo funciona correctamente", ¡estás listo!

---

## 🎯 Tu Primer Prompt con Skills

### Ejemplo Mínimo (Copia y Pega)

```python
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
            {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
            {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
            {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Necesito agregar un botón de logout al header"
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

print(response.content[0].text)
```

### O Usar el Helper

```python
# Usar el ejemplo incluido
python examples/usage_example.py
```

---

## 📖 Flujo de Aprendizaje Recomendado

### Día 1: Configuración (15 min)
1. ✅ Ejecutar setup
2. ✅ Configurar .env
3. ✅ Ejecutar test_skills.py
4. ✅ Leer README.md

### Día 2: Primer Uso (30 min)
1. ✅ Ejecutar examples/usage_example.py
2. ✅ Hacer tu primer prompt real
3. ✅ Revisar QUICK_START.md
4. ✅ Entender el flujo de las skills

### Día 3: Profundizar (1 hora)
1. ✅ Leer skills/README.md
2. ✅ Revisar INTEGRATION_GUIDE.md
3. ✅ Personalizar según tu stack
4. ✅ Crear tu primer prompt complejo

### Día 4+: Optimización
1. ✅ Revisar RESOURCES.md
2. ✅ Explorar CLAUDE_CODE_INTEGRATION.md (si usas Claude Code IDE)
3. ✅ Personalizar skills según tus necesidades
4. ✅ Compartir mejoras con la comunidad

---

## 🎯 Casos de Uso Comunes

### Caso 1: Nuevo Proyecto desde Cero

```python
# Prompt sugerido
"Necesito crear un proyecto React con TypeScript que incluya:
- Sistema de autenticación
- Routing con React Router
- Estado global con Context API
- Estructura de componentes modular"
```

### Caso 2: Agregar Feature a Proyecto Existente

```python
# Prompt sugerido
"Necesito agregar un sistema de comentarios al proyecto existente.
El proyecto usa React + TypeScript y ya tiene autenticación configurada."
```

### Caso 3: Refactorizar Código

```python
# Prompt sugerido
"Necesito refactorizar el módulo de autenticación para:
- Separar lógica de UI
- Mejorar manejo de errores
- Mantener compatibilidad con código existente"
```

---

## 💡 Tips para Mejores Resultados

### ✅ Hacer
- **Sé específico**: Menciona tu stack tecnológico
- **Proporciona contexto**: Comparte estructura del proyecto si es relevante
- **Menciona restricciones**: Versiones, frameworks, convenciones
- **Itera**: Empieza simple, luego agrega complejidad

### ❌ Evitar
- Prompts muy vagos ("haz algo")
- Asumir que Claude conoce tu proyecto completo
- Saltarse el análisis del estado actual
- Ignorar las convenciones del proyecto

---

## 🔧 Personalización Rápida

### Ajustar Skills para Tu Stack

1. **Edita skills/[skill_name]/SKILL.md**
2. **Agrega ejemplos específicos de tu stack**
3. **Ajusta metodología si es necesario**

### Agregar Skills Personalizadas

1. **Crea skills/mi_skill/SKILL.md**
2. **Sigue el formato de las skills existentes**
3. **Agrega a tu lista de skills al usar**

---

## 📚 Próximos Pasos

- **QUICK_START.md** - Más ejemplos y detalles
- **INTEGRATION_GUIDE.md** - Integración avanzada
- **skills/README.md** - Entender cada skill
- **RESOURCES.md** - Recursos adicionales

---

## ❓ ¿Problemas?

1. **Verifica .env** - API key correcta
2. **Ejecuta test_skills.py** - Valida configuración
3. **Revisa QUICK_START.md** - Instrucciones detalladas
4. **Consulta INTEGRATION_GUIDE.md** - Troubleshooting

---

**¡Listo para empezar!** 🚀

Ejecuta `python test_skills.py` para verificar que todo funciona, luego haz tu primer prompt.
