# 🚀 Quick Start Guide

## Get Started in 3 Steps!

### Step 1: Setup (One-time)
```bash
python setup.py
```
This will:
- ✓ Install all dependencies
- ✓ Generate synthetic credit dataset (2,000 customers)
- ✓ Train Random Forest and XGBoost models

### Step 2: Launch Dashboard
```bash
streamlit run app.py
```
Dashboard opens at `http://localhost:8501`

### Step 3: Explore!
- Use sidebar to navigate between 5 pages
- Filter customers by risk category
- Analyze recommendations
- View scenario analysis

---

## Alternative: Use Scripts

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

---

## What You'll See

### 📊 Overview Dashboard
- Total customers: 2,000
- Average credit score: ~650
- Risk breakdown
- Portfolio statistics

### 🎯 Recommendations
- Current limits vs recommended limits
- Increase/decrease suggestions
- Risk-adjusted calculations
- Filter by category

### 📈 Risk Analysis
- Default probability distribution
- Feature importance
- High-risk customers
- Portfolio exposure

### 🌍 Scenarios
- Normal economy settings
- Recession adjustments (-25%)
- Growth opportunities (+25%)
- Recommendations per scenario

### 🔍 Customer Details
- Search any customer
- Detailed risk profile
- Recommendation reasoning
- Payment history

---

## Dataset Information

**Features:** 19 customer attributes
- Demographics (age, income)
- Credit metrics (score, utilization, debt-to-income)
- Payment behavior (on-time rate, late payments, history)
- Transaction patterns (volume, amounts, behavior)
- Risk indicators (default prob, bankruptcy, delinquency)
- Economic context (normal/recession/growth scenario)

**Size:** 2,000 customers with realistic correlations

---

## Customization

### Adjust Credit Limit Calculation
Edit `credit_limit_engine.py`:
```python
self.base_multiplier = 2.5  # Change this value
```

### Modify Risk Adjustment
Edit line 47-56 in `credit_limit_engine.py`

### Change Model Parameters
Edit `model_training.py`:
```python
RandomForestClassifier(n_estimators=200)  # Add more trees
```

---

## Troubleshooting

**"Data file not found"**
→ Run `python data_generator.py`

**"Models not found"**
→ Run `python model_training.py`

**Dashboard slow?**
→ Reduce dataset size in `data_generator.py` (change n_samples)

**Import errors?**
→ Run `pip install -r requirements.txt`

---

## Key Formula

```
Recommended Credit Limit = 
    Base Limit × Risk Multiplier × Adjustments

Where:
- Base = Income × 2.5 × Credit Score Factor
- Risk Multiplier = 1 - (Default Prob × 0.6)
- Adjustments = Payment History + Behavior Score
```

---

## Questions?

Check `README.md` for full documentation.
See `PROJECT_SUMMARY.md` for feature overview.

---

**Ready to analyze? Run:**
```bash
streamlit run app.py
```

🎉 Happy analyzing!

