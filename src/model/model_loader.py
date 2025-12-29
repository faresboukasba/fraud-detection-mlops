"""
Model loading and management utilities
"""
import logging
import joblib
import json
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ModelLoader:
    """Load and manage trained models"""
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize model loader
        
        Args:
            models_dir: Directory containing model artifacts
        """
        self.models_dir = models_dir
        self.models = {}
        self.scaler = None
        self.feature_names = None
    
    def load_scaler(self) -> Any:
        """
        Load preprocessing scaler
        
        Returns:
            Fitted StandardScaler
        """
        scaler_path = Path(self.models_dir) / "scaler.joblib"
        
        if not scaler_path.exists():
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")
        
        self.scaler = joblib.load(scaler_path)
        logger.info(f"Scaler loaded from {scaler_path}")
        return self.scaler
    
    def load_model(self, model_name: str) -> Any:
        """
        Load a specific model
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Loaded model
        """
        model_path = Path(self.models_dir) / f"{model_name}.joblib"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        model = joblib.load(model_path)
        self.models[model_name] = model
        logger.info(f"Model '{model_name}' loaded from {model_path}")
        return model
    
    def load_all_models(self) -> Dict[str, Any]:
        """
        Load all available models
        
        Returns:
            Dictionary of loaded models
        """
        models_dir_path = Path(self.models_dir)
        
        if not models_dir_path.exists():
            raise FileNotFoundError(f"Models directory not found at {self.models_dir}")
        
        for model_file in models_dir_path.glob("*.joblib"):
            if model_file.name != "scaler.joblib":
                model_name = model_file.stem
                self.load_model(model_name)
        
        logger.info(f"Loaded {len(self.models)} models")
        return self.models
    
    def load_feature_names(self) -> list:
        """
        Load feature order
        
        Returns:
            List of feature names
        """
        features_path = Path(self.models_dir) / "features_order.json"
        
        if not features_path.exists():
            raise FileNotFoundError(f"Features file not found at {features_path}")
        
        with open(features_path, "r") as f:
            self.feature_names = json.load(f)
        
        logger.info(f"Loaded {len(self.feature_names)} features")
        return self.feature_names
    
    def load_metrics(self) -> Dict[str, Any]:
        """
        Load training metrics
        
        Returns:
            Dictionary of training metrics
        """
        metrics_path = Path(self.models_dir) / "training_metrics.json"
        
        if not metrics_path.exists():
            raise FileNotFoundError(f"Metrics file not found at {metrics_path}")
        
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        
        logger.info("Metrics loaded")
        return metrics


if __name__ == "__main__":
    loader = ModelLoader()
    loader.load_scaler()
    loader.load_all_models()
    loader.load_feature_names()
    print("All models loaded successfully!")
