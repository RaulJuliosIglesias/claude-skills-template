"""
Codebase Analyzer - Helps analyze project structure and state
"""

import os
import json
from pathlib import Path

def analyze_project_structure(root_path):
    """
    Analyzes the project directory structure
    
    Args:
        root_path: Project root path
        
    Returns:
        dict with analyzed structure
    """
    structure = {
        'root': str(root_path),
        'directories': [],
        'files': [],
        'patterns': {}
    }
    
    for root, dirs, files in os.walk(root_path):
        # Ignore node_modules, .git, etc.
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
        
        level = root.replace(str(root_path), '').count(os.sep)
        indent = ' ' * 2 * level
        structure['directories'].append(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Limit to 5 files per directory
            structure['files'].append(f"{subindent}{file}")
    
    return structure

def identify_technologies(root_path):
    """
    Identifies technologies used in the project
    
    Args:
        root_path: Project root path
        
    Returns:
        dict with identified technologies
    """
    technologies = {
        'framework': None,
        'language': None,
        'build_tool': None,
        'testing': None,
        'libraries': []
    }
    
    # Look for package.json (Node.js/React)
    package_json = Path(root_path) / 'package.json'
    if package_json.exists():
        with open(package_json) as f:
            data = json.load(f)
            technologies['framework'] = 'React' if 'react' in data.get('dependencies', {}) else 'Node.js'
            technologies['language'] = 'TypeScript' if 'typescript' in data.get('devDependencies', {}) else 'JavaScript'
            technologies['build_tool'] = 'Vite' if 'vite' in data.get('devDependencies', {}) else 'Webpack'
            technologies['testing'] = 'Jest' if 'jest' in data.get('devDependencies', {}) else None
            technologies['libraries'] = list(data.get('dependencies', {}).keys())[:10]
    
    # Look for requirements.txt (Python)
    requirements_txt = Path(root_path) / 'requirements.txt'
    if requirements_txt.exists():
        technologies['language'] = 'Python'
        with open(requirements_txt) as f:
            technologies['libraries'] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    return technologies

def identify_naming_conventions(root_path):
    """
    Identifies naming conventions used
    
    Args:
        root_path: Project root path
        
    Returns:
        dict with identified conventions
    """
    conventions = {
        'components': None,
        'functions': None,
        'files': None
    }
    
    # Analyze files to identify patterns
    for root, dirs, files in os.walk(root_path):
        if files:
            # Analyze first files found
            sample_files = files[:10]
            for file in sample_files:
                if file.endswith('.tsx') or file.endswith('.jsx'):
                    # React components are usually PascalCase
                    if file[0].isupper():
                        conventions['components'] = 'PascalCase'
                elif file.endswith('.ts') or file.endswith('.js'):
                    # Functions are usually camelCase
                    if file[0].islower():
                        conventions['functions'] = 'camelCase'
                    conventions['files'] = 'camelCase' if file[0].islower() else 'PascalCase'
            break
    
    return conventions

def generate_codebase_summary(root_path):
    """
    Generates a complete codebase summary
    
    Args:
        root_path: Project root path
        
    Returns:
        dict with complete summary
    """
    return {
        'structure': analyze_project_structure(root_path),
        'technology_stack': identify_technologies(root_path),
        'conventions': identify_naming_conventions(root_path),
        'path': str(root_path)
    }
