#!/usr/bin/env python3
"""
Package creator for Punjab Vaccination Dashboard
Creates a comprehensive ZIP package with all files and documentation
"""

import os
import zipfile
from datetime import datetime

def create_vaccination_dashboard_package():
    """Create a complete package for the vaccination dashboard."""
    
    # Package name with timestamp
    package_name = f"punjab_vaccination_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Files to include in the package
    files_to_include = [
        'app.py',
        'data_loader.py',
        'visualization.py',
        'utils.py',
        'pyproject.toml',
        'uv.lock',
        'Dockerfile',
        'docker-compose.yml',
        '.dockerignore',
        'README.md',
        'INSTALLATION_GUIDE.md',
        'sample_vaccination_data.csv',
        '.streamlit/config.toml'
    ]
    
    print(f"🚀 Creating vaccination dashboard package: {package_name}")
    
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main project files
        for file_path in files_to_include:
            if os.path.exists(file_path):
                zipf.write(file_path)
                print(f"✅ Added: {file_path}")
            else:
                print(f"⚠️  Skipped (not found): {file_path}")
        
        # Create requirements.txt for pip users
        requirements_content = """streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
folium>=0.14.0
streamlit-folium>=0.13.0
requests>=2.31.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
reportlab>=4.0.0
"""
        
        zipf.writestr('requirements.txt', requirements_content)
        print("✅ Added: requirements.txt")
        
        # Create startup script for easy launch
        startup_script = """#!/bin/bash
# Punjab Vaccination Dashboard Startup Script
echo "🏥 Starting Punjab Vaccination Dashboard..."
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Docker detected - Starting with Docker (Recommended)"
    docker-compose up -d
    echo ""
    echo "✅ Dashboard starting at: http://localhost:5000"
    echo "⏳ Please wait 30-60 seconds for complete startup"
elif command -v python &> /dev/null; then
    echo "🐍 Python detected - Starting locally"
    # Install dependencies if needed
    if command -v uv &> /dev/null; then
        echo "Installing dependencies with UV..."
        uv sync
        uv run streamlit run app.py --server.port 5000
    else
        echo "Installing dependencies with pip..."
        pip install -r requirements.txt
        streamlit run app.py --server.port 5000
    fi
else
    echo "❌ Neither Docker nor Python found!"
    echo "Please install Docker Desktop or Python 3.11+ to continue"
    echo "See INSTALLATION_GUIDE.md for detailed instructions"
fi
"""
        zipf.writestr('start_dashboard.sh', startup_script)
        zipf.writestr('start_dashboard.bat', startup_script.replace('#!/bin/bash', '@echo off'))
        print("✅ Added: startup scripts")
        
    print(f"")
    print(f"🎉 Package created successfully: {package_name}")
    print(f"📦 Package size: {os.path.getsize(package_name) / 1024 / 1024:.2f} MB")
    print(f"")
    print(f"📋 Package contents:")
    print(f"   ✅ Complete dashboard application")
    print(f"   ✅ Docker setup for easy deployment")
    print(f"   ✅ Excel & PDF export capabilities")
    print(f"   ✅ Dark theme support")
    print(f"   ✅ Sample vaccination data")
    print(f"   ✅ Comprehensive installation guide")
    print(f"   ✅ Startup scripts for all platforms")
    print(f"")
    print(f"🚀 To get started:")
    print(f"   1. Extract the ZIP file")
    print(f"   2. Read INSTALLATION_GUIDE.md")
    print(f"   3. Run start_dashboard.sh (Linux/Mac) or start_dashboard.bat (Windows)")
    print(f"   4. Open http://localhost:5000 in your browser")
    
    return package_name

if __name__ == "__main__":
    create_vaccination_dashboard_package()