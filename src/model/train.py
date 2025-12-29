"""
Model Training Module
Trains Isolation Forest and XGBoost models
"""

import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import f1_score, precision_score, recall_score


class IsolationForestModel:
    """Isolation Forest for anomaly detection"""
    
    def __init__(self, contamination, n_estimators=150, random_state=42):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = None
        self.anomaly_scores = None
        
    def fit(self, X_train):
        """Train Isolation Forest"""
        print("\n🔧 Entraînement Isolation Forest...")
        
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            max_samples='auto',
            max_features=0.8,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        self.model.fit(X_train)
        print(f"✓ Isolation Forest entraîné")
        
        return self
    
    def score_samples(self, X):
        """Get anomaly scores"""
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        return self.model.score_samples(X)
    
    def predict(self, X):
        """Get predictions"""
        return self.model.predict(X)


class XGBoostModel:
    """XGBoost with SMOTE for imbalanced data"""
    
    def __init__(self, scale_pos_weight, n_estimators=300, random_state=42):
        self.scale_pos_weight = scale_pos_weight
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.pipeline = None
        
    def fit(self, X_train, y_train):
        """Train XGBoost with SMOTE"""
        print("\n🔧 Entraînement XGBoost avec SMOTE...")
        
        xgb = XGBClassifier(
            objective='binary:logistic',
            eval_metric='logloss',
            n_estimators=self.n_estimators,
            max_depth=7,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=2,
            gamma=1.0,
            reg_lambda=5.0,
            reg_alpha=1.0,
            scale_pos_weight=self.scale_pos_weight,
            tree_method='hist',
            random_state=self.random_state,
            n_jobs=-1
        )
        
        # Create pipeline with SMOTE
        self.pipeline = ImbPipeline([
            ('smote', SMOTE(random_state=self.random_state, k_neighbors=5)),
            ('xgb', xgb)
        ])
        
        self.pipeline.fit(X_train, y_train)
        print(f"✓ XGBoost entraîné avec SMOTE")
        print(f"  Scale pos weight: {self.scale_pos_weight:.2f}")
        
        return self
    
    def predict_proba(self, X):
        """Get probability predictions"""
        if self.pipeline is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        return self.pipeline.predict_proba(X)
    
    def predict(self, X):
        """Get binary predictions"""
        return self.pipeline.predict(X)


class ModelTrainer:
    """
    Complete model training orchestration
    """
    
    def __init__(self, random_state=42, models_dir='models'):
        self.random_state = random_state
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.iso_forest = None
        self.xgb_model = None
        
    def train_both_models(self, X_train_scaled, y_train):
        """Train both Isolation Forest and XGBoost"""
        
        # Calculate contamination for IF
        contamination = (y_train == 1).sum() / len(y_train)
        
        # Train Isolation Forest
        self.iso_forest = IsolationForestModel(
            contamination=contamination,
            random_state=self.random_state
        )
        self.iso_forest.fit(X_train_scaled)
        
        # Calculate scale_pos_weight for XGBoost
        neg_count = np.sum(y_train == 0)
        pos_count = np.sum(y_train == 1)
        scale_pos_weight = neg_count / pos_count
        
        # Train XGBoost
        self.xgb_model = XGBoostModel(
            scale_pos_weight=scale_pos_weight,
            random_state=self.random_state
        )
        self.xgb_model.fit(X_train_scaled, y_train)
        
        return {
            'iso_forest': self.iso_forest,
            'xgb_model': self.xgb_model
        }
    
    def save_models(self):
        """Save trained models"""
        if self.iso_forest and self.xgb_model:
            joblib.dump(self.iso_forest.model, 
                       self.models_dir / 'isolation_forest.joblib')
            joblib.dump(self.xgb_model.pipeline, 
                       self.models_dir / 'xgboost.joblib')
            
            print(f"\n✓ Modèles sauvegardés dans {self.models_dir}")


if __name__ == "__main__":
    from src.data.data_pipeline import DataProcessor
    
    # Get data
    processor = DataProcessor()
    data = processor.run()
    
    # Train models
    trainer = ModelTrainer()
    models = trainer.train_both_models(
        data['X_train_scaled'],
        data['y_train']
    )
    
    # Get predictions
    iso_scores = models['iso_forest'].score_samples(data['X_test_scaled'])
    xgb_proba = models['xgb_model'].predict_proba(data['X_test_scaled'])[:, 1]
    
    print(f"\n✅ Models trained successfully!")
    print(f"  IF scores range: [{iso_scores.min():.4f}, {iso_scores.max():.4f}]")
    print(f"  XGB proba range: [{xgb_proba.min():.4f}, {xgb_proba.max():.4f}]")
