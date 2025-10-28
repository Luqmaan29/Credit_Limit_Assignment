# 💳 Dynamic Credit Limit Assignment System

A comprehensive credit limit assignment system that uses machine learning to suggest adaptive credit limits for customers based on their historical repayment behavior, account activity, and risk profile.

## 📋 Features

- **Predictive Models**: Uses Random Forest and XGBoost to estimate default probability
- **Risk-Adjusted Credit Allocation**: Calculates credit limits based on individual risk profiles
- **Scenario Analysis**: Optimizes credit adjustments under different economic conditions
- **Interactive Dashboard**: Streamlit-based UI for monitoring and decision-making
- **Comprehensive Analysis**: Customer risk assessment, utilization tracking, and recommendations

## 🎯 System Capabilities

### 1. Risk Prediction
- Predicts customer default probability using ensemble models
- Considers 18+ features including credit history, payment behavior, and account activity

### 2. Credit Limit Calculation
- Base limit calculation based on income and credit score
- Risk-adjusted adjustments based on default probability
- Multiple factor consideration (utilization, payment history, behavior)

### 3. Scenario Analysis
- **Normal**: Standard credit limit recommendations
- **Recession**: Conservative approach with reduced limits
- **Growth**: Aggressive expansion for low-risk customers

### 4. Dashboard Features
- **Overview**: Portfolio statistics and distributions
- **Recommendations**: Customer-specific credit limit suggestions
- **Risk Analysis**: Heatmaps and risk metrics
- **Scenario Analysis**: Economic condition impact analysis
- **Customer Details**: Individual customer drill-down

## 📊 Dataset Description

The system uses a synthetic dataset with the following features:

### Customer Demographics
- Customer ID
- Age
- Monthly Income

### Credit Metrics
- Credit Score
- Current Credit Limit
- Credit Utilization
- Debt-to-Income Ratio

### Historical Behavior
- Months Account Open
- Payment History Score
- Late Payments (12 months)
- On-Time Payment Rate

### Transaction Patterns
- Average Monthly Transactions
- Average Transaction Amount
- Customer Behavior Score

### Risk Indicators
- Default Probability
- Bankruptcy History
- Delinquency Flag
- High Utilization Flag

### Economic Context
- Economic Scenario (Normal/Recession/Growth)

**Total Features**: 19 customer attributes + default probability + default flag

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd Credit_Limit
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Run the setup script**
   ```bash
   python setup.py
   ```

   This will:
   - Install all required packages
   - Generate a synthetic dataset (2,000 customers)
   - Train the machine learning models

4. **Launch the Streamlit app**
   ```bash
   streamlit run app.py
   ```

   Or on Windows:
   ```bash
   python -m streamlit run app.py
   ```

The dashboard will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Credit_Limit/
├── app.py                      # Main Streamlit application
├── data_generator.py           # Synthetic data generation
├── model_training.py           # ML model training (RF + XGBoost)
├── credit_limit_engine.py     # Credit limit calculation logic
├── scenario_analysis.py        # Economic scenario analysis
├── setup.py                    # Setup automation script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── credit_data.csv         # Generated dataset
└── models/
    ├── rf_model.pkl            # Random Forest model
    ├── xgb_model.pkl           # XGBoost model
    ├── feature_columns.pkl     # Feature names
    └── feature_importance.csv  # Feature importance ranking
```

## 🎨 Using the Dashboard

### 1. Overview Tab
- View portfolio summary statistics
- Analyze credit score distribution
- Review utilization patterns
- Explore risk categorizations

### 2. Credit Recommendations Tab
- Filter customers by risk category
- View current vs recommended limits
- Analyze credit adjustments
- Export recommendation lists

### 3. Risk Analysis Tab
- Identify high-risk customers
- Analyze portfolio exposure
- Review feature importance
- Evaluate risk concentration

### 4. Scenario Analysis Tab
- Compare Normal, Recession, and Growth scenarios
- Analyze total exposure differences
- Review weighted risk metrics
- Get scenario-specific recommendations

### 5. Customer Details Tab
- Search individual customers
- View detailed risk profile
- Review recommendation rationale
- Analyze payment behavior

## 🧪 Model Details

### Machine Learning Models

**1. Random Forest Classifier**
- 100 trees
- Max depth: 10
- Handles non-linear relationships
- Robust to outliers

**2. XGBoost Classifier**
- 100 estimators
- Max depth: 6
- Learning rate: 0.1
- Gradient boosting for accuracy

**Ensemble Method**: Average of both model predictions

### Model Accuracy
- Trained on 2,000 samples
- 80/20 train-test split
- Typical ROC-AUC scores above 0.85
- Balanced accuracy for risk and opportunity

## 📈 Key Metrics Explained

### Risk Categories
- **Low Risk**: Default probability < 10%
- **Medium Risk**: Default probability 10-25%
- **High Risk**: Default probability 25-40%
- **Very High Risk**: Default probability > 40%

### Credit Limit Formula

```
Recommended Limit = Base Limit × Risk Multiplier × Factor Adjustments

Where:
- Base Limit = Monthly Income × 2.5 × Credit Score Multiplier
- Risk Multiplier = 1 - (Default Probability × 0.6)
- Factor Adjustments consider:
  - Credit utilization
  - Payment history
  - Behavior score
```

## 🔧 Customization

### Adjust Model Parameters
Edit `model_training.py` to modify:
- Number of trees/estimators
- Max depth
- Learning rate
- Feature selection

### Modify Credit Limit Logic
Edit `credit_limit_engine.py` to adjust:
- Base multiplier
- Risk adjustment weights
- Limit constraints
- Scenario multipliers

### Add Features
Edit `data_generator.py` to include:
- New synthetic features
- Different distributions
- Custom correlations

## 📊 Performance Optimization

### For Large Datasets (>10,000 customers)
1. Increase model n_estimators to 200
2. Add data sampling for dashboard performance
3. Implement caching for predictions
4. Use database instead of CSV

### For Real-Time Predictions
1. Pre-train and save models
2. Use model inference APIs
3. Batch predictions
4. Implement model retraining schedule

## 🛠️ Troubleshooting

### "Data file not found" error
Run the setup script:
```bash
python setup.py
```

### Models not loading
Re-train models:
```bash
python model_training.py
```

### Dashboard not updating
Clear Streamlit cache:
```bash
streamlit cache clear
```

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to fork, modify, and adapt this system for your specific credit risk management needs.

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Modify parameters as needed for your use case

---

**Built with**: Python, Scikit-learn, XGBoost, Pandas, Streamlit, Plotly  
**Version**: 2025  
**Status**: Production-ready demonstration system

