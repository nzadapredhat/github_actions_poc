# GitHub Actions Setup Guide

## 🎯 Quick Start

Your repository now has 2 automated GitHub Actions workflows ready to use! This guide will help you get everything set up and running.

## 📦 What's Been Created

### Workflow Files (in `.github/workflows/`)
1. ✅ **ci.yml** - Main CI pipeline for running tests
2. ✅ **publish-reports.yml** - GitHub Pages report publishing

## 🚀 Setup Steps

### Step 1: Push to GitHub
```bash
git add .github/
git commit -m "Add GitHub Actions workflows"
git push origin main
```

### Step 2: Enable GitHub Actions
1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. GitHub Actions should be enabled by default
4. You'll see the workflows listed

### Step 3: Enable GitHub Pages (Optional but Recommended)
To publish HTML test reports publicly:

1. Go to **Settings** → **Pages**
2. Under "Source", select **"GitHub Actions"**
3. Save the settings
4. After the first successful CI run, reports will be published

### Step 4: Configure Workflow Permissions
For the publish-reports workflow to work:

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **"Workflow permissions"**
3. Select **"Read and write permissions"**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Save

### Step 5: Test Your First Workflow Run
```bash
# Method 1: Push a change
echo "# Testing GitHub Actions" >> test.txt
git add test.txt
git commit -m "Test GitHub Actions"
git push origin main

# Method 2: Manual trigger
# Go to Actions → Select "CI - Test Next Gen UI Agent" → Click "Run workflow"
```

## 📊 What Each Workflow Does

### 🔄 CI - Test Next Gen UI Agent
- **Runs:** On every push/PR to main or develop
- **What it does:**
  - Sets up Python 3.13
  - Installs dependencies from requirements.txt
  - Runs your test suite (main.py)
  - Uploads test reports as artifacts
  - Generates test summary
- **Duration:** ~5-10 minutes
- **Artifacts:** Test reports (HTML + JSON) retained for 30 days

### 📄 Publish Test Reports
- **Runs:** Automatically after successful CI workflow
- **What it does:**
  - Downloads test artifacts from CI run
  - Publishes to GitHub Pages
  - Creates beautiful report index page
- **Duration:** ~1-2 minutes
- **Result:** Public URL to view all test reports

## 🎮 Using the Workflows

### Running Tests Manually
1. Go to **Actions** tab
2. Select **"CI - Test Next Gen UI Agent"**
3. Click **"Run workflow"**
4. Select branch (usually `main`)
5. Click **"Run workflow"** button

### Viewing Test Reports

#### Method 1: Download Artifacts
1. Go to the workflow run in Actions tab
2. Scroll to **"Artifacts"** section at the bottom
3. Download `test-reports-python-3.13.zip`
4. Extract and open `index.html` in a browser

#### Method 2: GitHub Pages (Recommended)
1. After CI completes successfully, reports auto-publish
2. Visit: `https://[your-username].github.io/[repo-name]/`
3. Browse all historical reports in one place

## 🔧 Customization

### Change Test Dataset
By default, the CI runs with `toy_story_dataset_120.json`. To use a different dataset:

**Option 1:** Edit main.py directly
```python
# Change line 19 in main.py:
with open("testdata/toy_story_dataset_10.json", 'r') as file:
```

**Option 2:** Modify the CI workflow
Add this step before running tests in `ci.yml`:
```yaml
- name: Use smaller dataset for faster CI
  run: |
    sed -i 's/toy_story_dataset_120.json/toy_story_dataset_5.json/' main.py
```

### Adjust Workflow Triggers
Edit `.github/workflows/ci.yml` to change when tests run:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add more branches
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 9 * * 1'  # Run every Monday at 9 AM
```

## 📈 Monitoring & Badges

### Add Status Badge to README
Add this to the top of your `README.md`:

```markdown
[![CI Tests](https://github.com/[username]/[repo]/workflows/CI%20-%20Test%20Next%20Gen%20UI%20Agent/badge.svg)](https://github.com/[username]/[repo]/actions)
```

Replace `[username]` and `[repo]` with your actual values.

### View Workflow History
- Go to **Actions** tab
- Select a workflow to see all runs
- View pass/fail rates over time
- Download historical artifacts (available for 30 days)

## 🐛 Troubleshooting

### ❌ "Workflow not found"
**Solution:** Ensure files are in `.github/workflows/` directory and pushed to GitHub

### ❌ "Permission denied" for publishing
**Solution:** 
1. Go to Settings → Actions → General
2. Enable "Read and write permissions"
3. Re-run the workflow

### ❌ "Pages deployment failed"
**Solution:** 
1. Enable GitHub Pages in Settings → Pages
2. Set source to "GitHub Actions"
3. Ensure workflow has correct permissions

### ❌ "Tests fail in CI but work locally"
**Possible causes:**
- Python version mismatch (CI uses 3.13, check your local version)
- Missing dependencies in requirements.txt
- Environment variables not set in CI
- LLM model not accessible in CI environment

**Solution:** Check the workflow logs for specific error messages

### ❌ "Artifacts not uploading"
**Solution:**
- Check if `AI_Reports/` directory is being created
- Verify tests are actually running
- Look at workflow logs for artifact upload errors

## 🔒 Security Best Practices

### Using Secrets for API Keys
If your tests need API keys or tokens:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add your secret (e.g., `LLM_API_KEY`, `OPENAI_API_KEY`)
4. Use in workflow:

```yaml
- name: Run tests
  run: python main.py
  env:
    API_KEY: ${{ secrets.LLM_API_KEY }}
```

Then access in your Python code:
```python
import os
api_key = os.environ.get('API_KEY')
```

## 📚 Next Steps

1. ✅ Push workflows to GitHub
2. ✅ Enable GitHub Pages for report hosting
3. ✅ Configure workflow permissions
4. ✅ Run first test workflow
5. ✅ Add status badge to README.md
6. ✅ Set up any needed secrets
7. ✅ Customize test dataset if needed

## 💡 Tips & Best Practices

- **Start small**: Test with `toy_story_dataset_5.json` first to verify everything works
- **Monitor costs**: GitHub Actions is free for public repos (2000 min/month for private)
- **Use artifacts**: Download test reports for detailed analysis
- **Check logs**: Click on any failed step to see detailed error messages
- **Iterate quickly**: Workflows can be updated anytime by editing and pushing changes

## 🎯 Workflow Behavior

### What Triggers a Test Run?
- ✅ Every push to `main` or `develop` branch
- ✅ Every pull request to `main` or `develop`
- ✅ Manual trigger via "Run workflow" button

### What Happens During a Test Run?
1. GitHub Actions spins up an Ubuntu VM
2. Python 3.13 is installed
3. Dependencies are installed from requirements.txt
4. Your test suite runs (main.py)
5. Test reports are generated in AI_Reports/
6. Reports are uploaded as artifacts
7. Summary is displayed in the Actions tab

### After Tests Complete
1. Artifacts are available for download (30 days)
2. If successful, publish-reports workflow triggers
3. Reports are published to GitHub Pages
4. You can view reports at your GitHub Pages URL

## 🆘 Need Help?

- 📖 [GitHub Actions Documentation](https://docs.github.com/en/actions)
- 📖 [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- 📖 [GitHub Pages Documentation](https://docs.github.com/en/pages)
- 📖 [Troubleshooting Workflows](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows)

---

**Happy Testing! 🚀**

Your Next Gen UI Agent Testing Framework is now automated and ready for continuous integration!
