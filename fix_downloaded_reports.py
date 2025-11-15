#!/usr/bin/env python3
"""
Utility script to fix downloaded HTML reports with CORS issues.

This script embeds JSON data directly into HTML reports to avoid CORS errors
when viewing them locally with the file:// protocol.

Usage:
    python fix_downloaded_reports.py <path_to_report_directory>
    
Example:
    python fix_downloaded_reports.py ~/Downloads/artifact/report_20251115_135705_llama3.2/
"""

import json
import os
import sys
import glob
from pathlib import Path


def fix_html_report(html_path: str, json_path: str) -> bool:
    """
    Embed JSON data directly into HTML report to avoid CORS issues.
    
    Args:
        html_path: Path to the HTML report file
        json_path: Path to the JSON results file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the JSON data
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if already fixed
        if "// Data embedded directly to avoid CORS issues" in html_content:
            print(f"  ℹ️  {html_path} - Already fixed, skipping")
            return True
        
        # Convert JSON data to JavaScript variable
        json_str = json.dumps(json_data, indent=2)
        
        # Create the replacement code
        replacement = f"""        // Data embedded directly to avoid CORS issues when viewing locally
        allResults = {json_str};
        updateSummary();
        displayResults();
        document.getElementById('loading').style.display = 'none';"""
        
        # Try to find and replace the fetch() pattern
        import re
        
        # Pattern to match the fetch call and its promise chain
        # This pattern is more flexible and matches the actual structure
        fetch_pattern = re.compile(
            r"(\s*)// Fetch and display results\s*\n"
            r"\s*fetch\('temp_results[^']*\.json'\)\s*\n"
            r".*?\.catch\([^}]*\}\);",
            re.MULTILINE | re.DOTALL
        )
        
        updated_html = fetch_pattern.sub(replacement, html_content)
        
        if updated_html == html_content:
            print(f"  ⚠️  {html_path} - Could not find fetch pattern to replace")
            return False
        
        # Write the updated HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"  ✅ {html_path} - Fixed successfully")
        return True
        
    except FileNotFoundError as e:
        print(f"  ❌ {html_path} - File not found: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"  ❌ {html_path} - Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"  ❌ {html_path} - Error: {e}")
        return False


def fix_report_directory(report_dir: str) -> tuple[int, int]:
    """
    Fix all HTML reports in a directory.
    
    Args:
        report_dir: Path to the report directory
        
    Returns:
        Tuple of (successful_count, failed_count)
    """
    report_path = Path(report_dir)
    
    if not report_path.exists():
        print(f"❌ Directory not found: {report_dir}")
        return 0, 0
    
    if not report_path.is_dir():
        print(f"❌ Not a directory: {report_dir}")
        return 0, 0
    
    # Find all index.html files and their corresponding JSON files
    html_files = list(report_path.glob("**/index.html"))
    
    if not html_files:
        print(f"❌ No index.html files found in: {report_dir}")
        return 0, 0
    
    print(f"\n🔍 Found {len(html_files)} HTML report(s) in {report_dir}")
    print("=" * 70)
    
    successful = 0
    failed = 0
    
    for html_file in html_files:
        # Look for corresponding JSON file in the same directory
        json_files = list(html_file.parent.glob("temp_results_*.json"))
        
        if not json_files:
            print(f"  ⚠️  {html_file} - No JSON file found, skipping")
            failed += 1
            continue
        
        # Use the first (and typically only) JSON file
        json_file = json_files[0]
        
        if fix_html_report(str(html_file), str(json_file)):
            successful += 1
        else:
            failed += 1
    
    return successful, failed


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    report_dir = sys.argv[1]
    
    print("\n" + "=" * 70)
    print("🔧 HTML Report CORS Fix Utility")
    print("=" * 70)
    
    successful, failed = fix_report_directory(report_dir)
    
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"  ✅ Successfully fixed: {successful}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📁 Total processed: {successful + failed}")
    print()
    
    if successful > 0:
        print("✨ Done! You can now open the HTML reports in your browser.")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()

