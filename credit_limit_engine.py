"""
Credit Limit Assignment Engine - Indian Market
Calculates risk-adjusted credit limits (INR) based on CIBIL score and default probability
All text in English
"""

import pandas as pd
import numpy as np

class CreditLimitEngine:
    """Engine for calculating adaptive credit limits based on risk"""
    
    def __init__(self):
        self.base_multiplier = 2.5  # Base credit limit = income * multiplier
        
    def calculate_base_limit(self, monthly_income, credit_score):
        """
        Calculate base credit limit (INR) based on income and CIBIL score
        
        Formula:
        - Base limit = Monthly Income × Base Multiplier
        - Adjust based on CIBIL score band (300-900 scale)
        """
        # CIBIL score adjustments (Indian credit scoring)
        if credit_score >= 750:
            score_multiplier = 1.5  # Excellent
        elif credit_score >= 700:
            score_multiplier = 1.3  # Very Good
        elif credit_score >= 650:
            score_multiplier = 1.1  # Good
        elif credit_score >= 550:
            score_multiplier = 1.0  # Fair
        elif credit_score >= 450:
            score_multiplier = 0.8  # Poor
        else:
            score_multiplier = 0.5  # Very Poor
        
        base_limit = monthly_income * 1000 * self.base_multiplier * score_multiplier
        
        return base_limit
    
    def apply_risk_adjustment(self, base_limit, default_prob, utilization, 
                             on_time_payment_rate, behavior_score):
        """
        Adjust credit limit based on risk factors
        
        Risk factors:
        - Default probability (primary)
        - Current utilization
        - Payment history
        - Behavior score
        """
        # Start with risk adjustment based on default probability
        risk_multiplier = 1 - (default_prob * 0.6)  # Reduce by up to 60% based on risk
        
        # Adjust for high utilization (risk of overextension)
        if utilization > 0.8:
            risk_multiplier *= 0.9
        elif utilization < 0.3:
            risk_multiplier *= 1.1  # Reward low utilization
        
        # Payment history adjustment
        payment_adjustment = on_time_payment_rate * 0.1
        risk_multiplier += payment_adjustment
        
        # Behavior score adjustment
        behavior_adjustment = behavior_score * 0.1
        risk_multiplier += behavior_adjustment
        
        # Ensure multiplier is within reasonable bounds
        risk_multiplier = np.clip(risk_multiplier, 0.2, 2.0)
        
        return base_limit * risk_multiplier
    
    def calculate_recommended_limit(self, row):
        """
        Calculate recommended credit limit for a customer
        
        Parameters:
        - row: DataFrame row with customer data
        """
        # Get base limit
        base_limit = self.calculate_base_limit(
            row['monthly_income'], 
            row['credit_score']
        )
        
        # Apply risk adjustments
        recommended_limit = self.apply_risk_adjustment(
            base_limit,
            row['predicted_default_prob'],
            row['credit_utilization'],
            row['on_time_payment_rate'],
            row['behavior_score']
        )
        
        # Apply constraints (Indian market)
        # Minimum limit: ₹10,000
        # Maximum limit: ₹500,000
        recommended_limit = max(10000, min(recommended_limit, 500000))
        
        return recommended_limit
    
    def calculate_credit_change(self, current_limit, recommended_limit):
        """Calculate credit limit change amount and percentage"""
        change_amount = recommended_limit - current_limit
        change_percentage = (change_amount / current_limit) * 100
        
        return change_amount, change_percentage
    
    def assign_risk_category(self, default_prob):
        """Assign risk category based on default probability"""
        if default_prob < 0.1:
            return "Low Risk"
        elif default_prob < 0.25:
            return "Medium Risk"
        elif default_prob < 0.4:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def calculate_adjustment_reason(self, row):
        """Generate reason for credit limit adjustment"""
        reasons = []
        
        if row['predicted_default_prob'] < 0.15:
            reasons.append("Excellent risk profile")
        elif row['predicted_default_prob'] > 0.35:
            reasons.append("Elevated default risk")
        
        if row['on_time_payment_rate'] > 0.95:
            reasons.append("Strong payment history")
        elif row['on_time_payment_rate'] < 0.7:
            reasons.append("Poor payment history")
        
        if row['credit_utilization'] > 0.8:
            reasons.append("High current utilization")
        elif row['credit_utilization'] < 0.3:
            reasons.append("Low utilization pattern")
        
        if row['behavior_score'] > 0.8:
            reasons.append("Good customer behavior")
        
        return " | ".join(reasons) if reasons else "Balanced profile"
    
    def process_customers(self, df):
        """
        Process all customers and calculate recommended limits
        
        Parameters:
        - df: DataFrame with customer data and predicted_default_prob column
        """
        results = []
        
        for idx, row in df.iterrows():
            recommended_limit = self.calculate_recommended_limit(row)
            change_amount, change_pct = self.calculate_credit_change(
                row['current_credit_limit'], recommended_limit
            )
            
            risk_category = self.assign_risk_category(row['predicted_default_prob'])
            reason = self.calculate_adjustment_reason(row)
            
            results.append({
                'customer_id': row.get('customer_id', f'CUST_{idx}'),
                'current_limit': row['current_credit_limit'],
                'recommended_limit': round(recommended_limit, 2),
                'change_amount': round(change_amount, 2),
                'change_percentage': round(change_pct, 2),
                'risk_category': risk_category,
                'default_probability': row['predicted_default_prob'],
                'adjustment_reason': reason,
                'credit_score': row['credit_score'],
                'utilization': row['credit_utilization'],
                'on_time_payment_rate': row['on_time_payment_rate']
            })
        
        return pd.DataFrame(results)

