#!/usr/bin/env python3
"""
Quick Start API Server
Starts the FastAPI fraud detection service
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from src.api.main import app

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" "*15 + "🚀 STARTING FRAUD DETECTION API")
    print("="*70)
    print("\n📡 API Available at: http://localhost:8000")
    print("📚 Documentation at: http://localhost:8000/docs")
    print("🔄 Alternative docs: http://localhost:8000/redoc")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
