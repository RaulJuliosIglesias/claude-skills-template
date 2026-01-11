"""
Codebase Analyzer - Ayuda a analizar la estructura y estado del proyecto
"""

import os
import json
from pathlib import Path

def analyze_project_structure(root_path):
    """
    Analiza la estructura de directorios del proyecto
    
    Args:
        root_path: Ruta raíz del proyecto
        
    Returns:
        dict con estructura analizada
    """
    structure = {
        'root': str(root_path),
        'directories': [],
        'files': [],
        'patterns': {}
    }
    
    for root, dirs, files in os.walk(root_path):
        # Ignorar node_modules, .git, etc.
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
        
        level = root.replace(str(root_path), '').count(os.sep)
        indent = ' ' * 2 * level
        structure['directories'].append(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Limitar a 5 archivos por directorio
            structure['files'].append(f"{subindent}{file}")
    
    return structure

def identify_technologies(root_path):
    """
    Identifica tecnologías usadas en el proyecto
    
    Args:
        root_path: Ruta raíz del proyecto
        
    Returns:
        dict con tecnologías identificadas
    """
    technologies = {
        'framework': None,
        'language': None,
        'build_tool': None,
        'testing': None,
        'libraries': []
    }
    
    # Buscar package.json (Node.js/React)
    package_json = Path(root_path) / 'package.json'
    if package_json.exists():
        with open(package_json) as f:
            data = json.load(f)
            technologies['framework'] = 'React' if 'react' in data.get('dependencies', {}) else 'Node.js'
            technologies['language'] = 'TypeScript' if 'typescript' in data.get('devDependencies', {}) else 'JavaScript'
            technologies['build_tool'] = 'Vite' if 'vite' in data.get('devDependencies', {}) else 'Webpack'
            technologies['testing'] = 'Jest' if 'jest' in data.get('devDependencies', {}) else None
            technologies['libraries'] = list(data.get('dependencies', {}).keys())[:10]
    
    # Buscar requirements.txt (Python)
    requirements_txt = Path(root_path) / 'requirements.txt'
    if requirements_txt.exists():
        technologies['language'] = 'Python'
        with open(requirements_txt) as f:
            technologies['libraries'] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    return technologies

def identify_naming_conventions(root_path):
    """
    Identifica convenciones de nombres usadas
    
    Args:
        root_path: Ruta raíz del proyecto
        
    Returns:
        dict con convenciones identificadas
    """
    conventions = {
        'components': None,
        'functions': None,
        'files': None
    }
    
    # Analizar archivos para identificar patrones
    for root, dirs, files in os.walk(root_path):
        if files:
            # Analizar primeros archivos encontrados
            sample_files = files[:10]
            for file in sample_files:
                if file.endswith('.tsx') or file.endswith('.jsx'):
                    # Componentes React suelen ser PascalCase
                    if file[0].isupper():
                        conventions['components'] = 'PascalCase'
                elif file.endswith('.ts') or file.endswith('.js'):
                    # Funciones suelen ser camelCase
                    if file[0].islower():
                        conventions['functions'] = 'camelCase'
                    conventions['files'] = 'camelCase' if file[0].islower() else 'PascalCase'
            break
    
    return conventions

def generate_codebase_summary(root_path):
    """
    Genera un resumen completo del código base
    
    Args:
        root_path: Ruta raíz del proyecto
        
    Returns:
        dict con resumen completo
    """
    return {
        'estructura': analyze_project_structure(root_path),
        'stack_tecnologico': identify_technologies(root_path),
        'convenciones': identify_naming_conventions(root_path),
        'ruta': str(root_path)
    }
