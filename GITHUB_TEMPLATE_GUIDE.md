# 📦 Guía: Usar Este Template en GitHub

Esta guía explica cómo usar este repositorio como template base para nuevos proyectos.

## 🎯 Propósito

Este template está diseñado para ser **descargado/clonado antes de empezar cualquier proyecto** para garantizar:
- ✅ Desarrollo consistente y metodológico
- ✅ Mejor calidad de código desde el inicio
- ✅ Protocolos claros para cualquier stack tecnológico
- ✅ Resultados profesionales con prompts sencillos

## 🚀 Opción 1: Usar como Template de GitHub

### Configurar como Template

1. **En tu repositorio de GitHub:**
   - Ve a Settings → General
   - Scroll hasta "Template repository"
   - Activa "Template repository"
   - Guarda cambios

2. **Usar el template:**
   - Al crear un nuevo repositorio, selecciona "Use this template"
   - O usa: `https://github.com/tu-usuario/claude-skills-template/generate`

### Ventajas
- ✅ GitHub mantiene la estructura
- ✅ Fácil de compartir con tu equipo
- ✅ Historial limpio desde el inicio

## 🔄 Opción 2: Clonar para Cada Proyecto

### Proceso Recomendado

```bash
# 1. Clonar el template
git clone https://github.com/tu-usuario/claude-skills-template.git mi-nuevo-proyecto
cd mi-nuevo-proyecto

# 2. Configurar
./setup.sh  # Linux/Mac
# O
setup.bat   # Windows

# 3. Configurar .env
# Editar .env y agregar tu API key

# 4. Inicializar como nuevo proyecto
rm -rf .git
git init
git add .
git commit -m "Initial commit: Template de Skills configurado"

# 5. Agregar tu código del proyecto
# Ahora puedes empezar a desarrollar con las skills activas
```

## 📋 Checklist de Inicio de Proyecto

Cuando empiezas un nuevo proyecto con este template:

### Fase 1: Configuración Inicial
- [ ] Clonar/descargar el template
- [ ] Ejecutar `setup.sh` o `setup.bat`
- [ ] Configurar `.env` con tu API key
- [ ] Verificar que las dependencias estén instaladas
- [ ] Probar con un ejemplo simple

### Fase 2: Personalización
- [ ] Revisar las skills y ajustar según tu stack
- [ ] Personalizar metodologías si es necesario
- [ ] Agregar skills específicas de tu dominio (opcional)
- [ ] Configurar estructura de tu proyecto

### Fase 3: Integración
- [ ] Cargar las skills en tu entorno (Claude Desktop/API)
- [ ] Probar con un requerimiento real
- [ ] Ajustar según resultados
- [ ] Documentar decisiones específicas del proyecto

## 🎨 Personalización por Tipo de Proyecto

### Para Proyectos React/TypeScript

```bash
# Después de clonar el template
npx create-react-app . --template typescript
# O
npm create vite@latest . -- --template react-ts

# Las skills ya están listas para usar
```

### Para Proyectos Node.js/Express

```bash
# Después de clonar el template
npm init -y
npm install express
# ... otras dependencias

# Las skills funcionan igual
```

### Para Proyectos Python

```bash
# Después de clonar el template
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt  # del template
# Agregar tus propias dependencias

# Las skills son independientes del stack
```

## 📁 Estructura Recomendada

Después de clonar, tu proyecto debería verse así:

```
mi-proyecto/
├── skills/              # Skills del template (mantener)
├── examples/            # Ejemplos (opcional, puedes eliminar)
├── outputs/             # Archivos generados (gitignored)
├── src/                 # Tu código del proyecto
├── .env                 # Configuración (gitignored)
├── .env.example         # Template de configuración
├── README.md            # Actualizar con info de tu proyecto
├── requirements.txt     # Dependencias Python (si aplica)
└── ...                  # Archivos de tu proyecto
```

## 🔧 Integración con Tu Workflow

### Con Claude Desktop

1. **Cargar skills:**
   - Abre Claude Desktop
   - Settings → Skills
   - Agrega el directorio `skills/` de tu proyecto
   - Las skills estarán disponibles automáticamente

2. **Usar en desarrollo:**
   - Abre Claude Desktop
   - Las skills se cargan automáticamente
   - Haz tus prompts normalmente
   - Las skills garantizan consistencia

### Con Claude API

```python
# En tu código del proyecto
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Las skills están en el directorio skills/
# Cárgalas según INTEGRATION_GUIDE.md
```

### Con Otros IAs

Ver **USAGE_WITH_OTHER_AI.md** para adaptar a ChatGPT, Gemini, etc.

## 📝 Actualizar README del Proyecto

Después de clonar, actualiza el README con:

```markdown
# Mi Proyecto

[Descripción de tu proyecto]

## Desarrollo con Skills

Este proyecto usa el [Claude Skills Template](link-al-template) para garantizar desarrollo consistente.

Las skills están en `skills/` y se cargan automáticamente cuando trabajas con Claude.

## Uso

[Instrucciones específicas de tu proyecto]
```

## 🎯 Flujo de Trabajo Recomendado

1. **Inicio de proyecto:**
   ```bash
   git clone template mi-proyecto
   cd mi-proyecto
   ./setup.sh
   # Configurar .env
   ```

2. **Durante desarrollo:**
   - Usa Claude con las skills cargadas
   - Haz prompts sencillos, las skills garantizan calidad
   - Las skills analizan, planifican e implementan consistentemente

3. **Mantenimiento:**
   - Actualiza las skills según mejores prácticas
   - Personaliza según necesidades del proyecto
   - Comparte mejoras con la comunidad

## 🔄 Actualizar el Template

Si mejoras el template:

1. **En el repositorio del template:**
   ```bash
   git add .
   git commit -m "feat: mejora en skills"
   git push
   ```

2. **En proyectos existentes:**
   ```bash
   # Opción 1: Merge manual
   git remote add template https://github.com/tu-usuario/claude-skills-template.git
   git fetch template
   git merge template/main --allow-unrelated-histories
   
   # Opción 2: Copiar cambios manualmente
   # Copiar solo skills/ actualizadas
   ```

## 💡 Tips

### Mantener Skills Actualizadas
- Revisa periódicamente mejoras en el template
- Actualiza skills según mejores prácticas
- Documenta personalizaciones específicas

### Compartir con Equipo
- Todos usan el mismo template
- Consistencia en metodología
- Fácil onboarding de nuevos miembros

### Para Múltiples Proyectos
- Mantén el template centralizado
- Clona para cada proyecto nuevo
- Personaliza según necesidades específicas

## 🚨 Importante

### No Committear
- `.env` (contiene API keys)
- `outputs/` (archivos generados)
- `venv/` o `node_modules/` (dependencias)

### Sí Committear
- `skills/` (las skills son parte del proyecto)
- `.env.example` (template sin secrets)
- Configuración del proyecto

## 📚 Recursos Adicionales

- **QUICK_START.md** - Inicio rápido
- **INTEGRATION_GUIDE.md** - Integración detallada
- **USAGE_WITH_OTHER_AI.md** - Uso con otros IAs
- **RESOURCES.md** - Recursos y referencias

---

**¡Listo para empezar!** Clona el template y comienza tu proyecto con metodología y calidad garantizadas. 🚀
