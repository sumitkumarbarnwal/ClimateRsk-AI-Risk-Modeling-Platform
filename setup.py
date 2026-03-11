#!/usr/bin/env python3
"""
Setup script for ESG Risk Modeling Platform
Handles installation and initial configuration
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_requirements():
    """Install required packages"""
    try:
        print("📦 Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 
        'sklearn', 'sqlalchemy'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            print(f"❌ Failed to import {package}")
            return False
    return True

def initialize_database():
    """Initialize the SQLite database"""
    try:
        from utils.sqlite_manager import SQLiteManager
        db_manager = SQLiteManager()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🌍 ESG Risk Modeling Platform Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("\n💡 Try using:")
        print("  pip install --upgrade pip")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n❌ Package import test failed")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Database initialization failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the application:")
    print("  streamlit run app.py")
    print("\nThe application will be available at: http://localhost:8501")

if __name__ == "__main__":
    main()