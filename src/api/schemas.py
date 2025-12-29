"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class PredictionRequest(BaseModel):
    """Schema for fraud prediction request"""
    
    # Example features - adjust based on your actual features
    feature_1: float = Field(..., description="Feature 1 value")
    feature_2: float = Field(..., description="Feature 2 value")
    feature_3: float = Field(..., description="Feature 3 value")
    # Add all features from your model
    
    class Config:
        example = {
            "feature_1": 0.5,
            "feature_2": 0.3,
            "feature_3": 0.8,
        }


class PredictionResponse(BaseModel):
    """Schema for fraud prediction response"""
    
    prediction: int = Field(..., description="Predicted class (0: legitimate, 1: fraud)")
    probability: float = Field(..., description="Probability of fraud")
    confidence: float = Field(..., description="Model confidence")
    
    class Config:
        example = {
            "prediction": 1,
            "probability": 0.92,
            "confidence": 0.95
        }


class HealthResponse(BaseModel):
    """Schema for health check response"""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    models_loaded: List[str] = Field(..., description="List of loaded models")


class BatchPredictionRequest(BaseModel):
    """Schema for batch fraud prediction request"""
    
    samples: List[PredictionRequest] = Field(..., description="List of samples to predict")


class BatchPredictionResponse(BaseModel):
    """Schema for batch fraud prediction response"""
    
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    total_samples: int = Field(..., description="Total samples processed")
    execution_time_ms: float = Field(..., description="Execution time in milliseconds")


if __name__ == "__main__":
    # Example usage
    request = PredictionRequest(feature_1=0.5, feature_2=0.3, feature_3=0.8)
    print(request.model_dump_json(indent=2))
