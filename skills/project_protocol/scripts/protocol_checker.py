"""
Protocol Checker - Verifies that the development process follows the protocol
"""

def check_phase_completion(phase_name, checklist):
    """
    Verifies that a protocol phase is complete
    
    Args:
        phase_name: Phase name
        checklist: Checklist items list
        
    Returns:
        dict with phase status
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
    Validates that requirements analysis is complete
    
    Args:
        analysis: Dict with requirements analysis
        
    Returns:
        dict with validation
    """
    required_fields = [
        'main_requirement',
        'functionalities',
        'constraints',
        'dependencies',
        'acceptance_criteria'
    ]
    
    missing = [field for field in required_fields if field not in analysis or not analysis[field]]
    
    return {
        'valid': len(missing) == 0,
        'missing_fields': missing,
        'completeness': (len(required_fields) - len(missing)) / len(required_fields) * 100
    }

def validate_codebase_analysis(analysis):
    """
    Validates that codebase analysis is complete
    
    Args:
        analysis: Dict with codebase analysis
        
    Returns:
        dict with validation
    """
    required_fields = [
        'structure',
        'technology_stack',
        'architecture',
        'patterns_conventions',
        'relevant_code'
    ]
    
    missing = [field for field in required_fields if field not in analysis or not analysis[field]]
    
    return {
        'valid': len(missing) == 0,
        'missing_fields': missing,
        'completeness': (len(required_fields) - len(missing)) / len(required_fields) * 100
    }

def generate_protocol_report(phases_status):
    """
    Generates a protocol status report
    
    Args:
        phases_status: List of phase statuses
        
    Returns:
        str with formatted report
    """
    report = "=" * 80 + "\n"
    report += "DEVELOPMENT PROTOCOL REPORT\n"
    report += "=" * 80 + "\n\n"
    
    for phase in phases_status:
        status_icon = "✅" if phase['status'] == 'complete' else "⏳"
        report += f"{status_icon} {phase['phase']}: {phase['completed']}/{phase['total']} "
        report += f"({phase['percentage']:.1f}%)\n"
    
    total_completed = sum(p['completed'] for p in phases_status)
    total_items = sum(p['total'] for p in phases_status)
    overall_percentage = (total_completed / total_items * 100) if total_items > 0 else 0
    
    report += "\n" + "-" * 80 + "\n"
    report += f"Overall Progress: {total_completed}/{total_items} ({overall_percentage:.1f}%)\n"
    report += "=" * 80 + "\n"
    
    return report
