"""
Synthetic Credit Limit Dataset Generator - Indian Market
Creates realistic customer data for Indian credit market (CIBIL, INR)
All text in English, adapted for Indian economic context
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_credit_dataset(n_samples=1000, random_seed=42):
    """
    Generate a synthetic credit dataset for Indian credit market
    
    Features:
    - Customer demographics (Indian context)
    - CIBIL credit score (300-900)
    - Income in INR
    - Repayment behavior
    - Risk indicators
    - Indian economic scenarios
    """
    np.random.seed(random_seed)
    
    # Customer Demographics
    customer_ids = [f'CUST_{i:05d}' for i in range(1, n_samples + 1)]
    ages = np.random.normal(38, 10, n_samples).astype(int)  # Indian banking age distribution
    ages = np.clip(ages, 18, 75)
    
    # CIBIL Credit Score (Indian range: 300-900)
    credit_score = np.random.normal(700, 100, n_samples).astype(int)
    credit_score = np.clip(credit_score, 300, 900)
    
    # Account Activity
    months_account_open = np.random.gamma(3, 8, n_samples).astype(int)
    months_account_open = np.clip(months_account_open, 1, 120)
    
    # Monthly Income (INR in thousands) - Indian salary ranges
    # Typical range: ₹15K - ₹200K per month
    monthly_income = np.random.lognormal(3.5, 0.7, n_samples)
    monthly_income = np.clip(monthly_income, 15, 200)
    
    # Debt-to-Income Ratio
    debt_to_income = np.random.beta(2, 5, n_samples) * 0.7
    debt_to_income = debt_to_income + np.random.normal(0, 0.05, n_samples)
    debt_to_income = np.clip(debt_to_income, 0, 0.9)
    
    # Current Credit Limit (INR)
    # Typical range: ₹10K - ₹500K for credit cards in India
    current_limit = np.random.lognormal(4, 0.9, n_samples) * 1000
    current_limit = np.clip(current_limit, 10000, 500000)
    
    # Credit Utilization Ratio
    utilization = np.random.beta(2, 3, n_samples)
    utilization = np.clip(utilization, 0, 1)
    
    # Repayment Behavior Metrics
    payment_history_score = np.random.beta(7, 2, n_samples)
    
    # Number of Late Payments (last 12 months)
    late_payments_12m = np.random.poisson(2, n_samples)
    late_payments_12m = np.clip(late_payments_12m, 0, 12)
    
    # Payment Consistency (% on-time payments)
    on_time_payment_rate = 1 - (late_payments_12m / 12) + np.random.normal(0, 0.1, n_samples)
    on_time_payment_rate = np.clip(on_time_payment_rate, 0, 1)
    
    # Transaction Volume
    avg_monthly_transactions = np.random.gamma(5, 20, n_samples)
    avg_monthly_transactions = np.clip(avg_monthly_transactions, 5, 200)
    
    # Transaction Amount (INR)
    # Typical Indian credit card transaction sizes
    avg_transaction_amount = np.random.lognormal(3.5, 0.7, n_samples)
    avg_transaction_amount = np.clip(avg_transaction_amount, 100, 25000)
    
    # Customer Behavior Score (composite)
    behavior_score = (payment_history_score * 0.4 + 
                     on_time_payment_rate * 0.3 + 
                     (1 - utilization) * 0.2 + 
                     (credit_score / 900) * 0.1)  # CIBIL max is 900
    behavior_score = np.clip(behavior_score, 0, 1)
    
    # Risk Factors
    has_bankruptcy = np.random.binomial(1, 0.05, n_samples)
    has_delinquency = np.random.binomial(1, 0.15, n_samples)
    high_utilization_flag = (utilization > 0.8).astype(int)
    
    # Indian Economic Scenario Indicator
    # 0: Normal (Moderate Growth), 1: Slowdown, 2: High Growth
    economic_scenario = np.random.choice([0, 1, 2], n_samples, p=[0.7, 0.2, 0.1])
    
    # Generate default probability (target variable)
    # Based on combination of risk factors (adjusted for CIBIL score)
    default_prob = (
        0.3 * (1 - behavior_score) +
        0.25 * (1 - credit_score / 900) +  # CIBIL max is 900
        0.2 * utilization +
        0.15 * debt_to_income / 0.5 +
        0.05 * has_bankruptcy +
        0.05 * has_delinquency
    )
    
    # Add noise
    default_prob += np.random.normal(0, 0.05, n_samples)
    default_prob = np.clip(default_prob, 0, 1)
    
    # Generate actual default outcome (0 or 1)
    defaulted = np.random.binomial(1, default_prob, n_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'age': ages,
        'credit_score': credit_score,
        'months_account_open': months_account_open,
        'monthly_income': monthly_income.round(2),
        'debt_to_income_ratio': debt_to_income.round(3),
        'current_credit_limit': current_limit.round(2),
        'credit_utilization': utilization.round(3),
        'payment_history_score': payment_history_score.round(3),
        'late_payments_12m': late_payments_12m,
        'on_time_payment_rate': on_time_payment_rate.round(3),
        'avg_monthly_transactions': avg_monthly_transactions.round(1),
        'avg_transaction_amount': avg_transaction_amount.round(2),
        'behavior_score': behavior_score.round(3),
        'has_bankruptcy': has_bankruptcy,
        'has_delinquency': has_delinquency,
        'high_utilization': high_utilization_flag,
        'economic_scenario': economic_scenario,
        'default_probability': default_prob.round(3),
        'defaulted': defaulted
    })
    
    return df

def save_dataset():
    """Generate and save the dataset"""
    print("Generating synthetic credit dataset...")
    df = generate_credit_dataset(n_samples=2000)
    
    # Save to CSV
    df.to_csv('data/credit_data.csv', index=False)
    print(f"Dataset saved to data/credit_data.csv with {len(df)} records")
    
    # Print basic statistics
    print("\nDataset Statistics:")
    print(df.describe())
    
    return df

if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    save_dataset()


