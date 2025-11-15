# Report Templates

This directory contains HTML templates for test report generation.

## Files

- `report_template.html` - Base HTML template for individual test run reports. This template is copied to each report directory and customized with the specific test run data.

## Usage

The `report_generator.py` script uses these templates when generating HTML reports for test runs. The template is:

1. Copied to the test run directory (e.g., `AI_Reports/report_TIMESTAMP_MODEL/`)
2. Modified to reference the specific JSON results file for that run
3. Served as an interactive report showing test results with filtering and search capabilities

## Important Notes

- **Do not delete this directory** - It is required for GitHub Actions CI/CD to work properly
- These templates are committed to version control (not in `.gitignore`)
- The `AI_Reports/` directory itself is gitignored, but these templates must be tracked
- Any changes to the template will affect all future test reports

