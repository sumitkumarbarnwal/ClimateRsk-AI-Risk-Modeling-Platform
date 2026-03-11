# Installation Guide - ESG Risk Modeling Platform

## Quick Start

### Method 1: Automated Setup (Recommended)
```bash
# Extract the project files
# Navigate to the project directory
cd esg-risk-platform

# Run automated setup
python setup.py

# Launch the application
python run.py
```

### Method 2: Manual Installation

#### Prerequisites
- Python 3.11 or higher
- pip package manager

#### Step 1: Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Initialize Database
```bash
python -c "from utils.sqlite_manager import SQLiteManager; SQLiteManager()"
```

#### Step 4: Launch Application
```bash
streamlit run app.py
```

## Troubleshooting

### Python 3.13 Issues (Windows)
If you encounter setuptools errors with Python 3.13:

```bash
# Option 1: Use Python 3.11 (recommended)
# Download from python.org

# Option 2: Fix Python 3.13
python -m pip install --upgrade pip setuptools wheel
pip install --no-build-isolation streamlit pandas numpy plotly scikit-learn sqlalchemy
```

### Port Issues
If port 8501 is busy:
- Streamlit will automatically find another available port
- Check the terminal output for the correct URL

### Import Errors
Ensure you're in the correct virtual environment:
```bash
which python  # Should show venv path
pip list      # Verify packages are installed
```

## Verification

After installation, test the platform:

1. Navigate to the displayed URL (usually http://localhost:8501)
2. Upload the sample dataset from `sample_data/financial_portfolio.csv`
3. Process the data with ESG integration
4. Train both baseline and ESG-enhanced models
5. Compare results in the Model Comparison page

Expected results:
- 5-15% AUC-ROC improvement with ESG factors
- Clear feature importance rankings
- Interactive risk dashboard

## Support

For issues:
1. Check Python version compatibility (3.11+)
2. Verify all dependencies are installed
3. Ensure database directory permissions
4. Try running setup.py again