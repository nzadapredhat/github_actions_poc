"""
Report Generator Utility
Handles HTML report generation for Next Gen UI Agent tests
"""
import os
import shutil
from typing import Optional
from utils.logger import get_logger

logger = get_logger("report_generator")


def setup_html_report(base_report_dir: str, run_dir: str, timestamp: str) -> Optional[str]:
    """
    Copy and configure HTML report template for a test run.
    
    Args:
        base_report_dir: Base directory for storing report outputs (not used for template location)
        run_dir: Directory for this specific test run
        timestamp: Timestamp string to use in JSON filename reference
        
    Returns:
        Path to the generated HTML report file, or None if setup failed
    """
    # Get the template from the templates directory (which is committed to git)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "templates", "report_template.html")
    run_index_html = os.path.join(run_dir, "index.html")
    
    try:
        # Ensure the run directory exists
        os.makedirs(run_dir, exist_ok=True)
        
        # Check if template exists
        if not os.path.exists(template_path):
            logger.error(f"HTML template not found at: {template_path}")
            logger.error(f"Please ensure the templates/report_template.html file exists in the repository")
            return None
        
        # Copy template to the run-specific report folder
        shutil.copy(template_path, run_index_html)
        logger.debug(f"Copied HTML template from {template_path} to: {run_index_html}")
        
        # Update the copied index.html to reference this run's JSON file
        with open(run_index_html, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Replace the generic JSON filename with the timestamped version
        updated_html = html_content.replace(
            "fetch('temp_results.json')", 
            f"fetch('temp_results_{timestamp}.json')"
        )
        
        with open(run_index_html, "w", encoding="utf-8") as f:
            f.write(updated_html)
        
        logger.info(f"✓ HTML report successfully created at: {run_index_html}")
        return run_index_html
        
    except FileNotFoundError as e:
        logger.error(f"File not found during HTML report setup: {e}")
        return None
    except PermissionError as e:
        logger.error(f"Permission denied during HTML report setup: {e}")
        return None
    except Exception as e:
        logger.warning(f"Failed to create HTML report template: {e}")
        logger.debug("Will continue with test execution and generate JSON results only")
        return None


def sanitize_model_name(model_name: str) -> str:
    """
    Sanitize model name for use in directory/file names.
    
    Args:
        model_name: Original model name (may contain special characters)
        
    Returns:
        Sanitized model name safe for filesystem use
    """
    # Replace problematic characters with underscores
    replacements = {
        ':': '_',
        '/': '_',
        '\\': '_',
        '<': '_',
        '>': '_',
        '"': '_',
        '|': '_',
        '?': '_',
        '*': '_',
        ' ': '_'
    }
    
    safe_name = model_name
    for char, replacement in replacements.items():
        safe_name = safe_name.replace(char, replacement)
    
    return safe_name


def create_report_directory(base_dir: str, timestamp: str, model_name: str) -> str:
    """
    Create a directory for storing test run reports.
    
    Args:
        base_dir: Base directory for all reports
        timestamp: Timestamp string for this run
        model_name: Name of the model being tested
        
    Returns:
        Path to the created report directory
    """
    safe_model_name = sanitize_model_name(model_name)
    run_dir = os.path.join(base_dir, f"report_{timestamp}_{safe_model_name}")
    os.makedirs(run_dir, exist_ok=True)
    logger.debug(f"Created report directory: {run_dir}")
    return run_dir


