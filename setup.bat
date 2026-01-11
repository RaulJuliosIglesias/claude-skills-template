@echo off
REM Quick setup script for Claude Skills Template (Windows)
REM Usage: setup.bat

echo 🚀 Setting up Claude Skills Template...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    exit /b 1
)

echo ✓ Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencies installed

REM Create .env if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your ANTHROPIC_API_KEY
    echo    Get your API key at: https://console.anthropic.com/
) else (
    echo ✓ .env file already exists
)

REM Create outputs directory
if not exist "outputs" (
    mkdir outputs
    echo ✓ outputs directory created
)

echo.
echo ✅ Setup completed!
echo.
echo Next steps:
echo 1. Edit .env and add your ANTHROPIC_API_KEY
echo 2. Run: python test_skills.py (verify configuration)
echo 3. Read GETTING_STARTED.md for your first use
echo 4. Review examples/ to see usage examples
echo.
echo To activate the virtual environment in the future:
echo   venv\Scripts\activate

pause
