# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the Next Gen UI Agent Testing Framework.

## 📋 Available Workflows

### 1. CI - Test Next Gen UI Agent (`ci.yml`)
**Trigger:** Push/PR to `main` or `develop` branches, Manual

**Purpose:** Main continuous integration workflow that runs tests and validates the application.

**Features:**
- ✅ Runs on Python 3.13
- ✅ Installs all dependencies from requirements.txt
- ✅ Executes the test suite
- ✅ Uploads test reports as artifacts
- ✅ Generates test summaries
- ✅ Continues even if tests fail (for reporting purposes)

**Artifacts Generated:**
- `test-reports-python-*`: Complete test reports (HTML + JSON)
- `test-results-json-*`: JSON test results only

---

### 2. Publish Test Reports (`publish-reports.yml`)
**Trigger:** After successful CI workflow completion, Manual

**Purpose:** Publishes HTML test reports to GitHub Pages for easy viewing.

**Features:**
- ✅ Automatically triggered after CI success
- ✅ Downloads test report artifacts
- ✅ Publishes to GitHub Pages
- ✅ Creates beautiful index page listing all reports
- ✅ Provides public URL for report access

**Setup Required:**
1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Grant workflow permissions: `Settings → Actions → General → Workflow permissions → Read and write permissions`

---

## 🚀 Getting Started

### Prerequisites
1. Enable GitHub Actions in your repository
2. Ensure you have Python 3.13 support
3. For GitHub Pages publishing, enable Pages in repository settings

### Using the Workflows

#### Running Tests on Push
Simply push to `main` or `develop` branch:
```bash
git push origin main
```

#### Manual Test Execution
1. Go to "Actions" tab in GitHub
2. Select "CI - Test Next Gen UI Agent"
3. Click "Run workflow"
4. Select branch and run

---

## 📊 Viewing Results

### Test Reports
1. **Via Artifacts**: 
   - Go to workflow run
   - Scroll to "Artifacts" section
   - Download zip files

2. **Via GitHub Pages** (if enabled):
   - Navigate to `https://<username>.github.io/<repository>/`
   - View interactive HTML reports

### Test Summaries
- Each workflow run includes a summary in the "Summary" section
- Shows pass/fail counts, pass rates, and artifacts

---

## 🔧 Customization

### Modify Test Dataset in CI
Edit `ci.yml` to change which test dataset to use:
```yaml
# In main.py, change the dataset file
# Default: toy_story_dataset_120.json
# Options: toy_story_dataset_5.json, toy_story_dataset_10.json, toy_story_dataset_120.json
```

Or modify the workflow to use a different dataset:
```yaml
- name: Use smaller dataset for faster CI
  run: |
    sed -i 's/toy_story_dataset_120.json/toy_story_dataset_10.json/' main.py
```

---

## 🛡️ Security

### Secrets Management
If you need to add API keys or secrets:
1. Go to `Settings → Secrets and variables → Actions`
2. Add repository secrets
3. Reference in workflows:
```yaml
env:
  API_KEY: ${{ secrets.YOUR_API_KEY }}
```

---

## 📝 Workflow Status Badges

Add these to your README.md to show workflow status:

```markdown
![CI](https://github.com/<username>/<repo>/workflows/CI%20-%20Test%20Next%20Gen%20UI%20Agent/badge.svg)
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Tests fail in CI but work locally
- **Solution**: Check Python version, dependencies, and environment variables

**Issue:** GitHub Pages not deploying
- **Solution**: Verify Pages is enabled and workflow has correct permissions

**Issue:** Artifacts not uploading
- **Solution**: Check artifact paths and ensure directories exist

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Setup](https://docs.github.com/en/pages)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Using Artifacts](https://docs.github.com/en/actions/guides/storing-workflow-data-as-artifacts)

---

**Last Updated:** 2025-11-15
