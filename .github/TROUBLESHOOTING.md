# Troubleshooting Guide

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

