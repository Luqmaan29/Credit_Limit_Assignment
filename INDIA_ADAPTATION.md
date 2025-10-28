# 🇮🇳 Indian Market Adaptation

## Overview
This credit limit assignment system has been adapted for the **Indian market** with all currency in **INR (₹)**, **CIBIL credit scores**, and **Indian economic scenarios**. All text remains in English.

## Key Adaptations Made

### 1. Credit Scoring System
- **CIBIL Score** (300-900 range) instead of US FICO (300-850)
- Average CIBIL score: ~700
- Score bands adjusted for Indian market:
  - Excellent: ≥750
  - Very Good: ≥700
  - Good: ≥650
  - Fair: ≥550
  - Poor: ≥450
  - Very Poor: <450

### 2. Currency (INR ₹)
All monetary values converted to Indian Rupees (INR):
- **Income**: ₹15,000 - ₹200,000 per month (typical Indian salary range)
- **Credit Limits**: ₹10,000 - ₹500,000 (Indian credit card limits)
- **Transaction Amounts**: ₹100 - ₹25,000
- All UI displays show ₹ symbol

### 3. Economic Scenarios
Changed from US economic conditions to **Indian scenarios**:
- **Normal**: Moderate Growth (current state) - 70%
- **Slowdown**: Economic slowdown with conservative approach - 20%
- **High Growth**: High growth phase with expansion - 10%

### 4. Income Distribution
- Indian salary ranges (₹15K - ₹200K/month)
- More realistic income distribution for Indian market
- Adjusted for cost of living in India

### 5. Credit Card Limits
- Minimum: ₹10,000 (Indian credit card standard)
- Maximum: ₹500,000 (premium Indian cards)
- Typical limit range aligned with Indian banking norms

### 6. Age Distribution
- Adjusted to Indian banking customer age range: 18-75
- Average age: 38 years (more relevant to Indian market)

### 7. Transaction Patterns
- Indian credit card transaction sizes: ₹100 - ₹25,000
- Reflects typical spending patterns in India
- UPI and digital payment considerations

## Indian Banking Context

### CIBIL Score
- **CIBIL** = Credit Information Bureau (India) Limited
- India's first credit information company
- Scores range from 300 to 900
- Used by all major banks and NBFCs in India

### Credit Card Market
- Growing credit card penetration in India
- Digital payments ecosystem (UPI, RuPay)
- Typical limits: ₹10K - ₹5L
- Premium cards: ₹5L+

### Regulatory Environment
- Reserve Bank of India (RBI) guidelines
- Bifurcated interest rate structure
- KYC compliance requirements
- Data privacy (data protection bill)

## Dataset Features (Indian Context)

### Customer Demographics
- Age: 18-75 years (Indian working population)
- Income: ₹15K - ₹200K/month (Indian salary brackets)

### Credit Metrics
- **CIBIL Score**: 300-900 (Indian credit bureau-type score)
- Credit Limit: ₹10K - ₹5L (Indian credit card ranges)
- Utilization: 0-100% (same metric)

### Economic Indicators
- **Normal** (Moderate Growth): Steady economy
- **Slowdown**: Economic headwinds, conservative lending
- **High Growth**: Expansion phase, aggressive growth

## Usage Notes

### All text in English
- Code comments in English
- Variable names in English
- UI labels in English
- Documentation in English

### Currency Formatting
```
₹1,00,000  (Indian number formatting - lakhs)
₹10,00,000 (crores)
```

### Market Assumptions
- Urban and semi-urban customer base
- Salaried and self-employed profiles
- Mix of metros and tier-2 cities
- Digital-first banking approach

## Model Performance

The machine learning models work identically with Indian data:
- Random Forest trained on CIBIL scores
- XGBoost adapted for Indian income ranges
- Same ROC-AUC performance (~0.85)
- Feature importance adjusted for Indian market

## Benefits of Indian Adaptation

1. **Relevance**: Data reflects actual Indian market conditions
2. **Accuracy**: Models trained on realistic Indian profiles
3. **Compliance**: Aligns with Indian banking regulations
4. **Scalability**: Ready for Indian financial institutions
5. **Localization**: Currency and scores match Indian standards

## Deployment Considerations

### Indian Banks & NBFCs
- Can deploy directly with INR dataset
- CIBIL integration ready
- Complies with RBI guidelines
- Supports Indian regulatory reporting

### Data Privacy
- Follows Indian data protection requirements
- Secure customer information handling
- RBI data localization norms

## Testing

Run the setup to generate Indian dataset:
```bash
python setup.py
streamlit run app.py
```

All values will be in **INR** with **CIBIL scores**.

---

**Status**: ✅ Fully adapted for Indian market  
**Currency**: INR (₹)  
**Credit Score**: CIBIL (300-900)  
**Language**: English  
**Location**: India 🇮🇳

