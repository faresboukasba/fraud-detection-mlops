"""
FastAPI application for fraud detection model serving
"""
import logging
import time
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    HealthResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
)
from model.model_loader import ModelLoader
from model.ensemble_predictor import EnsemblePredictor
from utils.preprocessing import PreprocessingPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for models
model_loader: ModelLoader = None
ensemble_predictor: EnsemblePredictor = None
preprocessing_pipeline: PreprocessingPipeline = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for app startup/shutdown
    """
    global model_loader, ensemble_predictor, preprocessing_pipeline
    
    # Startup
    logger.info("Initializing models...")
    try:
        # Load models
        model_loader = ModelLoader(models_dir="models")
        model_loader.load_scaler()
        model_loader.load_all_models()
        model_loader.load_feature_names()
        
        # Initialize ensemble predictor
        ensemble_predictor = EnsemblePredictor(model_loader.models)
        
        # Initialize preprocessing pipeline
        preprocessing_pipeline = PreprocessingPipeline(
            scaler=model_loader.scaler,
            feature_names=model_loader.feature_names
        )
        
        logger.info("Models loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Fraud Detection API",
    description="API for fraud detection predictions using ensemble models",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the Fraud Detection UI
    """
    try:
        # Try to find index.html in project root
        html_path = Path(__file__).parent.parent.parent / "index.html"
        if html_path.exists():
            with open(html_path, 'r') as f:
                return f.read()
        else:
            # Fallback: return simple HTML
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fraud Detection API</title>
                <style>
                    body { font-family: Arial; margin: 50px; text-align: center; }
                    h1 { color: #FF4B4B; }
                    .endpoint { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <h1>🔍 Fraud Detection API</h1>
                <p>API is running!</p>
                <div class="endpoint">
                    <strong>GET /health</strong> - Health check
                </div>
                <div class="endpoint">
                    <strong>POST /predict</strong> - Single prediction
                </div>
                <div class="endpoint">
                    <strong>POST /predict-batch</strong> - Batch predictions
                </div>
                <div class="endpoint">
                    <strong>GET /docs</strong> - API documentation
                </div>
            </body>
            </html>
            """
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    """
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        models_loaded=list(model_loader.models.keys())
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Make a single fraud prediction
    """
    if ensemble_predictor is None:
        raise HTTPException(status_code=503, detail="Models not ready")
    
    try:
        # Preprocess input
        request_dict = request.model_dump()
        X = preprocessing_pipeline.preprocess(request_dict)
        
        # Get predictions
        prediction = ensemble_predictor.predict(X)[0]
        probability = ensemble_predictor.predict_proba(X)[0]
        
        # Calculate confidence
        confidence = max(probability, 1 - probability)
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=float(confidence)
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict_batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    """
    Make batch fraud predictions
    """
    if ensemble_predictor is None:
        raise HTTPException(status_code=503, detail="Models not ready")
    
    try:
        start_time = time.time()
        predictions = []
        
        for sample in request.samples:
            # Preprocess input
            sample_dict = sample.model_dump()
            X = preprocessing_pipeline.preprocess(sample_dict)
            
            # Get predictions
            prediction = ensemble_predictor.predict(X)[0]
            probability = ensemble_predictor.predict_proba(X)[0]
            confidence = max(probability, 1 - probability)
            
            predictions.append(
                PredictionResponse(
                    prediction=int(prediction),
                    probability=float(probability),
                    confidence=float(confidence)
                )
            )
        
        execution_time = (time.time() - start_time) * 1000
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_samples=len(predictions),
            execution_time_ms=execution_time
        )
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics")
async def get_metrics() -> dict:
    """
    Get model training metrics
    """
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        metrics = model_loader.load_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error loading metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/features")
async def get_features() -> dict:
    """
    Get list of required features
    """
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    return {
        "features": model_loader.feature_names,
        "count": len(model_loader.feature_names)
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
