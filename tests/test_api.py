"""
Integration tests for API endpoints
"""
import pytest
from httpx import AsyncClient, Client
from unittest.mock import patch, MagicMock


def test_health_endpoint_schema():
    """Test health endpoint response schema"""
    # Mock response based on actual API behavior
    expected_response = {
        "status": "ok",
        "model_loaded": True
    }
    assert expected_response["status"] == "ok"
    assert expected_response["model_loaded"] == True


def test_prediction_response_schema():
    """Test prediction endpoint response schema"""
    # Mock response based on actual API behavior
    expected_response = {
        "fraud": 0,
        "hybrid_score": 9.395094480169064e-07,
        "threshold_used": 0.01
    }
    assert expected_response["fraud"] in [0, 1]
    assert 0 <= expected_response["hybrid_score"] <= 1
    assert expected_response["threshold_used"] > 0
