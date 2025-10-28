"""
Credit Risk Model Training
Implements Random Forest and XGBoost for default probability prediction
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
import xgboost as xgb

class CreditRiskModel:
    """Credit risk prediction model using Random Forest and XGBoost"""
    
    def __init__(self):
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        self.feature_columns = None
        self.models_trained = False
        
    def prepare_features(self, df):
        """Prepare features for model training"""
        # Select features (exclude identifiers and targets)
        exclude_cols = ['customer_id', 'default_probability', 'defaulted']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols]
        y = df['defaulted']
        
        if self.feature_columns is None:
            self.feature_columns = feature_cols
        
        return X, y
    
    def train_models(self, df):
        """Train both Random Forest and XGBoost models"""
        print("Preparing features...")
        X, y = self.prepare_features(df)
        
        print(f"Training with {len(X)} samples and {len(X.columns)} features")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest
        print("\nTraining Random Forest model...")
        self.rf_model.fit(X_train, y_train)
        rf_proba = self.rf_model.predict_proba(X_test)[:, 1]
        rf_pred = self.rf_model.predict(X_test)
        
        print(f"Random Forest - Accuracy: {accuracy_score(y_test, rf_pred):.4f}")
        print(f"Random Forest - ROC-AUC: {roc_auc_score(y_test, rf_proba):.4f}")
        
        # Train XGBoost
        print("\nTraining XGBoost model...")
        self.xgb_model.fit(X_train, y_train)
        xgb_proba = self.xgb_model.predict_proba(X_test)[:, 1]
        xgb_pred = self.xgb_model.predict(X_test)
        
        print(f"XGBoost - Accuracy: {accuracy_score(y_test, xgb_pred):.4f}")
        print(f"XGBoost - ROC-AUC: {roc_auc_score(y_test, xgb_proba):.4f}")
        
        self.models_trained = True
        
        return X_train, X_test, y_train, y_test
    
    def predict_default_probability(self, df):
        """Predict default probability for given customers"""
        if not self.models_trained:
            raise ValueError("Models not trained yet. Call train_models() first.")
        
        X, _ = self.prepare_features(df)
        
        # Get predictions from both models
        rf_proba = self.rf_model.predict_proba(X)[:, 1]
        xgb_proba = self.xgb_model.predict_proba(X)[:, 1]
        
        # Ensemble prediction (average)
        ensemble_proba = (rf_proba + xgb_proba) / 2
        
        return ensemble_proba
    
    def get_feature_importance(self):
        """Get feature importance from trained models"""
        if not self.models_trained:
            raise ValueError("Models not trained yet. Call train_models() first.")
        
        rf_importance = self.rf_model.feature_importances_
        xgb_importance = self.xgb_model.feature_importances_
        
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'rf_importance': rf_importance,
            'xgb_importance': xgb_importance,
            'avg_importance': (rf_importance + xgb_importance) / 2
        }).sort_values('avg_importance', ascending=False)
        
        return importance_df
    
    def save_models(self, filepath='models/'):
        """Save trained models"""
        import os
        os.makedirs(filepath, exist_ok=True)
        
        with open(f'{filepath}rf_model.pkl', 'wb') as f:
            pickle.dump(self.rf_model, f)
        
        with open(f'{filepath}xgb_model.pkl', 'wb') as f:
            pickle.dump(self.xgb_model, f)
        
        with open(f'{filepath}feature_columns.pkl', 'wb') as f:
            pickle.dump(self.feature_columns, f)
        
        print(f"Models saved to {filepath}")
    
    def load_models(self, filepath='models/'):
        """Load trained models"""
        with open(f'{filepath}rf_model.pkl', 'rb') as f:
            self.rf_model = pickle.load(f)
        
        with open(f'{filepath}xgb_model.pkl', 'rb') as f:
            self.xgb_model = pickle.load(f)
        
        with open(f'{filepath}feature_columns.pkl', 'rb') as f:
            self.feature_columns = pickle.load(f)
        
        self.models_trained = True
        print(f"Models loaded from {filepath}")

def train_and_save_model():
    """Main function to train and save the model"""
    # Load data
    print("Loading data...")
    df = pd.read_csv('data/credit_data.csv')
    
    # Train model
    model = CreditRiskModel()
    model.train_models(df)
    
    # Save model
    model.save_models()
    
    # Get feature importance
    importance = model.get_feature_importance()
    print("\nTop 10 Most Important Features:")
    print(importance.head(10))
    
    # Save feature importance
    importance.to_csv('models/feature_importance.csv', index=False)

if __name__ == '__main__':
    train_and_save_model()


