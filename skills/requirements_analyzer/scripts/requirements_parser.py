"""
Requirements Parser - Helps structure and analyze requirements
"""

def extract_main_requirement(user_message):
    """
    Extracts the main requirement from a user message
    
    Args:
        user_message: User message
        
    Returns:
        str with main requirement
    """
    # Identify common action verbs
    action_verbs = [
        'create', 'add', 'modify', 'delete', 'implement',
        'develop', 'build', 'make', 'need', 'want',
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
    Identifies functionalities mentioned in text
    
    Args:
        text: Text to analyze
        
    Returns:
        list of identified functionalities
    """
    # Keywords that indicate functionalities
    functionality_keywords = [
        'must', 'should', 'can', 'needs', 'include', 'have',
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
    Identifies constraints mentioned in text
    
    Args:
        text: Text to analyze
        
    Returns:
        dict with constraints by category
    """
    constraints = {
        'technological': [],
        'design': [],
        'performance': [],
        'security': [],
        'compatibility': []
    }
    
    # Keywords by category
    tech_keywords = ['use', 'framework', 'library', 'technology', 'use', 'framework', 'library']
    design_keywords = ['design', 'ui', 'ux', 'interface', 'design', 'interface']
    perf_keywords = ['fast', 'performance', 'speed', 'fast', 'speed']
    sec_keywords = ['security', 'secure', 'authentication', 'security', 'auth']
    compat_keywords = ['compatible', 'browser', 'platform', 'browser', 'platform']
    
    text_lower = text.lower()
    
    # Identify technological constraints
    for keyword in tech_keywords:
        if keyword in text_lower:
            # Extract context around keyword
            idx = text_lower.find(keyword)
            context = text[max(0, idx-50):min(len(text), idx+100)]
            constraints['technological'].append(context.strip())
    
    # Similar for other categories...
    
    return constraints

def structure_requirements_analysis(user_message):
    """
    Structures a complete requirements analysis
    
    Args:
        user_message: User message
        
    Returns:
        dict with structured analysis
    """
    return {
        'main_requirement': extract_main_requirement(user_message),
        'functionalities': identify_functionalities(user_message),
        'constraints': identify_constraints(user_message),
        'dependencies': [],  # Requires deeper analysis
        'acceptance_criteria': [],  # Requires deeper analysis
        'ambiguities': []  # Requires deeper analysis
    }

def format_requirements_template(analysis):
    """
    Formats analysis in standard template
    
    Args:
        analysis: Dict with requirements analysis
        
    Returns:
        str with formatted template
    """
    template = f"""
## Requirements Analysis

### Main Requirement
{analysis.get('main_requirement', 'Not identified')}

### Required Functionalities
"""
    for i, func in enumerate(analysis.get('functionalities', []), 1):
        template += f"{i}. {func}\n"
    
    template += "\n### Constraints\n"
    constraints = analysis.get('constraints', {})
    for category, items in constraints.items():
        if items:
            template += f"- {category.capitalize()}: {', '.join(items)}\n"
    
    return template
