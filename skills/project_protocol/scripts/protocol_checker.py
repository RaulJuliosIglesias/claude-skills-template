"""
Protocol Checker - Verifica que el proceso de desarrollo siga el protocolo
"""

def check_phase_completion(phase_name, checklist):
    """
    Verifica que una fase del protocolo esté completa
    
    Args:
        phase_name: Nombre de la fase
        checklist: Lista de items del checklist
        
    Returns:
        dict con estado de la fase
    """
    completed = sum(1 for item in checklist if item.get('completed', False))
    total = len(checklist)
    
    return {
        'phase': phase_name,
        'completed': completed,
        'total': total,
        'percentage': (completed / total * 100) if total > 0 else 0,
        'status': 'complete' if completed == total else 'incomplete'
    }

def validate_requirements_analysis(analysis):
    """
    Valida que el análisis de requerimientos esté completo
    
    Args:
        analysis: Dict con el análisis de requerimientos
        
    Returns:
        dict con validación
    """
    required_fields = [
        'requirement_principal',
        'funcionalidades',
        'restricciones',
        'dependencias',
        'criterios_aceptacion'
    ]
    
    missing = [field for field in required_fields if field not in analysis or not analysis[field]]
    
    return {
        'valid': len(missing) == 0,
        'missing_fields': missing,
        'completeness': (len(required_fields) - len(missing)) / len(required_fields) * 100
    }

def validate_codebase_analysis(analysis):
    """
    Valida que el análisis del código base esté completo
    
    Args:
        analysis: Dict con el análisis del código base
        
    Returns:
        dict con validación
    """
    required_fields = [
        'estructura',
        'stack_tecnologico',
        'arquitectura',
        'patrones_convenciones',
        'codigo_relevante'
    ]
    
    missing = [field for field in required_fields if field not in analysis or not analysis[field]]
    
    return {
        'valid': len(missing) == 0,
        'missing_fields': missing,
        'completeness': (len(required_fields) - len(missing)) / len(required_fields) * 100
    }

def generate_protocol_report(phases_status):
    """
    Genera un reporte del estado del protocolo
    
    Args:
        phases_status: Lista de estados de fases
        
    Returns:
        str con reporte formateado
    """
    report = "=" * 80 + "\n"
    report += "REPORTE DE PROTOCOLO DE DESARROLLO\n"
    report += "=" * 80 + "\n\n"
    
    for phase in phases_status:
        status_icon = "✅" if phase['status'] == 'complete' else "⏳"
        report += f"{status_icon} {phase['phase']}: {phase['completed']}/{phase['total']} "
        report += f"({phase['percentage']:.1f}%)\n"
    
    total_completed = sum(p['completed'] for p in phases_status)
    total_items = sum(p['total'] for p in phases_status)
    overall_percentage = (total_completed / total_items * 100) if total_items > 0 else 0
    
    report += "\n" + "-" * 80 + "\n"
    report += f"Progreso General: {total_completed}/{total_items} ({overall_percentage:.1f}%)\n"
    report += "=" * 80 + "\n"
    
    return report
