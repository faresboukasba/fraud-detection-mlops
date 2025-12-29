#!/usr/bin/env python3
"""
Complete Training & Inference Pipeline
Demonstrates the full workflow from data to predictions
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.data_pipeline import DataProcessor
from src.model.train import ModelTrainer
from src.model.ensemble_predictor import EnsemblePredictor
from src.model.model_loader import ModelLoader
import numpy as np
import joblib


def main():
    """Execute complete pipeline"""
    
    print("\n" + "="*70)
    print(" "*15 + "🚀 FRAUD DETECTION COMPLETE PIPELINE")
    print("="*70)
    
    # Step 1: Data Processing
    print("\n📊 STEP 1: Data Processing")
    print("-" * 70)
    processor = DataProcessor()
    data = processor.run()
    
    # Step 2: Model Training
    print("\n\n🔧 STEP 2: Model Training")
    print("-" * 70)
    trainer = ModelTrainer()
    models = trainer.train_both_models(
        data['X_train_scaled'],
        data['y_train']
    )
    
    # Step 3: Generate Predictions
    print("\n\n🔮 STEP 3: Generate Ensemble Predictions")
    print("-" * 70)
    iso_scores = models['iso_forest'].score_samples(data['X_test_scaled'])
    xgb_proba = models['xgb_model'].predict_proba(data['X_test_scaled'])[:, 1]
    
    ensemble = EnsemblePredictor()
    hybrid_proba = ensemble.combine_predictions(iso_scores, xgb_proba)
    
    print(f"\n✓ Hybrid predictions generated")
    print(f"  Score range: [{hybrid_proba.min():.4f}, {hybrid_proba.max():.4f}]")
    print(f"  Mean score: {hybrid_proba.mean():.4f}")
    
    # Step 4: Threshold Optimization
    print("\n\n⚙️  STEP 4: Threshold Optimization")
    print("-" * 70)
    best_threshold, metrics = ensemble.optimize_threshold(
        hybrid_proba,
        data['y_test']
    )
    
    # Step 5: Save Models
    print("\n\n💾 STEP 5: Save Models")
    print("-" * 70)
    
    models_dir = Path('models')
    models_dir.mkdir(exist_ok=True)
    
    joblib.dump(models['iso_forest'].model, models_dir / 'isolation_forest.joblib')
    joblib.dump(models['xgb_model'].pipeline, models_dir / 'xgboost.joblib')
    joblib.dump(data['scaler'], models_dir / 'scaler.joblib')
    
    config = {
        'iso_weight': ensemble.iso_weight,
        'xgb_weight': ensemble.xgb_weight,
        'threshold': best_threshold,
        'f1_score': metrics['f1'],
        'precision': metrics['precision'],
        'recall': metrics['recall'],
        'metrics': metrics
    }
    joblib.dump(config, models_dir / 'model_config.joblib')
    
    print(f"✓ Models saved to {models_dir}/")
    print(f"  - isolation_forest.joblib")
    print(f"  - xgboost.joblib")
    print(f"  - scaler.joblib")
    print(f"  - model_config.joblib")
    
    # Step 6: Load and Test
    print("\n\n🧪 STEP 6: Load & Test Models")
    print("-" * 70)
    
    loader = ModelLoader()
    loaded_models = loader.load_all()
    
    # Test on first 5 samples
    print(f"\n✓ Models loaded successfully!")
    print(f"\nTest predictions on first 5 samples:")
    
    X_test_sample = data['X_test_scaled'][:5]
    iso_test = loader.iso_forest.score_samples(X_test_sample)
    xgb_test = loader.xgb.predict_proba(X_test_sample)[:, 1]
    
    test_ensemble = EnsemblePredictor(
        iso_weight=loaded_models['config']['iso_weight'],
        xgb_weight=loaded_models['config']['xgb_weight'],
        threshold=loaded_models['config']['threshold']
    )
    
    test_hybrid = test_ensemble.combine_predictions(iso_test, xgb_test)
    test_pred = test_ensemble.predict(test_hybrid)
    
    print(f"\n  Sample | Hybrid Score | Prediction | Actual")
    print(f"  {'-'*55}")
    for i in range(5):
        pred_label = "Fraud  " if test_pred[i] == 1 else "Normal "
        actual_label = "Fraud  " if data['y_test'].iloc[i] == 1 else "Normal "
        print(f"    {i+1}    | {test_hybrid[i]:12.4f} | {pred_label} | {actual_label}")
    
    # Step 7: Summary
    print("\n\n" + "="*70)
    print(" "*20 + "✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    print(f"\n📊 SUMMARY:")
    print(f"  Training samples: {data['X_train_scaled'].shape[0]:,}")
    print(f"  Test samples: {data['X_test_scaled'].shape[0]:,}")
    print(f"  Features: {data['X_train_scaled'].shape[1]}")
    print(f"\n🎯 MODEL CONFIGURATION:")
    print(f"  Isolation Forest weight: {ensemble.iso_weight:.0%}")
    print(f"  XGBoost weight: {ensemble.xgb_weight:.0%}")
    print(f"  Decision threshold: {best_threshold:.3f}")
    print(f"\n📈 METRICS:")
    print(f"  F1-Score: {metrics['f1']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    
    print(f"\n📁 NEXT STEPS:")
    print(f"  1. Start API: python -m uvicorn src.api.main:app --reload")
    print(f"  2. Build Docker: docker build -t fraud-detection:latest .")
    print(f"  3. Run Container: docker run -p 8000:8000 fraud-detection:latest")
    print(f"  4. Test Endpoint: curl http://localhost:8000/health")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
