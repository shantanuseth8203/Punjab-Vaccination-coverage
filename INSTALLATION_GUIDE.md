# Punjab Vaccination Dashboard - Complete Installation Guide 🚀

Welcome to your comprehensive vaccination coverage dashboard! This guide will walk you through setting up and running the dashboard step by step.

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start with Docker](#quick-start-with-docker)
3. [Local Development Setup](#local-development-setup)
4. [Adding Your Data](#adding-your-data)
5. [Features Overview](#features-overview)
6. [Troubleshooting](#troubleshooting)
7. [Support](#support)

---

## 🔧 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Required for initial setup

### Required Software
- **Docker** (Recommended approach) OR
- **Python 3.11+** with pip/UV package manager

---

## 🐳 Quick Start with Docker (Recommended)

This is the easiest way to get started! Docker handles all dependencies automatically.

### Step 1: Install Docker
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation by opening terminal/command prompt and running:
   ```bash
   docker --version
   ```

### Step 2: Download and Extract
1. Extract the ZIP file to your desired location
2. Open terminal/command prompt in the extracted folder

### Step 3: Start the Dashboard
```bash
# Navigate to the project folder
cd vaccination-dashboard

# Start the dashboard (this will download and set up everything automatically)
docker-compose up -d

# Wait for the setup to complete (first time may take 2-3 minutes)
```

### Step 4: Access Your Dashboard
1. Open your web browser
2. Go to: **http://localhost:5000**
3. Your dashboard should be running! 🎉

### Managing the Docker Dashboard
```bash
# Stop the dashboard
docker-compose down

# Restart the dashboard
docker-compose restart

# View logs if needed
docker-compose logs vaccination-dashboard

# Update the dashboard (after making changes)
docker-compose up -d --build
```

---

## 💻 Local Development Setup

If you prefer to run without Docker or want to modify the code:

### Step 1: Install Python
1. Download Python 3.11+ from: https://www.python.org/downloads/
2. Ensure Python and pip are added to your system PATH
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

### Step 2: Install UV Package Manager (Recommended)
```bash
# Install UV for faster dependency management
pip install uv
```

### Step 3: Set Up the Project
```bash
# Navigate to the project folder
cd vaccination-dashboard

# Install all dependencies
uv sync

# Alternative with regular pip
# pip install -r requirements.txt
```

### Step 4: Run the Dashboard
```bash
# Start the dashboard
uv run streamlit run app.py --server.port 5000

# Alternative with regular python
# streamlit run app.py --server.port 5000
```

### Step 5: Access Your Dashboard
1. Open your web browser
2. Go to: **http://localhost:5000**
3. Your dashboard should be running! 🎉

---

## 📊 Adding Your Data

The dashboard supports multiple ways to add vaccination data:

### Option 1: File Upload (Easiest)
1. Open the dashboard in your browser
2. Click on the **file upload area** 
3. Select your CSV or Excel file with vaccination data
4. The dashboard will automatically process and display your data

**Required columns in your data file:**
- `district` - District name
- `vaccine_type` - Type of vaccine (BCG, DPT, Polio, etc.)
- `coverage_percentage` - Coverage percentage (0-100)

**Optional columns (for enhanced analysis):**
- `village` - Village/locality name
- `child_id` - Unique child identifier  
- `date` - Vaccination date
- `age_group` - Age category
- `gender` - Gender (Male/Female)

### Option 2: API Integration
If you have access to health department APIs:

1. Set environment variables:
   ```bash
   export VACCINATION_DATA_SOURCE=api
   export VACCINATION_API_URL=your_api_endpoint
   export VACCINATION_API_KEY=your_api_key
   ```

2. Restart the dashboard to load API data

### Option 3: Database Connection
For database integration:

1. Set environment variables:
   ```bash
   export VACCINATION_DATA_SOURCE=database
   export DB_HOST=your_database_host
   export DB_NAME=vaccination_db
   export DB_USER=your_username
   export DB_PASSWORD=your_password
   ```

2. Restart the dashboard to connect to your database

---

## ✨ Features Overview

Your dashboard includes these powerful features:

### 🎨 **Theme Options**
- **Light Theme**: Clean, professional appearance
- **Dark Theme**: Easy on the eyes for extended use
- Switch themes using the sidebar selector

### 📍 **Interactive Geographic Maps**
- Visual coverage mapping across Punjab districts
- Color-coded markers showing coverage levels
- Clickable markers with detailed information

### 📈 **Comprehensive Analytics**
- **Key Performance Indicators**: Total children, coverage rates, targets
- **Coverage Analysis**: Vaccine-specific charts and distributions
- **Timeline Analysis**: Trends over time, seasonal patterns
- **Demographics**: Age group and gender analysis

### 📋 **Advanced Export Options**
- **CSV Export**: Raw data for further analysis
- **Excel Reports**: Multi-sheet workbooks with summaries
- **PDF Reports**: Professional reports with charts and recommendations
- **Text Summaries**: Concise overview reports

### 🔍 **Intelligent Filtering**
- Filter by district, vaccine type, date range
- Age group and gender filtering
- Real-time data updates

### 💡 **Actionable Recommendations**
- AI-generated insights based on your data
- Priority areas identification
- Target achievement analysis

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### **Dashboard won't start**
```bash
# Check if port 5000 is in use
# Windows:
netstat -ano | findstr :5000

# Mac/Linux:
lsof -i :5000

# If port is busy, kill the process or change port in docker-compose.yml
```

#### **Docker issues**
```bash
# Restart Docker Desktop
# Clear Docker cache
docker system prune -a

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

#### **Data not loading**
1. **Check file format**: Ensure CSV/Excel files are properly formatted
2. **Verify columns**: Required columns must be present
3. **File permissions**: Ensure files are readable
4. **File size**: Large files may take time to process

#### **Charts not displaying**
1. **Clear browser cache**: Ctrl+F5 (Windows) or Cmd+R (Mac)
2. **Try different browser**: Chrome, Firefox, Safari, Edge
3. **Check internet connection**: Some components require internet access

#### **Memory issues**
1. **Large datasets**: Consider filtering data before upload
2. **Increase Docker memory**: Docker Desktop > Settings > Resources
3. **Close other applications**: Free up system memory

### **Performance Optimization**

For large datasets (>10,000 records):
1. **Filter data before upload**
2. **Use date range filtering**
3. **Consider database integration** instead of file upload

---

## 📞 Support

### Getting Help

1. **Check this guide first** - Most issues are covered here
2. **Review error messages** - They often contain helpful information
3. **Check Docker/Python logs** for detailed error information

### Log Files

**Docker logs:**
```bash
docker-compose logs vaccination-dashboard
```

**Python logs:**
Look for error messages in your terminal when running locally

### System Information

When reporting issues, please include:
- Operating system and version
- Docker version (if using Docker)
- Python version (if running locally)
- Browser name and version
- Error messages (if any)

---

## 🎯 Next Steps

1. **Upload your vaccination data** using the file upload feature
2. **Explore the analytics** across different tabs
3. **Generate reports** using the export features
4. **Switch to dark theme** for comfortable viewing
5. **Share insights** with your team using exported reports

---

## 🚀 Advanced Usage

### Custom Configuration

**Environment Variables:**
```bash
# Data source configuration
VACCINATION_DATA_SOURCE=csv  # Options: csv, database, api
VACCINATION_DATA_PATH=vaccination_data.csv

# Theme settings
DEFAULT_THEME=light  # Options: light, dark

# Performance settings
MAX_UPLOAD_SIZE=200MB
CACHE_TIMEOUT=3600
```

### API Integration

For connecting to health department APIs, you'll need:
- API endpoint URL
- Authentication credentials
- Proper data format mapping

Contact your IT administrator for API access details.

---

**🎉 Congratulations! Your vaccination dashboard is ready to help improve healthcare outcomes in rural Punjab.**

For additional support or questions, refer to the README.md file or contact your technical administrator.