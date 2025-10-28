"""
Scenario Analysis for Credit Limit Assignment - Indian Market
Analyzes different Indian economic conditions and their impact on credit decisions
"""

import pandas as pd
import numpy as np

class ScenarioAnalyzer:
    """Analyze credit limits under different economic scenarios"""
    
    SCENARIO_MULTIPLIERS = {
        'normal': 1.0,       # Moderate growth (current)
        'slowdown': 0.75,    # More conservative in economic slowdown
        'high_growth': 1.25  # More aggressive in high growth
    }
    
    def __init__(self):
        self.results = {}
    
    def apply_scenario_adjustment(self, base_limit, scenario):
        """Adjust credit limit based on economic scenario"""
        multiplier = self.SCENARIO_MULTIPLIERS.get(scenario, 1.0)
        return base_limit * multiplier
    
    def analyze_scenarios(self, df):
        """
        Analyze how credit limits would change under different scenarios
        
        Parameters:
        - df: DataFrame with customer data and recommended limits
        """
        scenarios = ['normal', 'slowdown', 'high_growth']
        analysis_results = []
        
        for scenario in scenarios:
            scenario_name = scenario.title()
            
            # Apply scenario multiplier
            adjusted_limits = df['recommended_limit'].apply(
                lambda x: self.apply_scenario_adjustment(x, scenario)
            )
            
            # Calculate aggregate statistics
            avg_limit = adjusted_limits.mean()
            total_credit_exposure = adjusted_limits.sum()
            high_risk_customers = len(df[df['default_probability'] > 0.35])
            
            # Calculate weighted average risk
            weighted_risk = (df['default_probability'] * adjusted_limits).sum() / adjusted_limits.sum()
            
            analysis_results.append({
                'scenario': scenario_name,
                'avg_credit_limit': round(avg_limit, 2),
                'total_exposure': round(total_credit_exposure, 2),
                'high_risk_customers': high_risk_customers,
                'weighted_avg_risk': round(weighted_risk, 3),
                'total_customers': len(df),
                'avg_limit_change_pct': round(
                    ((adjusted_limits - df['current_credit_limit']).mean() / 
                     df['current_credit_limit'].mean()) * 100, 2
                )
            })
        
        return pd.DataFrame(analysis_results)
    
    def get_scenario_recommendation(self, df):
        """Generate recommendation based on scenario analysis"""
        scenario_df = self.analyze_scenarios(df)
        
        recommendations = []
        
        for _, row in scenario_df.iterrows():
            scenario = row['scenario']
            avg_limit = row['avg_credit_limit']
            weighted_risk = row['weighted_avg_risk']
            high_risk = row['high_risk_customers']
            
            if scenario == 'Normal':
                if weighted_risk < 0.2 and high_risk < 100:
                    rec = f"{scenario}: Moderate growth strategy suitable. Low overall risk."
                elif weighted_risk < 0.3:
                    rec = f"{scenario}: Balanced approach recommended. Moderate risk."
                else:
                    rec = f"{scenario}: Conservative approach needed. High risk profile."
            
            elif scenario == 'Slowdown':
                if weighted_risk > 0.3:
                    rec = f"{scenario}: Strongly recommend credit reduction. High risk exposure during slowdown."
                elif high_risk > 150:
                    rec = f"{scenario}: Implement selective credit decreases. Monitor high-risk customers."
                else:
                    rec = f"{scenario}: Maintain conservative limits. Stable low-risk portfolio."
            
            else:  # High Growth
                if weighted_risk < 0.25 and high_risk < 80:
                    rec = f"{scenario}: Opportunity to expand credit. Strong customer base in growth phase."
                else:
                    rec = f"{scenario}: Selective credit expansion. Target low-risk segments."
            
            recommendations.append(rec)
        
        scenario_df['recommendation'] = recommendations
        
        return scenario_df
    
    def calculate_stress_test_metrics(self, df, shock_scenarios):
        """
        Calculate stress test metrics under economic shocks
        
        Parameters:
        - df: DataFrame with customer data
        - shock_scenarios: dict with scenario name and default probability multipliers
        """
        stress_results = []
        
        for scenario_name, shock_multiplier in shock_scenarios.items():
            # Apply shock to default probabilities
            stressed_default_probs = df['predicted_default_prob'] * shock_multiplier
            stressed_default_probs = np.clip(stressed_default_probs, 0, 1)
            
            # Calculate expected defaults
            expected_defaults = (stressed_default_probs * 
                                       df['recommended_limit']).sum()
            
            # Calculate risk concentration
            high_risk_exposure = df[stressed_default_probs > 0.35]['recommended_limit'].sum()
            total_exposure = df['recommended_limit'].sum()
            
            stress_results.append({
                'scenario': scenario_name,
                'shock_multiplier': shock_multiplier,
                'expected_default_loss': round(expected_defaults, 2),
                'high_risk_exposure': round(high_risk_exposure, 2),
                'concentration_ratio': round(high_risk_exposure / total_exposure, 3),
                'avg_stressed_default_prob': round(stressed_default_probs.mean(), 3)
            })
        
        return pd.DataFrame(stress_results)

