# Deployment Guide for SFT Number Generator

## Option 1: Streamlit Cloud (Recommended) 🚀

### Prerequisites
- GitHub account
- Streamlit account (free at share.streamlit.io)

### Steps:

1. **Create GitHub Repository**
   ```bash
   # Create new repository on GitHub named "sft-number-generator"
   git init
   git add .
   git commit -m "Initial commit: SFT Number Generator"
   git branch -M main
   git remote add origin https://github.com/YOURUSERNAME/sft-number-generator.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub account
   - Select your repository: `YOURUSERNAME/sft-number-generator`
   - Main file path: `streamlit_app.py`
   - Click "Deploy!"

3. **Configuration**
   - App will automatically install dependencies from requirements.txt
   - Configuration from .streamlit/config.toml will be applied
   - Your app will be available at: `https://YOURUSERNAME-sft-number-generator-streamlit-app-xyz.streamlit.app`

### Important Notes for Streamlit Cloud:
- Excel and JSON files will be stored in temporary storage
- Files will reset when the app restarts (Streamlit limitation)
- For production use, consider cloud storage integration (AWS S3, Google Drive API)

---

## Option 2: GitHub Pages (Static Alternative) 📄

GitHub Pages only supports static websites, so we need a different approach:

### Option 2A: JavaScript Version

Create a client-side JavaScript version:

1. **Create HTML Interface**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>SFT Number Generator</title>
       <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
   </head>
   <body>
       <!-- Interface elements -->
       <script src="sft-generator.js"></script>
   </body>
   </html>
   ```

2. **JavaScript Implementation**
   - Use localStorage for memory persistence
   - Generate Excel files client-side with xlsx.js
   - Deploy to GitHub Pages

### Option 2B: GitHub Actions + API

Use GitHub Actions to run Python scripts and serve results:

1. **Create GitHub Action**
   ```yaml
   # .github/workflows/update-data.yml
   name: Update SFT Data
   on:
     workflow_dispatch:
       inputs:
         app_name:
           description: 'Application Name'
           required: true

   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.9'
         - name: Install dependencies
           run: pip install -r requirements.txt
         - name: Generate SFT Number
           run: python generate_sft.py "${{ github.event.inputs.app_name }}"
         - name: Commit changes
           run: |
             git config --local user.email "action@github.com"
             git config --local user.name "GitHub Action"
             git add .
             git commit -m "Add new SFT number for ${{ github.event.inputs.app_name }}"
             git push
   ```

---

## Option 3: Other Cloud Platforms 🌩️

### Heroku
1. Install Heroku CLI
2. Create Procfile: `web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
3. Deploy: `git push heroku main`

### Railway
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run streamlit_app.py`

### Replit
1. Import from GitHub
2. Set run command: `streamlit run streamlit_app.py`
3. Configure port forwarding

---

## File Persistence Solutions 💾

For production deployment with persistent data:

### Option A: Cloud Storage
```python
# Add to sft_number_generator.py
import boto3  # for AWS S3
# or
from google.cloud import storage  # for Google Cloud Storage
```

### Option B: Database Integration
```python
# Add database support
import sqlite3
# or
import psycopg2  # for PostgreSQL
```

### Option C: External APIs
```python
# Use external services
import requests  # for REST APIs
```

---

## Quick Deployment Commands 🚀

```bash
# 1. Prepare files
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
git remote add origin https://github.com/YOURUSERNAME/sft-number-generator.git
git push -u origin main

# 3. Deploy to Streamlit Cloud
# Visit https://share.streamlit.io and follow the GUI

# 4. Your app will be live at:
# https://YOURUSERNAME-sft-number-generator-streamlit-app-xyz.streamlit.app
```

## Testing Before Deployment ✅

```bash
# Local testing
streamlit run streamlit_app.py

# Test all features:
# 1. Register single application
# 2. Bulk registration
# 3. Number reservation
# 4. Statistics view
# 5. Data export
```
