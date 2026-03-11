#!/usr/bin/env python3
"""
Quick launch script for ESG Risk Modeling Platform
"""

import os
import sys
import subprocess

def main():
    """Launch the Streamlit application"""
    try:
        # Ensure we're in the correct directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error launching application: {e}")

if __name__ == "__main__":
    main()