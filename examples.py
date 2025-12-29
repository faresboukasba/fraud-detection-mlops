"""
Example: Making predictions with the trained model
Demonstrates how to use the fraud detection system
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.model.model_loader import ModelLoader
from src.model.ensemble_predictor import EnsemblePredictor
import numpy as np


def example_single_prediction():
    """Make a single fraud prediction"""
    
    print("\n" + "="*70)
    print("Example 1: Single Transaction Prediction")
    print("="*70)
    
    # Load models
    loader = ModelLoader()
    try:
        models = loader.load_all()
    except FileNotFoundError:
        print("❌ Models not found. Please run train_pipeline.py first!")
        return
    
    # Create ensemble
    config = models['config']
    ensemble = EnsemblePredictor(
        iso_weight=config['iso_weight'],
        xgb_weight=config['xgb_weight'],
        threshold=config['threshold']
    )
    
    # Example transaction features
    # In real use, these would come from a database or API request
    sample_features = {
        'V1': -1.3598, 'V2': -0.0728, 'V3': 2.3606,
        'V4': 1.3417, 'V5': -0.3446, 'V6': 0.4637,
        'V7': -0.3831, 'V8': 0.8735, 'V9': 0.5699,
        'V10': -0.6450, 'V11': -0.4264, 'V12': -0.9155,
        'V13': -0.3810, 'V14': 1.3499, 'V15': -0.5717,
        'V16': -0.3640, 'V17': -0.7798, 'V18': 0.2710,
        'V19': -0.5514, 'V20': -0.0191, 'V21': 0.0479,
        'V22': 0.7837, 'V23': 0.2500, 'V24': -0.0142,
        'V25': 0.0489, 'V26': 0.0485, 'V27': -0.0220,
        'V28': 0.0228, 'Amount': 149.62, 'Time': 0.0
    }
    
    # Prepare features
    feature_values = np.array([list(sample_features.values())])
    X_scaled = models['scaler'].transform(feature_values)
    
    # Get predictions
    iso_score = models['iso_forest'].score_samples(X_scaled)[0]
    xgb_proba = models['xgb'].predict_proba(X_scaled)[0, 1]
    
    # Combine with ensemble
    iso_norm = 1 - (iso_score - iso_score) if iso_score == iso_score else 0.5
    hybrid_score = ensemble.iso_weight * iso_norm + ensemble.xgb_weight * xgb_proba
    
    is_fraud = ensemble.predict(np.array([hybrid_score]))[0]
    
    # Display results
    print(f"\n💳 Transaction Details:")
    print(f"   Amount: ${sample_features['Amount']:.2f}")
    print(f"   Time: {sample_features['Time']:.0f} seconds")
    
    print(f"\n🔮 Prediction Results:")
    print(f"   Hybrid Score: {hybrid_score:.4f}")
    print(f"   Threshold: {ensemble.threshold:.3f}")
    print(f"   Is Fraud: {'❌ YES - FRAUD DETECTED' if is_fraud == 1 else '✅ NO - Normal transaction'}")
    print(f"   Confidence: {max(hybrid_score, 1-hybrid_score):.2%}")


def example_batch_predictions():
    """Make batch predictions on multiple transactions"""
    
    print("\n\n" + "="*70)
    print("Example 2: Batch Predictions")
    print("="*70)
    
    # Load models
    loader = ModelLoader()
    try:
        models = loader.load_all()
    except FileNotFoundError:
        print("❌ Models not found. Please run train_pipeline.py first!")
        return
    
    config = models['config']
    ensemble = EnsemblePredictor(
        iso_weight=config['iso_weight'],
        xgb_weight=config['xgb_weight'],
        threshold=config['threshold']
    )
    
    # Multiple transactions
    transactions = [
        {
            'name': 'Normal Transaction',
            'amount': 50.0,
            'features': {
                'V1': 0.1, 'V2': 0.2, 'V3': 0.3, 'V4': 0.1,
                'V5': -0.1, 'V6': 0.2, 'V7': -0.1, 'V8': 0.3,
                'V9': 0.2, 'V10': -0.2, 'V11': -0.1, 'V12': -0.1,
                'V13': -0.1, 'V14': 0.1, 'V15': -0.2, 'V16': -0.1,
                'V17': -0.2, 'V18': 0.1, 'V19': -0.2, 'V20': 0.0,
                'V21': 0.0, 'V22': 0.2, 'V23': 0.1, 'V24': 0.0,
                'V25': 0.0, 'V26': 0.0, 'V27': 0.0, 'V28': 0.0,
                'Amount': 50.0, 'Time': 1000.0
            }
        },
        {
            'name': 'Suspicious Transaction',
            'amount': 2000.0,
            'features': {
                'V1': -5.0, 'V2': 2.0, 'V3': 4.0, 'V4': 3.0,
                'V5': -3.0, 'V6': 2.0, 'V7': -2.0, 'V8': 3.0,
                'V9': 2.0, 'V10': -2.0, 'V11': -2.0, 'V12': -3.0,
                'V13': -2.0, 'V14': 2.0, 'V15': -2.0, 'V16': -1.0,
                'V17': -3.0, 'V18': 1.0, 'V19': -2.0, 'V20': 0.0,
                'V21': 0.0, 'V22': 2.0, 'V23': 1.0, 'V24': 0.0,
                'V25': 0.0, 'V26': 0.0, 'V27': 0.0, 'V28': 0.0,
                'Amount': 2000.0, 'Time': 5000.0
            }
        },
    ]
    
    print(f"\n📊 Processing {len(transactions)} transactions...\n")
    
    for i, txn in enumerate(transactions, 1):
        features = np.array([list(txn['features'].values())])
        X_scaled = models['scaler'].transform(features)
        
        iso_score = models['iso_forest'].score_samples(X_scaled)[0]
        xgb_proba = models['xgb'].predict_proba(X_scaled)[0, 1]
        
        iso_norm = 1 - (iso_score - iso_score) if iso_score == iso_score else 0.5
        hybrid_score = ensemble.iso_weight * iso_norm + ensemble.xgb_weight * xgb_proba
        is_fraud = ensemble.predict(np.array([hybrid_score]))[0]
        
        fraud_label = "🚨 FRAUD" if is_fraud == 1 else "✅ NORMAL"
        
        print(f"Transaction {i}: {txn['name']}")
        print(f"  Amount: ${txn['amount']:.2f}")
        print(f"  Hybrid Score: {hybrid_score:.4f}")
        print(f"  Result: {fraud_label}")
        print()


def example_model_info():
    """Display model information"""
    
    print("\n" + "="*70)
    print("Example 3: Model Information")
    print("="*70)
    
    # Load models
    loader = ModelLoader()
    try:
        models = loader.load_all()
    except FileNotFoundError:
        print("❌ Models not found. Please run train_pipeline.py first!")
        return
    
    config = models['config']
    
    print(f"\n📊 Model Configuration:")
    print(f"  Isolation Forest weight: {config['iso_weight']:.0%}")
    print(f"  XGBoost weight: {config['xgb_weight']:.0%}")
    print(f"  Decision threshold: {config['threshold']:.3f}")
    
    print(f"\n📈 Performance Metrics:")
    print(f"  F1-Score: {config['f1_score']:.4f}")
    print(f"  Precision: {config['precision']:.4f}")
    print(f"  Recall: {config['recall']:.4f}")
    
    print(f"\n🔧 Model Details:")
    print(f"  Scaler type: StandardScaler")
    print(f"  Isolation Forest estimators: 150")
    print(f"  XGBoost estimators: 300")
    print(f"  Total features: 30+7 engineered = 37")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎯 FRAUD DETECTION - PREDICTION EXAMPLES")
    print("="*70)
    
    try:
        # Run all examples
        example_single_prediction()
        example_batch_predictions()
        example_model_info()
        
        print("\n" + "="*70)
        print("✅ Examples completed successfully!")
        print("="*70)
        print("\n💡 For API-based predictions, start the server:")
        print("   python start_api.py")
        print("")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
