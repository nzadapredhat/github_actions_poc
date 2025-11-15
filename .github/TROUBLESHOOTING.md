# Troubleshooting Guide

## Model Not Found Error (404)

### Problem
The following error occurs when running tests in GitHub Actions:
```
Error code: 404 - {'error': {'message': "model 'llama3.2' not found", 'type': 'api_error', 'param': None, 'code': None}}
openai.NotFoundError: Error code: 404 - {'error': {'message': "model 'llama3.2' not found"...
```

### Root Cause
The `next-gen-ui-langgraph` package has a hardcoded model name (e.g., `llama3.2`) in the `movies_agent`, but the GitHub Actions workflow was configured to pull a different model (e.g., `granite3.1-dense:2b`). The `llm_model` variable in `main.py` is only used for reporting purposes, not for configuring which model the agent actually uses.

### Solution
Update the GitHub Actions workflow to pull the correct model that matches what the `next-gen-ui-langgraph` package expects:

1. **Update the cache key** in `.github/workflows/test-and-publish.yml`:
   ```yaml
   key: ollama-${{ runner.os }}-llama3.2-v1
   restore-keys: |
     ollama-${{ runner.os }}-llama3.2-
   ```

2. **Update the model pull command**:
   ```bash
   if ollama list | grep -q "llama3.2"; then
     echo "Model llama3.2 already available (from cache)"
   else
     echo "Pulling llama3.2 model..."
     ollama pull llama3.2
   fi
   ```

3. **Update `main.py`** to match (for reporting consistency):
   ```python
   llm_model = "llama3.2"
   ```

### How to Identify the Required Model
If you encounter this error with a different model name:
1. Check the error message for the model name (e.g., `"model 'MODEL_NAME' not found"`)
2. Update the workflow to pull that specific model
3. The model name must match exactly what Ollama expects (check [Ollama's model library](https://ollama.com/library))

### Alternative: Configure the Package
If the `next-gen-ui-langgraph` package supports model configuration via environment variables:
```yaml
env:
  LLM_MODEL: "your-preferred-model"
```

Check the package documentation for available configuration options.

## CORS Error When Viewing Downloaded Reports

### Problem
When opening downloaded HTML reports in a browser, you see an error:
```
Access to fetch at 'file:///path/to/temp_results_*.json' from origin 'null' has been blocked by CORS policy
```

The report displays "Loading test results..." indefinitely and never shows the actual data.

### Root Cause
Browsers block JavaScript `fetch()` requests when viewing files using the `file://` protocol for security reasons. The HTML report tries to load the JSON data file via AJAX, which is blocked by the browser's CORS (Cross-Origin Resource Sharing) policy.

### Solution 1: Automatic Fix (For New Reports)
As of the latest update, the report generator automatically embeds JSON data directly into HTML reports, eliminating CORS issues. Reports generated after this update will work perfectly when opened locally.

To get the fixed version:
1. Pull the latest code changes
2. Re-run your tests to generate new reports
3. The new reports will work without CORS errors

### Solution 2: Fix Downloaded Reports (Existing Reports)
For reports you've already downloaded that have the CORS issue, use the fix utility script:

```bash
# Navigate to your project directory
cd /path/to/GitHub_Actions

# Fix a single report directory
python fix_downloaded_reports.py ~/Downloads/artifact/report_20251115_135705_llama3.2/

# Or fix all reports in the AI_Reports directory
python fix_downloaded_reports.py AI_Reports/
```

The script will:
- Find all `index.html` files and their corresponding JSON data
- Embed the JSON data directly into the HTML files
- Allow you to view the reports without CORS errors

### Solution 3: Use a Local Web Server (Alternative)
If you prefer not to modify the files, you can serve them through a local web server:

```bash
# Navigate to the report directory
cd ~/Downloads/artifact/report_20251115_135705_llama3.2/

# Start a simple Python web server
python3 -m http.server 8000

# Open in browser: http://localhost:8000/index.html
```

### Solution 4: Browser Extension
Some browsers allow you to disable CORS checks for local files, but this is **not recommended** for security reasons.

### Technical Details
The fix works by:
1. Reading the JSON data file
2. Converting it to a JavaScript variable
3. Embedding it directly in the HTML `<script>` section
4. Replacing the `fetch()` call with direct data assignment

This makes the report completely self-contained and viewable anywhere without needing to fetch external files.

## Connection Error in GitHub Actions

### Problem
The following error occurs when running tests in GitHub Actions:
```
httpcore.ConnectError: [Errno 111] Connection refused
openai.APIConnectionError: Connection error.
```

### Root Cause
The LLM client (configured in `next-gen-ui-langgraph`) is trying to connect to a local Ollama instance at `http://localhost:11434`, which is not available in the GitHub Actions environment by default.

### Solution Implemented
We've added Ollama installation and setup to the GitHub Actions workflow:

1. **Install Ollama** - Downloads and installs Ollama on the runner
2. **Start Ollama Service** - Runs Ollama in the background
3. **Wait for Ready** - Ensures Ollama is fully started before proceeding
4. **Pull Model** - Downloads the `granite3.1-dense:2b` model
5. **Set Environment Variables** - Configures the OpenAI client to use Ollama

### Environment Variables Set
- `OPENAI_API_BASE`: `http://localhost:11434/v1` - Points to local Ollama instance
- `OPENAI_API_KEY`: `ollama` - Placeholder key (Ollama doesn't require authentication)

### Workflow Changes
See `.github/workflows/test-and-publish.yml`:
- Added "Install and start Ollama" step
- Added environment variables to "Run tests" step
- Added "Check Ollama status" step for debugging

## Alternative Solutions

If Ollama doesn't work well in GitHub Actions (slow downloads, resource constraints), consider:

### Option 1: Use OpenAI API
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  # Remove OPENAI_API_BASE to use default OpenAI endpoint
```

And update the model in `main.py`:
```python
llm_model = "gpt-4"  # or "gpt-3.5-turbo"
```

### Option 2: Use Azure OpenAI
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
  OPENAI_API_BASE: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
  OPENAI_API_VERSION: "2024-02-01"
```

### Option 3: Mock LLM for Testing
Create a mock implementation for CI/CD that doesn't require actual LLM calls:
```python
if os.getenv('CI') == 'true':
    # Use mock LLM for testing
    pass
```

### Option 4: Use Smaller/Faster Model
If Ollama is slow, try a smaller model:
```python
llm_model = "granite3.1-dense:1b"  # or "llama2:3b"
```

## Debugging Tips

### Check Ollama Logs
The workflow captures Ollama logs in the "Check Ollama status" step. Review these if tests fail.

### Verify Model Availability
The workflow runs `ollama list` after pulling the model. Check this output to ensure the model downloaded successfully.

### Test Locally with Docker
Replicate the GitHub Actions environment locally:
```bash
docker run -it ubuntu:latest bash
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > /tmp/ollama.log 2>&1 &
ollama pull granite3.1-dense:2b
# Run your tests
```

### Check Resource Usage
Large models may exceed GitHub Actions runner resources:
- GitHub Actions runners have 2 CPU cores and 7GB RAM
- Some models may be too large or slow for this environment

## Configuration in next-gen-ui-langgraph

The `next-gen-ui-langgraph` package should respect these environment variables:
- `OPENAI_API_BASE` or `OPENAI_BASE_URL`
- `OPENAI_API_KEY`

If it doesn't, you may need to:
1. Check the package documentation for configuration options
2. Modify the import/initialization in `main.py`
3. Create a wrapper configuration file

## GitHub Actions Secrets

To use external APIs, add secrets to your repository:
1. Go to Settings → Secrets and variables → Actions
2. Add `OPENAI_API_KEY` or other required secrets
3. Reference them in the workflow with `${{ secrets.SECRET_NAME }}`

## Performance Considerations

### Model Download Time
The `granite3.1-dense:2b` model may take 5-10 minutes to download on first run. Consider:
- Using GitHub Actions caching for the Ollama models
- Using a smaller model for CI/CD
- Only running full tests on specific triggers (release, manual)

### Caching Ollama Models
Add this to cache the model between runs:
```yaml
- name: Cache Ollama models
  uses: actions/cache@v3
  with:
    path: ~/.ollama
    key: ollama-${{ runner.os }}-granite3.1-dense-2b
```

## Monitoring

Monitor workflow runs for:
- Ollama startup time
- Model download time
- Test execution time
- Memory usage warnings

If tests are too slow or fail frequently, consider the alternative solutions above.

