"""
Unit tests for API schemas
"""
import pytest
from src.api.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest


def test_prediction_request_creation():
    """Test PredictionRequest instantiation"""
    request = PredictionRequest(
        Time=0.0,
        V1=-1.36,
        V2=-0.07,
        V3=2.54,
        V4=4.41,
        V5=-0.05,
        V6=-0.10,
        V7=0.64,
        V8=0.46,
        V9=-0.05,
        V10=-0.03,
        V11=-2.24,
        V12=-0.65,
        V13=-0.42,
        V14=-0.38,
        V15=1.16,
        V16=-0.17,
        V17=-0.37,
        V18=0.20,
        V19=0.01,
        V20=-0.44,
        V21=-0.01,
        V22=-0.23,
        V23=0.10,
        V24=-0.46,
        V25=-0.12,
        V26=-0.51,
        V27=-0.07,
        V28=0.01,
        Amount=149.62,
        amount_zscore=0.0,
        amount_log=5.0,
        v1_v2_ratio=18.32,
        high_value=0.0,
        variance_all=0.5,
        max_abs_v=4.4,
        mean_abs_v=0.6
    )
    assert request.Time == 0.0
    assert request.Amount == 149.62


def test_prediction_response_creation():
    """Test PredictionResponse instantiation"""
    response = PredictionResponse(
        fraud=0,
        hybrid_score=0.001,
        threshold_used=0.01
    )
    assert response.fraud == 0
    assert response.hybrid_score == 0.001


def test_batch_prediction_request():
    """Test BatchPredictionRequest with multiple samples"""
    sample1 = PredictionRequest(
        Time=0.0,
        V1=-1.36,
        V2=-0.07,
        V3=2.54,
        V4=4.41,
        V5=-0.05,
        V6=-0.10,
        V7=0.64,
        V8=0.46,
        V9=-0.05,
        V10=-0.03,
        V11=-2.24,
        V12=-0.65,
        V13=-0.42,
        V14=-0.38,
        V15=1.16,
        V16=-0.17,
        V17=-0.37,
        V18=0.20,
        V19=0.01,
        V20=-0.44,
        V21=-0.01,
        V22=-0.23,
        V23=0.10,
        V24=-0.46,
        V25=-0.12,
        V26=-0.51,
        V27=-0.07,
        V28=0.01,
        Amount=149.62,
        amount_zscore=0.0,
        amount_log=5.0,
        v1_v2_ratio=18.32,
        high_value=0.0,
        variance_all=0.5,
        max_abs_v=4.4,
        mean_abs_v=0.6
    )
    
    batch = BatchPredictionRequest(samples=[sample1])
    assert len(batch.samples) == 1
    assert batch.samples[0].Amount == 149.62
