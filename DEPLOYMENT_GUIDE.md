# 🚀 Deployment Guide - LSI Coupon Dashboard

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [GitHub Setup](#github-setup)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Alternative: Heroku Deployment](#alternative-heroku-deployment)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required:
- ✅ GitHub account ([Sign up](https://github.com/join))
- ✅ Git installed ([Download](https://git-scm.com/downloads))
- ✅ All project files ready

### Optional (for local testing):
- Python 3.8+
- pip

---

## 2. GitHub Setup

### Step 1: Create New Repository

1. Go to [GitHub](https://github.com)
2. Click **"New"** or **"+"** → **"New repository"**
3. Fill in:
   - **Repository name:** `lsi-coupon-dashboard` (or your choice)
   - **Description:** "Interactive dashboard for LSI coupon statistics"
   - **Public** or **Private** (your choice)
   - ✅ **Do NOT** initialize with README (we have our own)
4. Click **"Create repository"**

### Step 2: Push Your Code

Open terminal in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: LSI Coupon Dashboard"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/lsi-coupon-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**✅ Your code is now on GitHub!**

---

## 3. Streamlit Cloud Deployment

### Step 1: Access Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub

### Step 2: Deploy App

1. Click **"New app"** button
2. Fill in deployment settings:

```
Repository: YOUR_USERNAME/lsi-coupon-dashboard
Branch: main
Main file path: app.py
App URL (optional): lsi-coupon-dashboard (or custom subdomain)
```

3. Click **"Deploy!"**

### Step 3: Wait for Deployment

- ⏳ First deployment takes 2-5 minutes
- 📊 You'll see build logs
- ✅ When done, you'll get a URL like: `https://lsi-coupon-dashboard.streamlit.app`

### Step 4: Test Your App

1. Click the URL
2. Upload a sample Excel file
3. Test all filters and tabs
4. Verify charts and tables display correctly

**🎉 Your dashboard is LIVE!**

---

## 4. Alternative: Heroku Deployment

If you prefer Heroku instead of Streamlit Cloud:

### Additional Files Needed

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create lsi-coupon-dashboard

# Push code
git push heroku main

# Open app
heroku open
```

---

## 5. Testing

### Local Testing (Before Deployment)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Test in browser
# Open: http://localhost:8501
```

### Test Checklist

- [ ] File upload works
- [ ] Date range filter works
- [ ] Store filter (select all / specific)
- [ ] Coupon filter (keywords / specific)
- [ ] Line chart displays correctly
- [ ] Data table shows below chart
- [ ] Pivot table tab works
- [ ] Data detail tab shows filtered data
- [ ] Excel export works (all sheets)
- [ ] CSV downloads work
- [ ] Metrics cards update correctly
- [ ] Legend click hides/shows lines
- [ ] Responsive on mobile

---

## 6. Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
# Check requirements.txt has all dependencies
cat requirements.txt

# If missing, add:
streamlit==1.31.1
pandas==2.1.4
openpyxl==3.1.2
plotly==5.18.0

# Commit and push
git add requirements.txt
git commit -m "Fix dependencies"
git push
```

### Problem: "App is not loading"

**Solution:**
1. Check Streamlit Cloud logs
2. Verify `app.py` is in root folder
3. Check for syntax errors
4. Ensure all imports are in requirements.txt

### Problem: "Excel upload not working"

**Solution:**
```python
# Check file uploader in app.py
uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=['xlsx', 'xls'],  # Make sure these are included
    help="Upload your LSI Coupon Statistics file"
)
```

### Problem: "Chart not displaying"

**Solution:**
1. Check data has required columns
2. Verify date column format
3. Look for errors in Streamlit logs
4. Test with sample data first

### Problem: "Deployment keeps failing"

**Solution:**
1. Check Python version in `runtime.txt`:
   ```
   python-3.9.18
   ```
2. Simplify requirements.txt (remove version pins)
3. Check GitHub repository is public (or grant Streamlit access)

---

## 📊 Post-Deployment

### Share Your Dashboard

1. **Get your URL:**
   - Streamlit Cloud: `https://YOUR-APP.streamlit.app`
   - Custom domain: [Add custom domain](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/custom-subdomains)

2. **Share:**
   - Copy URL
   - Send to team/stakeholders
   - Add to documentation

### Monitor Usage

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View:
   - Usage stats
   - Logs
   - Resource usage

### Update App

When you make changes:

```bash
# Make changes to app.py
# Test locally first
streamlit run app.py

# Commit and push
git add .
git commit -m "Update: description of changes"
git push

# Streamlit Cloud auto-deploys! 🚀
```

---

## 🔐 Security Notes

### Don't Commit:
- ❌ Real data files (.xlsx)
- ❌ API keys
- ❌ Passwords
- ❌ Secrets

### Use Secrets Management:

Create `.streamlit/secrets.toml` (locally only):
```toml
# This file is in .gitignore
[database]
user = "your_user"
password = "your_password"
```

Access in app:
```python
import streamlit as st
user = st.secrets["database"]["user"]
```

Add secrets in Streamlit Cloud:
1. Go to app settings
2. Click "Secrets"
3. Paste your secrets.toml content

---

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Docs](https://plotly.com/python/)
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [Streamlit Community](https://discuss.streamlit.io)

---

## ✅ Deployment Checklist

Before going live:

- [ ] All features tested locally
- [ ] Requirements.txt complete
- [ ] README.md updated
- [ ] .gitignore configured
- [ ] Code pushed to GitHub
- [ ] Deployed to Streamlit Cloud
- [ ] Live URL tested
- [ ] Sample data prepared for users
- [ ] Documentation complete
- [ ] Team notified

---

**🎉 Congratulations! Your dashboard is deployed!**

For questions or issues, create an issue on GitHub.
