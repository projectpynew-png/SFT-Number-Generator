# Create requirements.txt for deployment
requirements = '''streamlit==1.28.0
pandas==2.1.0
openpyxl==3.1.2
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements)

# Create .streamlit/config.toml for configuration
config_toml = '''[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 200
'''

import os
os.makedirs('.streamlit', exist_ok=True)
with open('.streamlit/config.toml', 'w') as f:
    f.write(config_toml)

# Create README.md for GitHub deployment
readme_content = '''# SFT Number Generator System

A comprehensive web-based system for generating unique SFT numbers for applications with persistent memory and Excel backend integration.

## 🚀 Features

- **Unique Number Generation**: Generate numbers in range 3000-9999
- **No Duplicates**: Advanced memory system prevents repetition
- **Excel Backend**: Automatic database updates with full audit trail
- **Bulk Registration**: Register multiple applications at once
- **Number Reservation**: Reserve specific numbers for special applications
- **Real-time Statistics**: Usage analytics and reporting
- **Data Export**: Download Excel reports and CSV files

## 🌐 Live Demo

Visit the live application: [SFT Number Generator](https://your-app.streamlit.app)

## 🏃‍♂️ Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sft-number-generator.git
cd sft-number-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud Deployment

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repository

## 📁 File Structure

```
sft-number-generator/
├── streamlit_app.py          # Main Streamlit web application
├── sft_number_generator.py   # Core SFT generator class
├── sft_demo.py              # Demo script for testing
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── sft_records.xlsx         # Excel database (auto-generated)
├── sft_memory.json          # Memory persistence (auto-generated)
└── README.md               # This file
```

## 🔧 Configuration

The system uses the following configuration:
- **Number Range**: 3000 - 9999 (7,000 total numbers)
- **Database**: Excel file with automatic updates
- **Memory**: JSON file for persistence across sessions
- **Web Interface**: Streamlit with responsive design

## 📊 Usage

### Single Application Registration
1. Navigate to "Register Application"
2. Enter application name and description
3. Click "Generate SFT Number"
4. Your unique number will be displayed

### Bulk Registration
1. Go to "Bulk Registration"
2. Enter applications in format: `AppName | Description`
3. Click "Bulk Register Applications"
4. View results in the generated table

### Number Reservation
1. Visit "Reserve Number"
2. Enter desired SFT number (3000-9999)
3. Check availability status
4. Reserve if available

## 📈 System Statistics

The dashboard provides:
- Total available numbers
- Numbers currently used
- Remaining capacity
- Usage percentage
- Registration timeline

## 💾 Data Export

Export options include:
- Complete Excel report with summary
- CSV data export
- Real-time download generation

## 🛠️ Technical Details

- **Backend**: Python with pandas for data management
- **Frontend**: Streamlit for web interface
- **Database**: Excel files with openpyxl
- **Memory**: JSON-based persistence
- **Deployment**: Streamlit Cloud ready

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in this repository
- Contact: [your-email@example.com]

## 🎯 Roadmap

- [ ] User authentication system
- [ ] API endpoints for external integration
- [ ] Advanced analytics and reporting
- [ ] Number recycling for deleted applications
- [ ] Multi-tenant support
'''

with open('README.md', 'w') as f:
    f.write(readme_content)

print("📋 Created deployment files:")
print("   • requirements.txt - Python dependencies")
print("   • .streamlit/config.toml - Streamlit configuration")
print("   • README.md - GitHub documentation")

# Create a deployment guide
deployment_guide = '''# Deployment Guide for SFT Number Generator

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
'''

with open('DEPLOYMENT_GUIDE.md', 'w') as f:
    f.write(deployment_guide)

print("   • DEPLOYMENT_GUIDE.md - Step-by-step deployment instructions")