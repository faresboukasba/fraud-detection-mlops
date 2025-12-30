# Fraud Detection MLOps Project

A production-ready machine learning project for fraud detection with API deployment capabilities.

pour tester l'api suivez le fichier suivant : TESTER_API_TERMINAL.md
## Project Structure

```
project-root/
├─ src/
│  ├─ data/
│  │  ├─ download_data.py      # Data download utilities
│  │  ├─ clean_transform.py    # Data cleaning & transformation
│  │  └─ data_pipeline.py      # Complete data pipeline
│  ├─ model/
│  │  ├─ train.py              # Model training
│  │  ├─ ensemble_predictor.py # Ensemble predictions
│  │  └─ model_loader.py       # Model loading utilities
│  ├─ api/
│  │  ├─ main.py               # FastAPI application
│  │  ├─ schemas.py            # Pydantic schemas
│  │  └─ model_loader.py       # API model loading
│  └─ utils/
│     └─ preprocessing.py       # Preprocessing for API
├─ models/                      # Model artifacts (scaler, models, features)
├─ data/
│  ├─ raw/                      # Raw data
│  └─ processed/                # Processed data
├─ Dockerfile                   # Docker containerization
├─ requirements.txt             # Python dependencies
├─ .github/workflows/
│  ├─ test-aws.yml             # AWS testing workflow
│  └─ ci-cd.yml                # CI/CD pipeline
└─ README.md                    # This file

## Installation

### Prerequisites
- Python 3.11+
- pip or conda
- Docker (for containerization)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd fraud-detection-mlops
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Training Models

```python
from src.data.data_pipeline import DataPipeline
from src.model.train import ModelTrainer

# Run data pipeline
pipeline = DataPipeline()
processed_data = pipeline.run()

# Train models
trainer = ModelTrainer()
trainer.load_data(processed_data)
trainer.train_random_forest()
trainer.train_gradient_boosting()
trainer.save_artifacts()
```

### Running the API

```bash
# Development
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Production
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Endpoints

- **GET /health** - Health check
- **POST /predict** - Single prediction
- **POST /predict_batch** - Batch predictions
- **GET /metrics** - Training metrics
- **GET /features** - Required features

### Example Prediction Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_1": 0.5,
    "feature_2": 0.3,
    "feature_3": 0.8
  }'
```

## Docker

### Build Docker Image

```bash
docker build -t fraud-detection:latest .
```

### Run Container

```bash
docker run -p 8000:8000 fraud-detection:latest
```

### Push to Docker Registry

```bash
docker tag fraud-detection:latest <registry>/fraud-detection:latest
docker push <registry>/fraud-detection:latest
```

## Deployment

### AWS Deployment

The project includes GitHub Actions workflows for automated testing and deployment:

- **test-aws.yml** - Runs tests on AWS infrastructure
- **ci-cd.yml** - CI/CD pipeline for deployment

### Environment Variables

Create a `.env` file with:

```env
AWS_REGION= eu-west-3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
ECR_REGISTRY=your-registry
```

## Model Artifacts

The `models/` directory contains:

- `scaler.joblib` - Fitted StandardScaler for feature normalization
- `random_forest.joblib` - Trained Random Forest model
- `gradient_boosting.joblib` - Trained Gradient Boosting model
- `features_order.json` - Feature names in order
- `training_metrics.json` - Training metrics and performance

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Code Quality

```bash
# Format code
black src/

# Lint code
pylint src/

# Type checking
mypy src/
```



## Contributing

1. Create a feature branch
2. Make changes and run tests
3. Submit a pull request



