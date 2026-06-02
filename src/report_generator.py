import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, Any, Optional

def generate_health_report(result: Dict[str, Any]) -> str:
    """
    Generate a comprehensive health report from analysis results.
    
    Args:
        result: Dictionary containing analysis results
        
    Returns:
        Formatted health report as string
    """
    report = []
    report.append("THYMU HEALTH PREDICTOR REPORT")
    report.append("=" * 50)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary section
    summary = format_summary(result)
    report.append(summary)
    report.append("")
    
    # Detailed metrics
    if 'thymus_volume' in result:
        report.append("DETAILED METRICS:")
        report.append("-" * 30)
        report.append(f"Thymus Volume: {result['thymus_volume']:.2f} cm³")
        
    if 'health_score' in result:
        report.append(f"Health Score: {result['health_score']:.2f}/100")
        
    if 'risk_factors' in result:
        report.append("Risk Factors Detected:")
        for factor, value in result['risk_factors'].items():
            report.append(f"  - {factor}: {value}")
            
    if 'recommendations' in result:
        report.append("RECOMMENDATIONS:")
        report.append("-" * 30)
        for rec in result['recommendations']:
            report.append(f"  • {rec}")
            
    return "\n".join(report)

def format_summary(result: Dict[str, Any]) -> str:
    """
    Format a summary section for the health report.
    
    Args:
        result: Dictionary containing analysis results
        
    Returns:
        Formatted summary string
    """
    summary_lines = []
    
    # Basic information
    summary_lines.append("SUMMARY:")
    summary_lines.append("-" * 30)
    
    # Health status
    if 'health_status' in result:
        summary_lines.append(f"Overall Health Status: {result['health_status']}")
    else:
        summary_lines.append("Overall Health Status: Unknown")
        
    # Risk level
    if 'risk_level' in result:
        summary_lines.append(f"Risk Level: {result['risk_level']}")
    else:
        summary_lines.append("Risk Level: Unknown")
        
    # Age-related insights
    if 'age_group' in result:
        summary_lines.append(f"Age Group: {result['age_group']}")
        
    # Key findings
    if 'key_findings' in result:
        summary_lines.append("Key Findings:")
        for finding in result['key_findings']:
            summary_lines.append(f"  • {finding}")
            
    return "\n".join(summary_lines)

def save_report(report: str, output_path: str) -> bool:
    """
    Save the generated report to a file.
    
    Args:
        report: The formatted report string
        output_path: Path where the report should be saved
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_path, 'w') as f:
            f.write(report)
        return True
    except Exception as e:
        print(f"Error saving report: {e}")
        return False