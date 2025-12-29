# Integration Guide: Notebook → Production

This document explains how the Jupyter notebook (`fraud_detection_optimized_final.ipynb`) integrates with the modularized production code in `src/`.

## 🔄 Workflow Mapping

### Notebook Section → Production Module

| Notebook Section | Module | Purpose |
|---|---|---|
| **2. Data Loading** | `src/data/download_data.py` | Dataset downloading from Kaggle |
| **3. Feature Engineering** | `src/data/clean_transform.py` | Feature creation & scaling |
| **2+3 Combined** | `src/data/data_pipeline.py` | Complete orchestration |
| **5. Isolation Forest** | `src/model/train.py` | IF model training |
| **6. XGBoost** | `src/model/train.py` | XGB model training |
| **7. Ensemble Voting** | `src/model/ensemble_predictor.py` | Weighted voting & threshold optimization |
| **8. Threshold Optimization** | `src/model/ensemble_predictor.py` | F1-based threshold finding |
| **11. Model Saving** | `src/model/model_loader.py` | Model persistence |
| **12. Production Usage** | `src/api/main.py` | FastAPI serving |

## 📊 Data Flow

```
Notebook Development
        ↓
    ↓ Extract code cells
        ↓
Production Modules
        ↓
    ├─ src/data/     (Data pipeline)
    ├─ src/model/    (Training & inference)
    ├─ src/api/      (API serving)
    └─ src/utils/    (Utilities)
        ↓
    FastAPI Application
        ↓
    Docker Container
        ↓
    Cloud Deployment (AWS/Azure/GCP)
```

## 🛠️ Using Production Code from Notebook

### Step 1: Load Data (replaces Notebook Section 2)
```python
from src.data.download_data import DataPipeline

pipeline = DataPipeline()
data = pipeline.run()
# Returns: X_train, X_test, y_train, y_test
```

### Step 2: Feature Engineering (replaces Notebook Section 3)
```python
from src.data.clean_transform import FeatureEngineer

engineer = FeatureEngineer()
X_train_scaled, X_test_scaled = engineer.process_pipeline(
    data['X_train'], 
    data['X_test']
)
```

### Step 3: Complete Pipeline (replaces Notebook Sections 2+3)
```python
from src.data.data_pipeline import DataProcessor

processor = DataProcessor()
data = processor.run()  # One call for everything
```

### Step 4: Train Models (replaces Notebook Sections 5+6)
```python
from src.model.train import ModelTrainer

trainer = ModelTrainer()
models = trainer.train_both_models(
    data['X_train_scaled'],
    data['y_train']
)
```

### Step 5: Create Ensemble (replaces Notebook Section 7)
```python
from src.model.ensemble_predictor import EnsemblePredictor

ensemble = EnsemblePredictor()
iso_scores = models['iso_forest'].score_samples(data['X_test_scaled'])
xgb_proba = models['xgb_model'].predict_proba(data['X_test_scaled'])[:, 1]

hybrid_proba = ensemble.combine_predictions(iso_scores, xgb_proba)
best_threshold, metrics = ensemble.optimize_threshold(hybrid_proba, data['y_train'])
```

### Step 6: Save Models (replaces Notebook Section 11)
```python
import joblib

joblib.dump(trainer.iso_forest.model, 'models/isolation_forest.joblib')
joblib.dump(trainer.xgb_model.pipeline, 'models/xgboost.joblib')
joblib.dump(data['scaler'], 'models/scaler.joblib')
```

## 🚀 Running from API (replaces Notebook Section 12)

Instead of running code in notebook, use the FastAPI:

```bash
python -m uvicorn src.api.main:app --reload
```

Then make requests:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"transaction": {...}}'
```

## 📝 Notebook Development → Production Checklist

- [ ] **Exploration**: Use notebook for EDA and experimentation
- [ ] **Extract**: Move successful code to `src/` modules
- [ ] **Test**: Verify modules work in isolation
- [ ] **Integrate**: Use `DataProcessor`, `ModelTrainer`, `EnsemblePredictor`
- [ ] **Validate**: Run tests with different data scenarios
- [ ] **Package**: Create Docker image
- [ ] **Deploy**: Push to cloud provider

## 🔗 Example: Full Pipeline in Production Code

```python
# Complete ML pipeline using modularized code
from src.data.data_pipeline import DataProcessor
from src.model.train import ModelTrainer
from src.model.ensemble_predictor import EnsemblePredictor
from src.model.model_loader import ModelLoader
import joblib

# Step 1: Process data
processor = DataProcessor()
data = processor.run()

# Step 2: Train models
trainer = ModelTrainer()
models = trainer.train_both_models(
    data['X_train_scaled'],
    data['y_train']
)

# Step 3: Create ensemble
ensemble = EnsemblePredictor()
iso_scores = models['iso_forest'].score_samples(data['X_test_scaled'])
xgb_proba = models['xgb_model'].predict_proba(data['X_test_scaled'])[:, 1]
hybrid_proba = ensemble.combine_predictions(iso_scores, xgb_proba)
threshold, metrics = ensemble.optimize_threshold(hybrid_proba, data['y_train'])

# Step 4: Evaluate on test set
y_pred = ensemble.predict(hybrid_proba)

# Step 5: Save everything
joblib.dump(trainer.iso_forest.model, 'models/isolation_forest.joblib')
joblib.dump(trainer.xgb_model.pipeline, 'models/xgboost.joblib')
joblib.dump(data['scaler'], 'models/scaler.joblib')
joblib.dump(ensemble.get_config(), 'models/model_config.json')

print("✅ Full pipeline completed!")
```

## 🌐 From Local to API

Once models are saved, the API can serve predictions:

```python
# In src/api/main.py (automatic)
1. Load models from disk
2. Validate incoming requests
3. Preprocess features
4. Get ensemble predictions
5. Return results
```

## 📦 Containerization for Deployment

```bash
# Build image with all code
docker build -t fraud-detection:latest .

# Run container (API starts automatically)
docker run -p 8000:8000 fraud-detection:latest

# Test
curl http://localhost:8000/health
```

## 🎓 Summary

- **Notebook** = Development & exploration
- **src/** = Production-ready modular code
- **API** = Service layer for predictions
- **Docker** = Deployment container
- **Cloud** = Scalable inference

The notebook contains all the logic; we've just reorganized it into reusable, testable modules for production use! 🚀
