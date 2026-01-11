"""
Requirements Parser - Ayuda a estructurar y analizar requerimientos
"""

def extract_main_requirement(user_message):
    """
    Extrae el requerimiento principal de un mensaje del usuario
    
    Args:
        user_message: Mensaje del usuario
        
    Returns:
        str con requerimiento principal
    """
    # Identificar verbos de acción comunes
    action_verbs = [
        'crear', 'agregar', 'modificar', 'eliminar', 'implementar',
        'desarrollar', 'construir', 'hacer', 'necesito', 'quiero',
        'create', 'add', 'modify', 'delete', 'implement', 'develop', 'build', 'need', 'want'
    ]
    
    lines = user_message.lower().split('\n')
    main_line = None
    
    for line in lines:
        for verb in action_verbs:
            if verb in line:
                main_line = line.strip()
                break
        if main_line:
            break
    
    return main_line if main_line else lines[0].strip()

def identify_functionalities(text):
    """
    Identifica funcionalidades mencionadas en el texto
    
    Args:
        text: Texto a analizar
        
    Returns:
        list de funcionalidades identificadas
    """
    # Palabras clave que indican funcionalidades
    functionality_keywords = [
        'debe', 'puede', 'necesita', 'incluir', 'tener',
        'must', 'should', 'can', 'needs', 'include', 'have'
    ]
    
    functionalities = []
    sentences = text.split('.')
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for keyword in functionality_keywords:
            if keyword in sentence_lower:
                functionalities.append(sentence.strip())
                break
    
    return functionalities

def identify_constraints(text):
    """
    Identifica restricciones mencionadas en el texto
    
    Args:
        text: Texto a analizar
        
    Returns:
        dict con restricciones por categoría
    """
    constraints = {
        'tecnologicas': [],
        'diseno': [],
        'rendimiento': [],
        'seguridad': [],
        'compatibilidad': []
    }
    
    # Palabras clave por categoría
    tech_keywords = ['usar', 'framework', 'librería', 'tecnología', 'use', 'framework', 'library']
    design_keywords = ['diseño', 'ui', 'ux', 'interfaz', 'design', 'interface']
    perf_keywords = ['rápido', 'performance', 'velocidad', 'fast', 'speed']
    sec_keywords = ['seguridad', 'seguro', 'autenticación', 'security', 'auth']
    compat_keywords = ['compatible', 'navegador', 'plataforma', 'browser', 'platform']
    
    text_lower = text.lower()
    
    # Identificar restricciones tecnológicas
    for keyword in tech_keywords:
        if keyword in text_lower:
            # Extraer contexto alrededor de la palabra clave
            idx = text_lower.find(keyword)
            context = text[max(0, idx-50):min(len(text), idx+100)]
            constraints['tecnologicas'].append(context.strip())
    
    # Similar para otras categorías...
    
    return constraints

def structure_requirements_analysis(user_message):
    """
    Estructura un análisis completo de requerimientos
    
    Args:
        user_message: Mensaje del usuario
        
    Returns:
        dict con análisis estructurado
    """
    return {
        'requirement_principal': extract_main_requirement(user_message),
        'funcionalidades': identify_functionalities(user_message),
        'restricciones': identify_constraints(user_message),
        'dependencias': [],  # Requiere análisis más profundo
        'criterios_aceptacion': [],  # Requiere análisis más profundo
        'ambiguedades': []  # Requiere análisis más profundo
    }

def format_requirements_template(analysis):
    """
    Formatea el análisis en el template estándar
    
    Args:
        analysis: Dict con análisis de requerimientos
        
    Returns:
        str con template formateado
    """
    template = f"""
## Análisis de Requerimientos

### Requerimiento Principal
{analysis.get('requirement_principal', 'No identificado')}

### Funcionalidades Requeridas
"""
    for i, func in enumerate(analysis.get('funcionalidades', []), 1):
        template += f"{i}. {func}\n"
    
    template += "\n### Restricciones\n"
    constraints = analysis.get('restricciones', {})
    for category, items in constraints.items():
        if items:
            template += f"- {category.capitalize()}: {', '.join(items)}\n"
    
    return template
