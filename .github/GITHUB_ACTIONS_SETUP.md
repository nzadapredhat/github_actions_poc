# GitHub Actions Setup Guide

## 🎯 Quick Start

Your repository now has a single automated GitHub Actions workflow that handles both testing and report publishing!

## 📦 What's Been Created

### Workflow File (in `.github/workflows/`)
✅ **test-and-publish.yml** - All-in-one workflow for testing and publishing

**What it does:**
- Runs Python tests automatically
- Uploads test reports as artifacts
- Publishes reports to GitHub Pages
- Generates detailed summaries

---

## 🚀 Setup Steps

### Step 1: Push to GitHub
```bash
git add .github/
git commit -m "Add GitHub Actions workflow for testing and reporting"
git push origin main
```

### Step 2: Verify Workflow is Running
1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see the workflow running automatically
4. Click on the workflow run to see progress

### Step 3: Enable GitHub Pages (Optional but Recommended)
To publish HTML test reports publicly:

1. Go to **Settings** → **Pages**
2. Under "Source", select **"GitHub Actions"**
3. Click **Save**
4. After the workflow completes, your reports will be available at `https://[username].github.io/[repo-name]/`

### Step 4: Configure Workflow Permissions
For GitHub Pages publishing to work:

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **"Workflow permissions"**
3. Select **"Read and write permissions"**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**

---

## 📊 What Happens When You Push

### Automatic Workflow Execution

```
You push code
    ↓
Test Job
  • Sets up Python 3.13
  • Installs dependencies
  • Runs your test suite
  • Uploads artifacts
  • Creates summary
    ↓
Publish Job (only on main/develop push)
  • Downloads reports
  • Publishes to GitHub Pages
  • Creates index page
    ↓
Done!
  • View artifacts in Actions tab
  • View reports on GitHub Pages
```

### What Gets Generated

**Test Reports (Artifacts):**
- HTML reports with test results
- JSON files with detailed data
- Available for download for 30 days

**GitHub Pages:**
- Public website with all reports
- Beautiful index page
- Historical reports tracking

**Test Summary:**
- Total tests executed
- Passed/Failed counts
- Pass rate percentage

---

## 🎮 Using the Workflow

### Automatic Execution
The workflow runs automatically on:
- ✅ Every push to `main` branch
- ✅ Every push to `develop` branch
- ✅ Every pull request to `main` or `develop`

**Note:** GitHub Pages publishing only happens on push to main/develop, NOT on pull requests.

### Manual Execution
1. Go to **Actions** tab in GitHub
2. Select **"Test and Publish Reports"**
3. Click **"Run workflow"**
4. Select branch (usually `main`)
5. Click green **"Run workflow"** button

---

## 📈 Viewing Test Reports

### Method 1: Download Artifacts (Always Available)

1. Go to **Actions** tab
2. Click on any workflow run
3. Scroll to bottom → **"Artifacts"** section
4. Download `test-reports-python-3.13.zip`
5. Extract and open `index.html` in browser

**Pros:** Always available, works immediately  
**Retention:** 30 days

### Method 2: GitHub Pages (Recommended)

1. Enable GitHub Pages (see Step 3 above)
2. After workflow completes, visit:  
   `https://[your-username].github.io/[repo-name]/`
3. Browse all reports in one place

**Pros:** No download needed, beautiful UI, historical tracking  
**Requirement:** GitHub Pages must be enabled

---

## 🔧 Customization

### Change Test Dataset

By default, the workflow runs all tests from your `main.py` configuration. To use a different dataset:

**Option 1: Edit main.py**
```python
# Line 19 in main.py:
with open("testdata/toy_story_dataset_10.json", 'r') as file:
```

**Option 2: Add a workflow step**
Edit `test-and-publish.yml` and add before "Run tests":
```yaml
- name: Use smaller dataset for faster CI
  run: |
    sed -i 's/toy_story_dataset_120.json/toy_story_dataset_5.json/' main.py
```

### Add More Branches

Edit `test-and-publish.yml`:
```yaml
on:
  push:
    branches: [ main, develop, staging, production ]  # Add more
```

### Add Scheduled Runs

Edit `test-and-publish.yml`:
```yaml
on:
  push:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM UTC
```

Common cron patterns:
- `0 */6 * * *` - Every 6 hours
- `0 9 * * 1-5` - Weekdays at 9 AM
- `0 0 * * 0` - Every Sunday at midnight

---

## 📝 Add Status Badge to README

Show your workflow status with a badge! Add this to your `README.md`:

```markdown
[![Tests](https://github.com/[username]/[repo]/workflows/Test%20and%20Publish%20Reports/badge.svg)](https://github.com/[username]/[repo]/actions)
```

Replace `[username]` and `[repo]` with your actual GitHub username and repository name.

Example:
```markdown
[![Tests](https://github.com/nzadap/GitHub_Actions/workflows/Test%20and%20Publish%20Reports/badge.svg)](https://github.com/nzadap/GitHub_Actions/actions)
```

---

## 🐛 Troubleshooting

### ❌ Workflow not appearing in Actions tab

**Solution:** 
- Ensure file is in `.github/workflows/` directory
- File must have `.yml` or `.yaml` extension
- Push to GitHub to activate

### ❌ Tests fail in CI but work locally

**Possible causes:**
- Python version mismatch (CI uses 3.13)
- Missing dependencies in requirements.txt
- Environment variables not set
- File paths different in CI

**Solution:** 
1. Check workflow logs for specific errors
2. Verify Python version: `python --version`
3. Ensure all dependencies are in requirements.txt
4. Check file paths are relative, not absolute

### ❌ GitHub Pages not deploying

**Common issues:**

1. **Pages not enabled**
   - Go to Settings → Pages
   - Set source to "GitHub Actions"
   - Save

2. **Permission denied**
   - Settings → Actions → General
   - Enable "Read and write permissions"
   - Save and re-run workflow

3. **Publish job skipped**
   - Publish only runs on push to main/develop
   - PRs do NOT trigger publishing (by design)
   - Check if test job succeeded

### ❌ Artifacts not uploading

**Solution:**
- Check if `AI_Reports/` directory exists after tests
- Look at workflow logs for "Upload test reports" step
- Verify tests actually ran and generated reports

### ❌ "No reports available" on GitHub Pages

**This is normal if:**
- First time setup (run workflow once first)
- Tests failed and generated no reports
- Reports folder is empty

**Solution:** Run the workflow successfully at least once

---

## 🔒 Security & Secrets

### Using API Keys or Tokens

If your tests need API keys:

1. **Add Secret to GitHub:**
   - Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `API_KEY` (or any name)
   - Value: Your actual API key
   - Click "Add secret"

2. **Use in Workflow:**
   Edit `test-and-publish.yml`:
   ```yaml
   - name: Run tests
     run: python main.py
     env:
       API_KEY: ${{ secrets.API_KEY }}
       LLM_TOKEN: ${{ secrets.LLM_TOKEN }}
   ```

3. **Access in Python:**
   ```python
   import os
   api_key = os.environ.get('API_KEY')
   ```

---

## 💡 Best Practices

### 1. Start with Small Dataset
- Use `toy_story_dataset_5.json` initially
- Verify workflow works correctly
- Scale up to larger datasets later

### 2. Monitor Workflow Minutes
- GitHub provides 2000 free minutes/month for private repos
- Public repos have unlimited minutes
- Check usage: Settings → Billing

### 3. Use Artifacts for Debugging
- Download artifacts to see exact test output
- Check logs for detailed error messages
- Artifacts persist for 30 days

### 4. Branch Protection
Consider setting up branch protection:
- Settings → Branches
- Add rule for `main` branch
- Require status checks to pass
- Require "Test and Publish Reports" to succeed before merging

---

## 📊 Understanding the Workflow

### Two Jobs in One Workflow

**Job 1: Test**
- Always runs on push/PR
- Runs tests and creates artifacts
- Continues even if tests fail
- Duration: ~5-10 minutes

**Job 2: Publish**
- Only runs after test job
- Only on push to main/develop (NOT on PRs)
- Publishes reports to GitHub Pages
- Duration: ~1-2 minutes

### Why Two Jobs?

- **Separation of concerns:** Testing vs Publishing
- **Conditional publishing:** PRs get tested but don't publish
- **Faster PR feedback:** PRs don't wait for publishing
- **Artifact sharing:** Test job creates, publish job uses

---

## 🎯 Next Steps

1. ✅ Push workflow to GitHub
2. ✅ Enable GitHub Pages
3. ✅ Configure permissions
4. ✅ Run first test
5. ✅ View reports on GitHub Pages
6. ✅ Add status badge to README
7. ✅ Set up branch protection (optional)
8. ✅ Configure secrets if needed

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Troubleshooting Workflows](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows)

---

## 🆘 Still Need Help?

If you're stuck:
1. Check the workflow logs in the Actions tab
2. Look for error messages in the failed steps
3. Verify all setup steps were completed
4. Check that files are in correct locations

**Happy Testing! 🚀**

Your Next Gen UI Agent Testing Framework is now fully automated!
