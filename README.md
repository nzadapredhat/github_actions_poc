# Next Gen UI Agent Testing Framework

A comprehensive testing framework for evaluating LLM-based UI component selection and generation. This project validates the Next Gen UI Agent's ability to correctly identify and generate appropriate UI components based on user prompts.

## 🎯 Overview

This framework tests the Next Gen UI Agent by:
- Processing user prompts from test datasets
- Comparing expected vs. actual UI component selections
- Generating detailed HTML reports with test results
- Supporting multiple LLM models for testing
- Tracking test metrics and performance

## ✨ Features

- **Automated Testing**: Batch processing of test datasets with comprehensive error handling
- **HTML Report Generation**: Beautiful, interactive HTML reports with test results visualization
- **Multiple LLM Support**: Configurable LLM models for testing different AI backends
- **Detailed Logging**: Comprehensive logging system for debugging and analysis
- **Test Metrics**: Automatic calculation of pass rates, success metrics, and detailed results
- **Error Tracking**: Captures exceptions, tracebacks, and error details for failed tests
- **Timestamped Results**: All test runs are timestamped for easy tracking and comparison

## 📋 Prerequisites

- Python 3.13 or higher
- Virtual environment (recommended)
- Access to LLM models (currently configured for granite3.1-dense:2b)

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd GitHub_Actions
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv path/to/venv
source path/to/venv/bin/activate  # On macOS/Linux
# or
path\to\venv\Scripts\activate     # On Windows
```

3. **Install dependencies**:
```bash
pip install next-gen-ui-langgraph
pip install next-gen-ui-agent
pip install smart-assertions
pip install pydantic
pip install pyyaml
pip install jsonpath-ng
```

## 📦 Project Structure

```
GitHub_Actions/
├── main.py                    # Main test execution script
├── report_generator.py        # HTML report generation utilities
├── utils/
│   ├── __init__.py
│   └── logger.py             # Logging configuration
├── testdata/
│   ├── toy_story_dataset_5.json
│   ├── toy_story_dataset_10.json
│   └── toy_story_dataset_120.json
├── AI_Reports/               # Generated test reports
│   ├── index.html           # Base HTML template
│   └── report_*/            # Individual test run directories
└── path/to/venv/            # Virtual environment
```

## 🎮 Usage

### Basic Execution

Run the test suite with the default configuration:

```bash
python main.py
```

### Configuration

Modify the LLM model in `main.py`:

```python
llm_model = "granite3.1-dense:2b"  # Change to your preferred model
```

Select a test dataset:

```python
with open("testdata/toy_story_dataset_120.json", 'r') as file:
    data = json.load(file)
```

Available datasets:
- `toy_story_dataset_5.json` - 5 test cases
- `toy_story_dataset_10.json` - 10 test cases
- `toy_story_dataset_120.json` - 120 test cases

### Test Data Format

Test datasets should follow this JSON structure:

```json
[
  {
    "Prompt": "User input prompt text",
    "expected_component": "ExpectedComponentName"
  }
]
```

## 📊 Reports

After each test run, the framework generates:

1. **JSON Results File**: `temp_results_<timestamp>.json`
   - Contains detailed test results
   - Includes timestamps, status, and error information
   - Located in `AI_Reports/report_<timestamp>_<model>/`

2. **HTML Report**: `index.html`
   - Interactive visualization of test results
   - Displays pass/fail statistics
   - Shows individual test details
   - Accessible via web browser

### Report Location

Reports are organized by timestamp and model:
```
AI_Reports/
└── report_20251115_003411_granite3.1-dense_2b/
    ├── index.html
    └── temp_results_20251115_003411.json
```

## 🔍 Test Results

Each test result includes:

- **user_prompt**: The input prompt used for testing
- **expected_component**: The expected UI component
- **actual_results**: The component selected by the LLM
- **status**: Pass/fail status (boolean)
- **llm_model**: Model used for the test
- **timestamp**: ISO format timestamp
- **error** (if failed): Error message
- **exception_type** (if failed): Exception class name
- **traceback** (if failed): Full error traceback

### Sample Output

```
============================================================
TEST SUMMARY
Total Tests: 120
Passed: 115
Failed: 5
Pass Rate: 95.83%
Results saved to: AI_Reports/report_20251115_003411_granite3.1-dense_2b/temp_results_20251115_003411.json
HTML Report: AI_Reports/report_20251115_003411_granite3.1-dense_2b/index.html
============================================================
```

## 🛠️ Key Components

### main.py
Main test execution script that:
- Loads test datasets
- Invokes the movie agent and NGUI agent
- Compares expected vs. actual results
- Generates comprehensive test reports
- Logs test summaries and metrics

### report_generator.py
Report generation utilities including:
- `create_report_directory()`: Creates timestamped report directories
- `setup_html_report()`: Configures HTML report templates
- `sanitize_model_name()`: Ensures model names are filesystem-safe

### utils/logger.py
Logging configuration providing:
- Standardized logging format
- Console output with timestamps
- Debug, info, warning, and error level support

## 🐛 Debugging

The framework includes comprehensive error handling:

```python
# Logs are written to console with detailed formatting
logger.info("Starting test execution")
logger.error("Error message", exc_info=True)
```

Enable debug logging to see detailed execution flow:
```python
logger.setLevel(logging.DEBUG)
```

## 🔧 Troubleshooting

**Issue**: HTML report not generated
- **Solution**: Ensure `AI_Reports/index.html` template exists

**Issue**: Import errors for next_gen_ui packages
- **Solution**: Verify virtual environment is activated and packages are installed

**Issue**: LLM model not found
- **Solution**: Check model availability and configuration

## 📝 License

[Specify your license here]

## 👥 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Contact

**Nachiket Zadap**

## 🙏 Acknowledgments

- Next Gen UI Agent framework
- LangGraph for agent orchestration
- Smart Assertions for soft assertion support

---

**Note**: This framework is designed for testing and validating LLM-based UI component selection. Ensure you have proper access to LLM models before running tests.

