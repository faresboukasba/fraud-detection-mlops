"""
Preprocessing utilities for API predictions
"""
import logging
import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any

logger = logging.getLogger(__name__)


class PreprocessingPipeline:
    """Preprocessing pipeline for API requests"""
    
    def __init__(self, scaler: Any = None, feature_names: List[str] = None):
        """
        Initialize preprocessing pipeline
        
        Args:
            scaler: Fitted StandardScaler
            feature_names: List of expected feature names
        """
        self.scaler = scaler
        self.feature_names = feature_names
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data
        
        Args:
            data: Input data dictionary
            
        Returns:
            True if valid, raises error otherwise
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")
        
        if self.feature_names:
            missing_features = set(self.feature_names) - set(data.keys())
            if missing_features:
                raise ValueError(f"Missing features: {missing_features}")
        
        return True
    
    def dict_to_array(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Convert dictionary to numpy array in correct feature order
        
        Args:
            data: Input data dictionary
            
        Returns:
            Numpy array with features in correct order
        """
        if self.feature_names is None:
            raise ValueError("Feature names not set")
        
        values = [data[feature] for feature in self.feature_names]
        return np.array(values).reshape(1, -1)
    
    def scale_features(self, X: np.ndarray) -> np.ndarray:
        """
        Scale features using fitted scaler
        
        Args:
            X: Input features
            
        Returns:
            Scaled features
        """
        if self.scaler is None:
            logger.warning("Scaler not set, returning unscaled features")
            return X
        
        return self.scaler.transform(X)
    
    def preprocess(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Complete preprocessing pipeline
        
        Args:
            data: Input data dictionary
            
        Returns:
            Preprocessed features ready for model prediction
        """
        # Validate input
        self.validate_input(data)
        
        # Convert to array
        X = self.dict_to_array(data)
        
        # Scale features
        X_scaled = self.scale_features(X)
        
        return X_scaled
    
    def handle_missing_values(self, data: Dict[str, Any], strategy: str = "mean") -> Dict[str, Any]:
        """
        Handle missing values in input data
        
        Args:
            data: Input data
            strategy: Strategy for handling missing values
            
        Returns:
            Data with missing values handled
        """
        for key, value in data.items():
            if value is None:
                if strategy == "mean":
                    data[key] = 0.0
                elif strategy == "zero":
                    data[key] = 0.0
                else:
                    raise ValueError(f"Unknown strategy: {strategy}")
        
        return data
    
    def validate_feature_ranges(self, data: Dict[str, Any], ranges: Dict[str, tuple]) -> bool:
        """
        Validate that features are within expected ranges
        
        Args:
            data: Input data
            ranges: Dictionary of (min, max) tuples for each feature
            
        Returns:
            True if all features are in range
        """
        for feature, (min_val, max_val) in ranges.items():
            if feature in data:
                value = data[feature]
                if not (min_val <= value <= max_val):
                    logger.warning(
                        f"Feature '{feature}' value {value} is outside range [{min_val}, {max_val}]"
                    )
        
        return True


if __name__ == "__main__":
    # Example usage
    from model.model_loader import ModelLoader
    
    loader = ModelLoader()
    scaler = loader.load_scaler()
    features = loader.load_feature_names()
    
    pipeline = PreprocessingPipeline(scaler=scaler, feature_names=features)
    
    # Example input
    sample_input = {feature: 0.5 for feature in features}
    preprocessed = pipeline.preprocess(sample_input)
    print(f"Preprocessed shape: {preprocessed.shape}")
