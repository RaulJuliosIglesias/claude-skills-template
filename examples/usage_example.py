"""
Usage example of the Skills template for consistent development
"""

from anthropic import Anthropic
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found. Configure your .env file.")

# Initialize client
client = Anthropic(api_key=API_KEY)

def create_development_request(user_requirement, project_path=None):
    """
    Creates a development request using all template skills
    
    Args:
        user_requirement: User requirement
        project_path: Optional project path to analyze
        
    Returns:
        Claude response with analysis and plan
    """
    
    # Build message with project context if provided
    system_context = ""
    if project_path:
        system_context = f"""
        
Project context:
- Project path: {project_path}
- Please analyze the current project state before proposing solutions.
"""
    
    messages = [{
        "role": "user",
        "content": f"""
{user_requirement}

{system_context}

Please follow the complete protocol:
1. Analyze requirements in a structured way
2. Understand the current project state
3. Create a coherent implementation plan
4. Provide implementation following project best practices
"""
    }]
    
    # Use all template skills
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
    Prints Claude's response in formatted way
    """
    print("=" * 80)
    print("CLAUDE RESPONSE")
    print("=" * 80)
    print()
    
    for content in response.content:
        if content.type == "text":
            print(content.text)
            print()
        elif content.type == "tool_use":
            print(f"🔧 Tool used: {content.name}")
            print()
    
    print("=" * 80)
    print(f"📊 Tokens: {response.usage.input_tokens} input, {response.usage.output_tokens} output")
    print("=" * 80)

# Usage example
if __name__ == "__main__":
    # Example 1: Simple requirement
    print("Example 1: Simple Requirement")
    print("-" * 80)
    
    requirement = "I need to add a logout button to the application header"
    
    response = create_development_request(requirement)
    print_response(response)
    
    print("\n\n")
    
    # Example 2: Complex requirement with context
    print("Example 2: Complex Requirement")
    print("-" * 80)
    
    requirement = """
    I need to implement a complete authentication system that includes:
    - Login with email and password
    - New user registration
    - Password recovery
    - Private route protection
    - Session handling with JWT
    """
    
    project_path = Path.cwd()  # Adjust according to your project
    
    response = create_development_request(requirement, project_path=str(project_path))
    print_response(response)
