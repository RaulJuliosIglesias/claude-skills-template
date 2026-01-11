"""
Script de verificación rápida para validar que el template está correctamente configurado
"""

import os
import sys
from pathlib import Path

# Colores para output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

def print_success(message):
    print(f"{GREEN}✅{NC} {message}")

def print_error(message):
    print(f"{RED}❌{NC} {message}")

def print_warning(message):
    print(f"{YELLOW}⚠️{NC} {message}")

def check_python_version():
    """Verifica versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Se requiere Python 3.8+")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import anthropic
        print_success("anthropic instalado")
    except ImportError:
        print_error("anthropic no instalado - Ejecuta: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        print_success("python-dotenv instalado")
    except ImportError:
        print_error("python-dotenv no instalado - Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Verifica que .env existe y tiene API key"""
    env_path = Path(".env")
    if not env_path.exists():
        print_warning(".env no existe - Cópialo desde .env.example")
        return False
    
    load_dotenv = __import__('dotenv').load_dotenv
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print_warning(".env existe pero ANTHROPIC_API_KEY no está configurada")
        return False
    
    if api_key.startswith("sk-ant-api03-") or api_key.startswith("sk-ant-"):
        print_success("ANTHROPIC_API_KEY configurada")
        return True
    else:
        print_warning("ANTHROPIC_API_KEY parece no tener formato correcto")
        return False

def check_skills_structure():
    """Verifica que las skills estén presentes"""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        print_error("Directorio skills/ no existe")
        return False
    
    required_skills = [
        "project_protocol",
        "requirements_analyzer",
        "codebase_understanding",
        "implementation_protocol"
    ]
    
    all_present = True
    for skill in required_skills:
        skill_path = skills_dir / skill / "SKILL.md"
        if skill_path.exists():
            print_success(f"Skill {skill} presente")
        else:
            print_error(f"Skill {skill} no encontrada")
            all_present = False
    
    return all_present

def check_examples():
    """Verifica que los ejemplos existan"""
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print_warning("Directorio examples/ no existe")
        return False
    
    examples = ["usage_example.py", "complete_example.py"]
    all_present = True
    
    for example in examples:
        example_path = examples_dir / example
        if example_path.exists():
            print_success(f"Ejemplo {example} presente")
        else:
            print_warning(f"Ejemplo {example} no encontrado")
            all_present = False
    
    return all_present

def test_api_connection():
    """Prueba conexión con API (opcional)"""
    try:
        from anthropic import Anthropic
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            print_warning("No se puede probar API - ANTHROPIC_API_KEY no configurada")
            return None
        
        client = Anthropic(api_key=api_key)
        
        # Test simple (no consume muchos tokens)
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": "Responde solo 'OK'"
            }]
        )
        
        if response.content[0].text.strip().upper() == "OK":
            print_success("Conexión con API funcionando")
            return True
        else:
            print_warning("API respondió pero con respuesta inesperada")
            return None
            
    except Exception as e:
        print_warning(f"No se pudo probar API: {str(e)}")
        return None

def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 60)
    print("🔍 Verificando Configuración del Template")
    print("=" * 60)
    print()
    
    checks = {
        "Python": check_python_version(),
        "Dependencias": check_dependencies(),
        "Archivo .env": check_env_file(),
        "Estructura de Skills": check_skills_structure(),
        "Ejemplos": check_examples(),
    }
    
    print()
    print("-" * 60)
    
    # Intentar test de API (opcional)
    api_test = test_api_connection()
    if api_test is not None:
        checks["Conexión API"] = api_test
    
    print()
    print("=" * 60)
    print("📊 Resumen")
    print("=" * 60)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for check_name, result in checks.items():
        status = f"{GREEN}✅{NC}" if result else f"{RED}❌{NC}"
        print(f"{status} {check_name}")
    
    print()
    print(f"Resultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print()
        print(f"{GREEN}🎉 ¡Todo está configurado correctamente!{NC}")
        print()
        print("Próximos pasos:")
        print("1. Lee GETTING_STARTED.md para tu primer uso")
        print("2. Ejecuta: python examples/usage_example.py")
        print("3. ¡Empieza a desarrollar con las skills!")
        return 0
    else:
        print()
        print(f"{YELLOW}⚠️  Algunas verificaciones fallaron{NC}")
        print()
        print("Sigue estos pasos:")
        print("1. Revisa los errores arriba")
        print("2. Consulta QUICK_START.md para ayuda")
        print("3. Ejecuta setup.sh o setup.bat si no lo has hecho")
        return 1

if __name__ == "__main__":
    sys.exit(main())
