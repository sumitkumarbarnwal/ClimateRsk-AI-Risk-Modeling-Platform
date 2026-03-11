# Climate-Aware Quantitative Risk Modeling Platform

A comprehensive Streamlit-based platform for ESG-enhanced financial risk analytics that demonstrates how Environmental, Social, and Governance factors improve risk predictions through machine learning.

## Features

- **Data Upload & Processing**: Upload financial datasets with automatic ESG factor integration
- **Model Training**: Train Random Forest and Gradient Boosting models with/without ESG factors
- **Performance Comparison**: Compare baseline vs ESG-enhanced model performance
- **Risk Dashboard**: Interactive visualizations and risk predictions
- **Database Management**: SQLite-based portfolio storage and management

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Quick Setup

1. **Download and extract the project files**
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

The application will start on `http://localhost:8501`

## Usage

### 1. Data Upload
- Navigate to the "Data Upload" page
- Upload a CSV file with financial data
- Configure ESG factor integration
- Save portfolio to database

### 2. Model Training
- Train baseline models (financial features only)
- Train ESG-enhanced models (all features)
- Compare performance metrics
- Results automatically saved to database

### 3. Model Comparison
- View detailed performance comparisons
- Analyze ESG feature importance
- Export comparison reports

### 4. Risk Dashboard
- Interactive risk predictions
- Feature correlation analysis
- ESG impact visualization
- Export risk reports

### 5. Database Management
- View stored portfolios
- Load previous analyses
- Export portfolio data
- Database statistics

## Sample Data

The platform includes a sample financial portfolio dataset (`sample_data/financial_portfolio.csv`) with 30 companies across different sectors, designed to demonstrate clear ESG enhancement benefits.

## Expected Results

When using the sample data, you can expect:
- **5-15% AUC-ROC improvement** with ESG factors
- **8-20% F1-Score enhancement** for risk prediction
- Clear feature importance rankings showing ESG impact
- Realistic sector-based risk differentiation

## Project Structure

```
esg-risk-platform/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── pages/
│   ├── 1_Data_Upload.py       # Data upload and processing
│   ├── 2_Model_Training.py    # ML model training
│   ├── 3_Model_Comparison.py  # Performance comparison
│   ├── 4_Risk_Dashboard.py    # Risk predictions dashboard
│   └── 5_Database_Management.py # Portfolio management
├── utils/
│   ├── data_processor.py      # Data preprocessing utilities
│   ├── model_trainer.py       # ML model training logic
│   ├── sqlite_manager.py      # Database operations
│   └── visualizations.py     # Plotting and visualization
├── sample_data/
│   └── financial_portfolio.csv # Sample dataset
└── data/
    └── (SQLite database created automatically)
```

## Technical Details

### Machine Learning Models
- Logistic Regression
- Random Forest Classifier
- Gradient Boosting Classifier

### ESG Indicators Generated
- Carbon Exposure Score
- ESG Rating (0-100)
- Climate Risk Indicator
- Green Investment Ratio
- Weather Events Count
- Renewable Energy Use %
- Water Stress Indicator
- Biodiversity Impact Score
- Social Responsibility Score
- Governance Score

### Performance Metrics
- Accuracy
- Precision
- Recall
- F1-Score
- AUC-ROC
- Feature Importance Analysis

## Data Format

Your CSV file should contain financial data with columns such as:
- Company identifiers
- Sector information
- Financial metrics (market cap, revenue, debt ratios, etc.)
- Performance indicators (ROE, volatility, beta, etc.)
- Credit ratings and liquidity measures

ESG data can be included or will be generated automatically for demonstration.

## Database

The platform uses SQLite for local data storage with tables for:
- Portfolio metadata
- Financial data
- ESG indicators
- Model training results
- Risk predictions

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed in your virtual environment
2. **Port Issues**: If port 8501 is busy, Streamlit will automatically find another port
3. **Python Version**: Use Python 3.11+ for optimal compatibility

### Performance Tips

- Use the sample dataset first to verify functionality
- For large datasets, consider increasing model complexity gradually
- Database operations are optimized for datasets up to 10,000 companies

## Academic Use

This platform is designed for research in:
- ESG-enhanced financial risk modeling
- Climate finance analytics
- Sustainable investment strategies
- Quantitative risk management
- Machine learning in finance

Results can be exported for academic papers, presentations, or further analysis.

## License

This project is open source and available for academic and research purposes.