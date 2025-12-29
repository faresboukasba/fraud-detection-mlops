"""
__init__.py - Package initialization
"""

__version__ = "1.0.0"
__author__ = "Fraud Detection Team"

from src.data.download_data import DataPipeline
from src.data.clean_transform import FeatureEngineer
from src.data.data_pipeline import DataProcessor
from src.model.train import ModelTrainer, IsolationForestModel, XGBoostModel
from src.model.ensemble_predictor import EnsemblePredictor
from src.model.model_loader import ModelLoader

__all__ = [
    'DataPipeline',
    'FeatureEngineer',
    'DataProcessor',
    'ModelTrainer',
    'IsolationForestModel',
    'XGBoostModel',
    'EnsemblePredictor',
    'ModelLoader'
]
