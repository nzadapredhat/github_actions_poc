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
    Copy HTML report template for a test run.
    Note: The actual data embedding happens in finalize_html_report()
    
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
        
        logger.info(f"✓ HTML report template created at: {run_index_html}")
        logger.info(f"  Note: Call finalize_html_report() after tests complete to embed data")
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


def finalize_html_report(html_path: str, json_path: str) -> bool:
    """
    Embed JSON data directly into HTML report to avoid CORS issues when viewing locally.
    
    Args:
        html_path: Path to the HTML report file
        json_path: Path to the JSON results file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import json
        
        # Read the JSON data
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Read the HTML template
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert JSON data to JavaScript variable
        json_str = json.dumps(json_data, indent=2)
        
        # Replace the fetch() call with embedded data
        # Find the fetch section and replace it
        fetch_pattern = """        // Fetch and display results
        fetch('temp_results.json')
            .then(response => response.json())
            .then(data => {
                allResults = data;
                updateSummary();
                displayResults();
                document.getElementById('loading').style.display = 'none';
            })
            .catch(error => {
                console.error('Error loading results:', error);
                document.getElementById('loading').innerHTML = 
                    '<div class="no-results"><h3>❌ Error loading test results</h3><p>' + error.message + '</p></div>';
            });"""
        
        replacement = f"""        // Data embedded directly to avoid CORS issues when viewing locally
        allResults = {json_str};
        updateSummary();
        displayResults();
        document.getElementById('loading').style.display = 'none';"""
        
        updated_html = html_content.replace(fetch_pattern, replacement)
        
        # Also handle the case where the JSON filename might be timestamped
        if fetch_pattern not in html_content:
            # Try to find and replace any fetch() call that looks like it's loading results
            import re
            fetch_regex = r"fetch\('temp_results[^']*\.json'\)\s*\.then\(response => response\.json\(\)\)\s*\.then\(data => \{[^}]*allResults = data;[^}]*\}\)\s*\.catch\([^)]*\);"
            if re.search(fetch_regex, html_content, re.DOTALL):
                updated_html = re.sub(
                    r"// Fetch and display results\s*fetch\('temp_results[^']*\.json'\).*?\.catch\([^;]*\);",
                    replacement,
                    html_content,
                    flags=re.DOTALL
                )
        
        # Write the updated HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        logger.info(f"✓ HTML report finalized with embedded data: {html_path}")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found during HTML report finalization: {e}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to finalize HTML report: {e}")
        return False


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


