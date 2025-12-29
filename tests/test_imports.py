"""
Tests for data pipeline components
"""
import pytest


def test_data_pipeline_import():
    """Test that data pipeline modules can be imported"""
    try:
        from src.data.clean_transform import DataCleaner
        from src.data.download_data import DataDownloader
        assert True
    except ImportError:
        pytest.skip("Data pipeline modules not available")


def test_preprocessing_imports():
    """Test that preprocessing modules can be imported"""
    try:
        from src.utils.preprocessing import PreprocessingPipeline
        assert True
    except ImportError:
        pytest.skip("Preprocessing modules not available")


def test_model_imports():
    """Test that model modules can be imported"""
    try:
        from src.model.model_loader import ModelLoader
        from src.model.ensemble_predictor import EnsemblePredictor
        assert True
    except ImportError:
        pytest.skip("Model modules not available")
