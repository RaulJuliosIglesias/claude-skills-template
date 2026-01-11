"""
Complete Example: Using the Skills Template for Consistent Development

This example demonstrates how to use all skills together to develop
a complete functionality following the established protocol.
"""

from anthropic import Anthropic
import os
from dotenv import load_dotenv
from pathlib import Path
import json

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found. Configure your .env file.")

# Initialize client
client = Anthropic(api_key=API_KEY)

def get_project_context(project_path):
    """
    Gets project context to include in prompt
    
    Args:
        project_path: Project path
        
    Returns:
        str with project context
    """
    context_parts = []
    
    # Basic information
    context_parts.append(f"Project path: {project_path}")
    
    # Check package.json (React/Node)
    package_json = Path(project_path) / "package.json"
    if package_json.exists():
        with open(package_json) as f:
            data = json.load(f)
            context_parts.append(f"Name: {data.get('name', 'N/A')}")
            context_parts.append(f"Main dependencies: {', '.join(list(data.get('dependencies', {}).keys())[:5])}")
    
    # Check directory structure
    src_path = Path(project_path) / "src"
    if src_path.exists():
        dirs = [d.name for d in src_path.iterdir() if d.is_dir()]
        context_parts.append(f"Directories in src/: {', '.join(dirs[:5])}")
    
    return "\n".join(context_parts)

def develop_with_protocol(user_requirement, project_path=None, verbose=True):
    """
    Develops a functionality following the complete protocol
    
    Args:
        user_requirement: User requirement
        project_path: Optional project path
        verbose: If True, prints detailed information
        
    Returns:
        Claude response
    """
    if verbose:
        print("=" * 80)
        print("DEVELOPMENT WITH COMPLETE PROTOCOL")
        print("=" * 80)
        print(f"\n📋 Requirement: {user_requirement}\n")
    
    # Build context
    context = ""
    if project_path:
        project_context = get_project_context(project_path)
        context = f"""
        
PROJECT CONTEXT:
{project_context}

IMPORTANT: Before implementing, completely analyze the current project state.
"""
    
    # Build message following protocol
    message = f"""
{user_requirement}
{context}

Please follow the complete development protocol:

1. REQUIREMENTS ANALYSIS (requirements_analyzer):
   - Identify the main requirement
   - List all necessary functionalities
   - Identify constraints and dependencies
   - Define acceptance criteria

2. CODEBASE UNDERSTANDING (codebase_understanding):
   - Analyze the project structure
   - Identify technologies and frameworks used
   - Recognize patterns and conventions
   - Locate relevant existing code

3. PLANNING (project_protocol):
   - Create a coherent implementation plan
   - Design solution respecting existing architecture
   - Identify components to create/modify
   - Plan integration

4. IMPLEMENTATION (implementation_protocol):
   - Implement following project conventions
   - Maintain consistency with existing code
   - Document important decisions
   - Validate that it meets requirements

Please provide:
- Complete requirements analysis
- Current project state analysis
- Detailed implementation plan
- Implemented code following standards
"""
    
    if verbose:
        print("🔄 Sending request to Claude with all skills...\n")
    
    # Load all template skills
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=8192,  # More tokens for complete responses
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
        print("✅ Response received\n")
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
                if hasattr(content, 'input'):
                    print(f"   Input: {str(content.input)[:200]}...")
                print()
        
        print("=" * 80)
        print(f"📊 Token Usage:")
        print(f"   Input: {response.usage.input_tokens:,}")
        print(f"   Output: {response.usage.output_tokens:,}")
        print(f"   Total: {response.usage.input_tokens + response.usage.output_tokens:,}")
        print("=" * 80)
    
    return response

def example_simple_feature():
    """Example 1: Simple functionality"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Simple Functionality")
    print("=" * 80)
    
    requirement = "Add a 'Logout' button to the application header"
    
    response = develop_with_protocol(
        requirement,
        project_path=Path.cwd().parent,  # Adjust according to your project
        verbose=True
    )
    
    return response

def example_complex_feature():
    """Example 2: Complex functionality"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Complex Functionality")
    print("=" * 80)
    
    requirement = """
    I need to implement a complete notification system that includes:
    - Real-time notifications using WebSockets
    - Notification panel in header
    - Mark as read/unread
    - Different notification types (info, warning, error, success)
    - Database persistence
    - Integration with existing user system
    """
    
    response = develop_with_protocol(
        requirement,
        project_path=Path.cwd().parent,  # Adjust according to your project
        verbose=True
    )
    
    return response

def example_refactoring():
    """Example 3: Refactoring"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Refactoring")
    print("=" * 80)
    
    requirement = """
    Refactor the authentication module to:
    - Separate business logic from UI
    - Implement a services pattern
    - Improve error handling
    - Add more robust validation
    - Maintain compatibility with existing code
    """
    
    response = develop_with_protocol(
        requirement,
        project_path=Path.cwd().parent,  # Adjust according to your project
        verbose=True
    )
    
    return response

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   Skills Template - Complete Usage Example                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Run examples
    # Uncomment the example you want to test:
    
    # example_simple_feature()
    # example_complex_feature()
    # example_refactoring()
    
    # Or create your own example:
    custom_requirement = input("Enter your requirement (or press Enter to use example): ").strip()
    
    if custom_requirement:
        develop_with_protocol(
            custom_requirement,
            project_path=Path.cwd().parent,
            verbose=True
        )
    else:
        print("\nUsing default example...\n")
        example_simple_feature()
