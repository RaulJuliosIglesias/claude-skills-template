"""
Ejemplo de uso del template de Skills para desarrollo consistente
"""

from anthropic import Anthropic
import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY no encontrada. Configura tu .env file.")

# Inicializar cliente
client = Anthropic(api_key=API_KEY)

def create_development_request(user_requirement, project_path=None):
    """
    Crea una solicitud de desarrollo usando todas las skills del template
    
    Args:
        user_requirement: Requerimiento del usuario
        project_path: Ruta opcional del proyecto a analizar
        
    Returns:
        response de Claude con análisis y plan
    """
    
    # Construir mensaje con contexto del proyecto si se proporciona
    system_context = ""
    if project_path:
        system_context = f"""
        
Contexto del proyecto:
- Ruta del proyecto: {project_path}
- Por favor, analiza el estado actual del proyecto antes de proponer soluciones.
"""
    
    messages = [{
        "role": "user",
        "content": f"""
{user_requirement}

{system_context}

Por favor, sigue el protocolo completo:
1. Analiza los requerimientos de forma estructurada
2. Comprende el estado actual del proyecto
3. Crea un plan de implementación coherente
4. Proporciona la implementación siguiendo las mejores prácticas del proyecto
"""
    }]
    
    # Usar todas las skills del template
    response = client.beta.messages.create(
        model=MODEL,
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
        messages=messages,
        betas=[
            "code-execution-2025-08-25",
            "files-api-2025-04-14",
            "skills-2025-10-02"
        ]
    )
    
    return response

def print_response(response):
    """
    Imprime la respuesta de Claude de forma formateada
    """
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
            print()
    
    print("=" * 80)
    print(f"📊 Tokens: {response.usage.input_tokens} entrada, {response.usage.output_tokens} salida")
    print("=" * 80)

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo 1: Requerimiento simple
    print("Ejemplo 1: Requerimiento Simple")
    print("-" * 80)
    
    requirement = "Necesito agregar un botón de logout al header de la aplicación"
    
    response = create_development_request(requirement)
    print_response(response)
    
    print("\n\n")
    
    # Ejemplo 2: Requerimiento complejo con contexto
    print("Ejemplo 2: Requerimiento Complejo")
    print("-" * 80)
    
    requirement = """
    Necesito implementar un sistema de autenticación completo que incluya:
    - Login con email y contraseña
    - Registro de nuevos usuarios
    - Recuperación de contraseña
    - Protección de rutas privadas
    - Manejo de sesiones con JWT
    """
    
    project_path = Path.cwd()  # Ajustar según tu proyecto
    
    response = create_development_request(requirement, project_path=str(project_path))
    print_response(response)
