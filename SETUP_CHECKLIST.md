# ✅ Checklist de Configuración

Checklist rápido para verificar que el template esté configurado correctamente.

> **💡 Tip**: Ejecuta `python test_skills.py` para verificación automática  
> **📖 Instrucciones**: Consulta `QUICK_START.md` o `GETTING_STARTED.md` para detalles

## 📋 Pre-Instalación

### Verificaciones Iniciales
- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Git instalado (si vas a clonar)
- [ ] Acceso a internet para descargar dependencias
- [ ] API key de Anthropic (o de otro proveedor de IA)

## 🔧 Instalación

### Paso 1: Obtener el Template
- [ ] Clonado o descargado el repositorio
- [ ] Navegado al directorio del proyecto

### Paso 2: Configuración del Entorno
- [ ] Ejecutado `setup.sh` (Linux/Mac) o `setup.bat` (Windows)
  - O manualmente:
  - [ ] Creado entorno virtual (`python -m venv venv`)
  - [ ] Activado entorno virtual
  - [ ] Instaladas dependencias (`pip install -r requirements.txt`)

### Paso 3: Configuración de API
- [ ] Copiado `.env.example` a `.env`
- [ ] Editado `.env` y agregado `ANTHROPIC_API_KEY`
- [ ] Verificado que `.env` está en `.gitignore`

### Paso 4: Verificación
- [ ] Probado con ejemplo básico (`python examples/usage_example.py`)
- [ ] Verificado que las skills están en `skills/`
- [ ] Creado directorio `outputs/` (si no existe)

## 📚 Documentación (Opcional)

- [ ] Leído `README.md` (visión general)
- [ ] Revisado `QUICK_START.md` o `INTEGRATION_GUIDE.md` según necesidad

## 🎯 Configuración de Skills

### Para Claude Desktop
- [ ] Claude Desktop instalado
- [ ] Abierto Settings → Skills
- [ ] Agregado directorio `skills/` como fuente
- [ ] Verificado que las skills aparecen

### Para Claude API
- [ ] Revisado `INTEGRATION_GUIDE.md`
- [ ] Probado carga de skills en código
- [ ] Verificado que funciona con ejemplo

### Para Otros IAs
- [ ] Revisado `USAGE_WITH_OTHER_AI.md`
- [ ] Adaptado según el sistema de IA
- [ ] Probado con ejemplo

## 🧪 Pruebas

### Pruebas Básicas
- [ ] Ejecutado `examples/usage_example.py` exitosamente
- [ ] Verificado que se genera respuesta de Claude
- [ ] Revisado que el análisis sigue el protocolo

### Pruebas Avanzadas
- [ ] Ejecutado `examples/complete_example.py`
- [ ] Probado con requerimiento real de tu proyecto
- [ ] Verificado que las skills funcionan correctamente

## 🎨 Personalización (Opcional)

### Ajustes Básicos
- [ ] Revisado las skills en `skills/`
- [ ] Entendido cómo funcionan
- [ ] Decidido si necesitas personalizarlas

### Personalización Avanzada
- [ ] Editado `SKILL.md` de alguna skill según necesidad
- [ ] Agregado skills específicas de tu dominio (opcional)
- [ ] Documentado personalizaciones

## 🚀 Listo para Usar

### Verificación Final
- [ ] Todo instalado correctamente
- [ ] API key configurada
- [ ] Skills cargadas y funcionando
- [ ] Ejemplos probados exitosamente
- [ ] Documentación leída

### Próximos Pasos
- [ ] Empezar a usar en tu proyecto
- [ ] Hacer primeros prompts con las skills
- [ ] Iterar y ajustar según resultados

## ❓ Troubleshooting

Si algo no funciona:

1. **API Key no funciona**
   - Verifica que esté correcta en `.env`
   - Verifica que no tenga espacios extra
   - Prueba regenerar la key en console.anthropic.com

2. **Skills no se cargan**
   - Verifica que los archivos `SKILL.md` existan
   - Verifica formato YAML frontmatter
   - Revisa `INTEGRATION_GUIDE.md`

3. **Dependencias no instalan**
   - Verifica Python 3.8+
   - Actualiza pip: `pip install --upgrade pip`
   - Prueba reinstalar: `pip install -r requirements.txt --force-reinstall`

4. **Ejemplos no funcionan**
   - Verifica que `.env` esté configurado
   - Verifica que el entorno virtual esté activado
   - Revisa errores en la consola

## 📞 Ayuda

- Consulta `QUICK_START.md` para instrucciones detalladas
- Revisa `INTEGRATION_GUIDE.md` para problemas de integración
- Consulta `RESOURCES.md` para recursos adicionales

---

**✅ Todo listo?** Consulta `QUICK_START.md` para comenzar. 🚀
