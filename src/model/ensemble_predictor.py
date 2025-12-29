"""
Ensemble predictor combining multiple models
"""
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)


class EnsemblePredictor:
    """Ensemble model for fraud detection predictions"""
    
    def __init__(self, models: Dict[str, Any], weights: Dict[str, float] = None):
        """
        Initialize ensemble predictor
        
        Args:
            models: Dictionary of trained models
            weights: Dictionary of model weights (default: equal weights)
        """
        self.models = models
        
        if weights is None:
            # Equal weights by default
            n_models = len(models)
            self.weights = {name: 1.0 / n_models for name in models.keys()}
        else:
            # Normalize weights
            total = sum(weights.values())
            self.weights = {name: w / total for name, w in weights.items()}
        
        logger.info(f"Ensemble initialized with weights: {self.weights}")
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions using ensemble voting
        
        Args:
            X: Input features
            
        Returns:
            Predicted labels (0 or 1)
        """
        predictions = []
        
        for model_name, model in self.models.items():
            pred = model.predict(X)
            weight = self.weights[model_name]
            predictions.append(pred * weight)
        
        ensemble_pred = np.sum(predictions, axis=0)
        return (ensemble_pred >= 0.5).astype(int)
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Get probability predictions using ensemble
        
        Args:
            X: Input features
            
        Returns:
            Probability of fraud for each sample
        """
        probas = []
        
        for model_name, model in self.models.items():
            proba = model.predict_proba(X)[:, 1]
            weight = self.weights[model_name]
            probas.append(proba * weight)
        
        ensemble_proba = np.mean(probas, axis=0)
        return ensemble_proba
    
    def update_weights(self, weights: Dict[str, float]):
        """
        Update ensemble weights
        
        Args:
            weights: New weights dictionary
        """
        total = sum(weights.values())
        self.weights = {name: w / total for name, w in weights.items()}
        logger.info(f"Weights updated: {self.weights}")


if __name__ == "__main__":
    # Example usage
    from model_loader import ModelLoader
    
    loader = ModelLoader()
    models_dict = loader.load_all_models()
    
    ensemble = EnsemblePredictor(models_dict)
    # predictions = ensemble.predict(X_test)
