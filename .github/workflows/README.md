# GitHub Actions Workflows

This directory contains the automated CI/CD workflow for the Next Gen UI Agent Testing Framework.

## 📋 Workflow

### Test and Publish Reports (`test-and-publish.yml`)

**Trigger:** Push/PR to `main` or `develop` branches, Manual

**Purpose:** All-in-one workflow that runs tests and publishes results to GitHub Pages.

**Jobs:**

#### 1. Test Job
- ✅ Runs on Python 3.13
- ✅ Installs all dependencies from requirements.txt
- ✅ Executes the test suite
- ✅ Uploads test reports as artifacts (30-day retention)
- ✅ Generates detailed test summaries with pass/fail counts
- ✅ Continues even if tests fail (for reporting purposes)

#### 2. Publish Job
- ✅ Automatically runs after test job completes
- ✅ Only triggers on push to main/develop (not on PRs)
- ✅ Downloads test reports from test job
- ✅ Publishes to GitHub Pages
- ✅ Creates beautiful index page listing all reports

**Artifacts Generated:**
- `test-reports-python-3.13`: Complete test reports (HTML + JSON) - retained for 30 days

---

## 🚀 Getting Started

### Prerequisites
1. Enable GitHub Actions in your repository
2. Ensure you have Python 3.13 support
3. For GitHub Pages publishing, enable Pages in repository settings

### Using the Workflow

#### Running Tests on Push
Simply push to `main` or `develop` branch:
```bash
git push origin main
```

This will:
1. Run all tests
2. Upload artifacts
3. Publish reports to GitHub Pages (if enabled)

#### Manual Test Execution
1. Go to "Actions" tab in GitHub
2. Select "Test and Publish Reports"
3. Click "Run workflow"
4. Select branch and run

---

## 📊 Viewing Results

### Test Reports

**Method 1: Via Artifacts**
- Go to workflow run
- Scroll to "Artifacts" section
- Download `test-reports-python-3.13.zip`
- Extract and open HTML files

**Method 2: Via GitHub Pages (Recommended)**
- Navigate to `https://<username>.github.io/<repository>/`
- View interactive HTML reports
- Browse all historical reports
- No download needed

### Test Summaries
Each workflow run includes a summary in the "Summary" section showing:
- Total tests executed
- Passed/Failed counts
- Pass rate percentage
- Links to artifacts

---

## 🔧 Customization

### Change Test Dataset
Modify which test dataset to use by editing `main.py`:

```python
# Line 19 in main.py:
with open("testdata/toy_story_dataset_10.json", 'r') as file:
```

Available datasets:
- `toy_story_dataset_5.json` - Quick validation (5 tests)
- `toy_story_dataset_10.json` - Medium run (10 tests)
- `toy_story_dataset_120.json` - Full suite (120 tests)

### Adjust Workflow Triggers
Edit `test-and-publish.yml` to change when tests run:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add more branches
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 9 * * 1'  # Add scheduled runs (e.g., every Monday at 9 AM)
```

### Disable GitHub Pages Publishing
To only run tests without publishing to GitHub Pages:

1. Comment out or remove the `publish` job in `test-and-publish.yml`
2. Or modify the condition: `if: false` in the publish job

---

## 🛡️ Security

### Secrets Management
If you need to add API keys or secrets:
1. Go to `Settings → Secrets and variables → Actions`
2. Add repository secrets
3. Reference in workflow:

```yaml
- name: Run tests
  run: python main.py
  env:
    API_KEY: ${{ secrets.YOUR_API_KEY }}
```

---

## 📝 Workflow Status Badge

Add this to your README.md to show workflow status:

```markdown
[![Tests](https://github.com/<username>/<repo>/workflows/Test%20and%20Publish%20Reports/badge.svg)](https://github.com/<username>/<repo>/actions)
```

Replace `<username>` and `<repo>` with your actual values.

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Tests fail in CI but work locally
- **Solution**: Check Python version (CI uses 3.13), dependencies, and environment variables

**Issue:** GitHub Pages not deploying
- **Solution**: 
  - Verify Pages is enabled (Settings → Pages)
  - Set source to "GitHub Actions"
  - Check workflow has proper permissions (Settings → Actions → General → Read and write permissions)

**Issue:** Artifacts not uploading
- **Solution**: Check artifact paths and ensure AI_Reports directory is created

**Issue:** Publish job not running
- **Solution**: 
  - Publish only runs on push to main/develop, not on PRs
  - Check if test job completed successfully
  - Verify GitHub Pages is enabled

---

## 💡 How It Works

### Workflow Flow

```
Push to main/develop
    ↓
Test Job runs
    ├─ Setup Python 3.13
    ├─ Install dependencies
    ├─ Run tests (main.py)
    ├─ Generate reports
    ├─ Upload artifacts
    └─ Create summary
    ↓
Publish Job runs (only on push, not PRs)
    ├─ Download test reports
    ├─ Prepare GitHub Pages content
    ├─ Create index page
    ├─ Upload to Pages
    └─ Deploy to GitHub Pages
    ↓
Reports available at:
    • Artifacts (download)
    • GitHub Pages (view online)
```

### Key Features

- ✅ **Single Workflow**: One file for both testing and publishing
- ✅ **Smart Publishing**: Only publishes on push to main/develop, not on PRs
- ✅ **Always Reports**: Uploads artifacts even if tests fail
- ✅ **Detailed Summaries**: Shows pass/fail counts and percentages
- ✅ **30-Day Retention**: Artifacts available for download for 30 days

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Setup](https://docs.github.com/en/pages)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Using Artifacts](https://docs.github.com/en/actions/guides/storing-workflow-data-as-artifacts)

---

**Last Updated:** 2025-11-15
