@echo off
REM Script de configuración rápida para Claude Skills Template (Windows)
REM Uso: setup.bat

echo 🚀 Configurando Claude Skills Template...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.8 o superior.
    exit /b 1
)

echo ✓ Python encontrado
python --version

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    echo ✓ Entorno virtual creado
) else (
    echo ✓ Entorno virtual ya existe
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📥 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencias instaladas

REM Crear .env si no existe
if not exist ".env" (
    echo 📝 Creando archivo .env...
    copy .env.example .env
    echo ⚠️  Por favor edita .env y agrega tu ANTHROPIC_API_KEY
    echo    Obtén tu API key en: https://console.anthropic.com/
) else (
    echo ✓ Archivo .env ya existe
)

REM Crear directorio de outputs
if not exist "outputs" (
    mkdir outputs
    echo ✓ Directorio outputs creado
)

echo.
echo ✅ Configuración completada!
echo.
echo Próximos pasos:
echo 1. Edita .env y agrega tu ANTHROPIC_API_KEY
echo 2. Ejecuta: python test_skills.py (verificar configuración)
echo 3. Lee GETTING_STARTED.md para tu primer uso
echo 4. Revisa examples/ para ver ejemplos de uso
echo.
echo Para activar el entorno virtual en el futuro:
echo   venv\Scripts\activate

pause
