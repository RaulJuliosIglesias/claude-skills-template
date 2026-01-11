"""
Ejemplo Completo: Uso del Template de Skills para Desarrollo Consistente

Este ejemplo demuestra cómo usar todas las skills juntas para desarrollar
una funcionalidad completa siguiendo el protocolo establecido.
"""

from anthropic import Anthropic
import os
from dotenv import load_dotenv
from pathlib import Path
import json

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY no encontrada. Configura tu .env file.")

# Inicializar cliente
client = Anthropic(api_key=API_KEY)

def get_project_context(project_path):
    """
    Obtiene contexto del proyecto para incluir en el prompt
    
    Args:
        project_path: Ruta del proyecto
        
    Returns:
        str con contexto del proyecto
    """
    context_parts = []
    
    # Información básica
    context_parts.append(f"Ruta del proyecto: {project_path}")
    
    # Verificar package.json (React/Node)
    package_json = Path(project_path) / "package.json"
    if package_json.exists():
        with open(package_json) as f:
            data = json.load(f)
            context_parts.append(f"Nombre: {data.get('name', 'N/A')}")
            context_parts.append(f"Dependencias principales: {', '.join(list(data.get('dependencies', {}).keys())[:5])}")
    
    # Verificar estructura de directorios
    src_path = Path(project_path) / "src"
    if src_path.exists():
        dirs = [d.name for d in src_path.iterdir() if d.is_dir()]
        context_parts.append(f"Directorios en src/: {', '.join(dirs[:5])}")
    
    return "\n".join(context_parts)

def develop_with_protocol(user_requirement, project_path=None, verbose=True):
    """
    Desarrolla una funcionalidad siguiendo el protocolo completo
    
    Args:
        user_requirement: Requerimiento del usuario
        project_path: Ruta opcional del proyecto
        verbose: Si True, imprime información detallada
        
    Returns:
        response de Claude
    """
    if verbose:
        print("=" * 80)
        print("DESARROLLO CON PROTOCOLO COMPLETO")
        print("=" * 80)
        print(f"\n📋 Requerimiento: {user_requirement}\n")
    
    # Construir contexto
    context = ""
    if project_path:
        project_context = get_project_context(project_path)
        context = f"""
        
CONTEXTO DEL PROYECTO:
{project_context}

IMPORTANTE: Antes de implementar, analiza completamente el estado actual del proyecto.
"""
    
    # Construir mensaje siguiendo el protocolo
    message = f"""
{user_requirement}
{context}

Por favor, sigue el protocolo completo de desarrollo:

1. ANÁLISIS DE REQUERIMIENTOS (requirements_analyzer):
   - Identifica el requerimiento principal
   - Lista todas las funcionalidades necesarias
   - Identifica restricciones y dependencias
   - Define criterios de aceptación

2. COMPRENSIÓN DEL CÓDIGO BASE (codebase_understanding):
   - Analiza la estructura del proyecto
   - Identifica tecnologías y frameworks usados
   - Reconoce patrones y convenciones
   - Localiza código relevante existente

3. PLANIFICACIÓN (project_protocol):
   - Crea un plan de implementación coherente
   - Diseña la solución respetando la arquitectura existente
   - Identifica componentes a crear/modificar
   - Planifica la integración

4. IMPLEMENTACIÓN (implementation_protocol):
   - Implementa siguiendo las convenciones del proyecto
   - Mantén consistencia con el código existente
   - Documenta decisiones importantes
   - Valida que cumple los requerimientos

Por favor, proporciona:
- Análisis completo de requerimientos
- Análisis del estado actual del proyecto
- Plan de implementación detallado
- Código implementado siguiendo estándares
"""
    
    if verbose:
        print("🔄 Enviando solicitud a Claude con todas las skills...\n")
    
    # Cargar todas las skills del template
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=8192,  # Más tokens para respuestas completas
        container={
            "skills": [
                {"type": "custom", "skill_id": "project_protocol", "version": "latest"},
                {"type": "custom", "skill_id": "requirements_analyzer", "version": "latest"},
                {"type": "custom", "skill_id": "codebase_understanding", "version": "latest"},
                {"type": "custom", "skill_id": "implementation_protocol", "version": "latest"}
            ]
        },
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{"role": "user", "content": message}],
        betas=[
            "code-execution-2025-08-25",
            "files-api-2025-04-14",
            "skills-2025-10-02"
        ]
    )
    
    if verbose:
        print("✅ Respuesta recibida\n")
        print("=" * 80)
        print("RESPUESTA DE CLAUDE")
        print("=" * 80)
        print()
        
        for content in response.content:
            if content.type == "text":
                print(content.text)
                print()
            elif content.type == "tool_use":
                print(f"🔧 Herramienta usada: {content.name}")
                if hasattr(content, 'input'):
                    print(f"   Input: {str(content.input)[:200]}...")
                print()
        
        print("=" * 80)
        print(f"📊 Uso de Tokens:")
        print(f"   Entrada: {response.usage.input_tokens:,}")
        print(f"   Salida: {response.usage.output_tokens:,}")
        print(f"   Total: {response.usage.input_tokens + response.usage.output_tokens:,}")
        print("=" * 80)
    
    return response

def example_simple_feature():
    """Ejemplo 1: Funcionalidad simple"""
    print("\n" + "=" * 80)
    print("EJEMPLO 1: Funcionalidad Simple")
    print("=" * 80)
    
    requirement = "Agregar un botón de 'Cerrar Sesión' en el header de la aplicación"
    
    response = develop_with_protocol(
        requirement,
        project_path=Path.cwd().parent,  # Ajustar según tu proyecto
        verbose=True
    )
    
    return response

def example_complex_feature():
    """Ejemplo 2: Funcionalidad compleja"""
    print("\n" + "=" * 80)
    print("EJEMPLO 2: Funcionalidad Compleja")
    print("=" * 80)
    
    requirement = """
    Necesito implementar un sistema completo de notificaciones que incluya:
    - Notificaciones en tiempo real usando WebSockets
    - Panel de notificaciones en el header
    - Marcar como leídas/no leídas
    - Diferentes tipos de notificaciones (info, warning, error, success)
    - Persistencia en base de datos
    - Integración con el sistema de usuarios existente
    """
    
    response = develop_with_protocol(
        requirement,
        project_path=Path.cwd().parent,  # Ajustar según tu proyecto
        verbose=True
    )
    
    return response

def example_refactoring():
    """Ejemplo 3: Refactorización"""
    print("\n" + "=" * 80)
    print("EJEMPLO 3: Refactorización")
    print("=" * 80)
    
    requirement = """
    Refactorizar el módulo de autenticación para:
    - Separar lógica de negocio de la UI
    - Implementar un patrón de servicios
    - Mejorar manejo de errores
    - Agregar validación más robusta
    - Mantener compatibilidad con código existente
    """
    
    response = develop_with_protocol(
        requirement,
        project_path=Path.cwd().parent,  # Ajustar según tu proyecto
        verbose=True
    )
    
    return response

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   Template de Skills - Ejemplo Completo de Uso             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Ejecutar ejemplos
    # Descomenta el ejemplo que quieras probar:
    
    # example_simple_feature()
    # example_complex_feature()
    # example_refactoring()
    
    # O crea tu propio ejemplo:
    custom_requirement = input("Ingresa tu requerimiento (o presiona Enter para usar ejemplo): ").strip()
    
    if custom_requirement:
        develop_with_protocol(
            custom_requirement,
            project_path=Path.cwd().parent,
            verbose=True
        )
    else:
        print("\nUsando ejemplo por defecto...\n")
        example_simple_feature()
