# Punjab Vaccination Coverage Dashboard 💉

A comprehensive dashboard for analyzing and improving childhood vaccination coverage in rural Punjab. This powerful tool provides interactive visualizations, real-time analytics, and actionable insights to help health officials make data-driven decisions.

## 🚀 Quick Start Guide

### Option 1: One-Click Setup (Easiest)
1. **Download** the ZIP package: `punjab_vaccination_dashboard_[timestamp].zip`
2. **Extract** to any folder on your computer
3. **Double-click** the startup script:
   - **Windows**: `start_dashboard.bat`
   - **Mac/Linux**: `start_dashboard.sh`
4. **Open** your browser to `http://localhost:5000`
5. **Done!** Your dashboard is running!

### Option 2: Docker Setup (Recommended)
```bash
# Extract the ZIP file, then:
cd vaccination-dashboard
docker-compose up -d

# Access at http://localhost:5000
```

### Option 3: Manual Python Setup
```bash
# Extract ZIP file and navigate to folder
cd vaccination-dashboard

# Install Python dependencies
pip install -r requirements.txt

# Start the dashboard
streamlit run app.py --server.port 5000

# Open http://localhost:5000
```

## 🔧 Prerequisites

**For One-Click Setup:**
- Just download and extract the ZIP file!

**For Docker Setup:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed

**For Manual Setup:**
- Python 3.11 or higher
  

https://github.com/user-attachments/assets/965c8c4d-99c8-4468-9178-a15bf82d945e




pip (comes with Python)

## ✨ Key Features

### 🎨 **Dual Theme Support**
- **Light Theme**: Professional, clean interface
- **Dark Theme**: Comfortable for extended use
- Toggle themes using the sidebar selector

### 📊 **Advanced Export Options**
- **📥 CSV Export**: Raw data for analysis
- **📊 Excel Reports**: Multi-sheet workbooks with summaries and statistics
- **📄 PDF Reports**: Professional documents with charts and recommendations
- **📋 Text Summaries**: Concise overview reports

### 🗺️ **Interactive Geographic Mapping**
- Visual coverage mapping across Punjab districts
- Color-coded markers showing coverage levels (Green: ≥90%, Orange: 75-89%, Red: <75%)
- Clickable markers with detailed district information

### 📈 **Comprehensive Analytics**
- **Key Performance Indicators**: Real-time metrics and target comparisons
- **Coverage Analysis**: Vaccine-specific charts and distributions
- **Timeline Analysis**: Trends over time and seasonal patterns
- **Demographics**: Age group and gender analysis
- **Smart Recommendations**: AI-generated insights for improvement

### 📱 **User-Friendly Interface**
- Responsive design works on all devices
- Intuitive navigation with tabbed interface
- Real-time filtering and data updates

## 📂 Adding Your Vaccination Data

### Method 1: File Upload (Easiest)
1. **Open** the dashboard in your browser
2. **Look for** the file upload area on the main page
3. **Click** "Browse files" and select your CSV or Excel file
4. **Watch** as your data loads automatically!

**Required columns in your data:**
- `district` - District name (e.g., "Amritsar", "Ludhiana")
- `vaccine_type` - Vaccine type (e.g., "BCG", "DPT1", "Polio")
- `coverage_percentage` - Coverage percentage (0-100)

**Optional columns for enhanced analysis:**
- `village` - Village/locality name
- `child_id` - Unique identifier for each child
- `date` - Vaccination date (YYYY-MM-DD format)
- `age_group` - Age category (e.g., "0-12 months")
- `gender` - Gender (Male/Female)

### Method 2: API Integration
For connecting to health department APIs:
1. Contact your IT administrator for API credentials
2. Set environment variables with your API details
3. Restart the dashboard to load live data

### Method 3: Database Connection
For direct database integration:
1. Configure database connection settings
2. Set environment variables for your database
3. Restart the dashboard to connect

## 🎯 Step-by-Step Usage Guide

### Getting Started
1. **Launch** the dashboard using any of the setup methods above
2. **Upload** your vaccination data or use the included sample data
3. **Explore** the dashboard using the tabs at the top

### Dashboard Navigation
1. **🗺️ Geographic Overview**: View coverage maps and district summaries
2. **📊 Coverage Analysis**: Analyze vaccine-specific performance
3. **📈 Trends & Timeline**: Track progress over time
4. **👥 Demographics**: Understand age and gender patterns
5. **📋 Detailed Reports**: Generate insights and export data

### Using Filters
- **District**: Focus on specific districts
- **Vaccine Type**: Analyze particular vaccines
- **Date Range**: Look at specific time periods
- **Age Group**: Filter by child age categories
- **Gender**: Compare male vs female coverage

### Generating Reports
1. **Go to** the "Detailed Reports" tab
2. **Choose** your export format:
   - CSV for raw data analysis
   - Excel for comprehensive reports
   - PDF for professional presentations
   - Text for quick summaries
3. **Click** the download button
4. **Save** the file to your computer

## 🔧 Troubleshooting

### Dashboard Won't Start
```bash
# Check if port 5000 is busy
# Windows:
netstat -ano | findstr :5000

# Mac/Linux:
lsof -i :5000

# If busy, kill the process or change port
```

### Data Not Loading
- **Check file format**: Ensure CSV/Excel is properly formatted
- **Verify columns**: Required columns must be present
- **File size**: Large files may take time to process
- **File permissions**: Ensure file is readable

### Charts Not Displaying
- **Refresh browser**: Press Ctrl+F5 (Windows) or Cmd+R (Mac)
- **Try different browser**: Chrome, Firefox, Safari work best
- **Clear cache**: Clear browser cache and cookies

### Performance Issues
- **Filter data**: Use date/district filters for large datasets
- **Reduce file size**: Consider breaking large files into smaller chunks
- **Close other apps**: Free up system memory

## 🔄 Updating the Dashboard

### For Docker Users:
```bash
# Download new ZIP file, extract, then:
docker-compose down
docker-compose up -d --build
```

### For Python Users:
```bash
# Download new ZIP file, extract, then:
pip install -r requirements.txt --upgrade
streamlit run app.py --server.port 5000
```

## 📞 Getting Help

### Before Contacting Support:
1. **Check this README** - Most issues are covered here
2. **Review error messages** - They often contain helpful information
3. **Try restarting** - Close and restart the dashboard

### When Reporting Issues, Include:
- Operating system (Windows, Mac, Linux)
- Setup method used (Docker, Python, One-click)
- Browser name and version
- Error messages (copy and paste exactly)
- Steps that led to the problem

### Log Files:
**Docker users:**
```bash
docker-compose logs vaccination-dashboard
```

**Python users:**
Look for error messages in your terminal/command prompt

## 🌟 Advanced Features

### Environment Configuration
Create a `.env` file for custom settings:
```
VACCINATION_DATA_SOURCE=csv
DEFAULT_THEME=light
MAX_UPLOAD_SIZE=200MB
```

### Custom Data Sources
The dashboard can connect to:
- Government health APIs
- Hospital management systems
- Database servers
- Cloud storage services

Contact your IT administrator for integration assistance.

## 📈 Sample Data Included

The dashboard comes with realistic sample data showing:
- 500 vaccination records across 10 Punjab districts
- Multiple vaccine types (BCG, DPT1-3, Polio, Measles)
- Coverage percentages reflecting real-world patterns
- Age and gender demographics

Use this sample data to:
- Learn how the dashboard works
- Test different features
- Train your team
- Demonstrate capabilities

## 🎉 Success Stories

This dashboard is designed to help:
- **Health Officials**: Track vaccination progress and identify gaps
- **Field Workers**: Focus efforts on low-coverage areas
- **Administrators**: Generate reports for stakeholders
- **Researchers**: Analyze vaccination patterns and trends

## 🚀 Next Steps

1. **Upload your real vaccination data**
2. **Train your team** on using the dashboard
3. **Set up regular reporting** using the export features
4. **Monitor key metrics** weekly or monthly
5. **Use insights** to improve vaccination programs

---

**🏥 Transform vaccination data into actionable insights for healthier communities in rural Punjab!**

*For additional support, refer to the INSTALLATION_GUIDE.md file or contact your technical administrator.*
