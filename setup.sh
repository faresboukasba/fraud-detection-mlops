#!/bin/bash

# Quick Setup & Run Script for Fraud Detection MLOps

set -e

echo "=================================================="
echo "🚀 Fraud Detection MLOps - Quick Setup"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip setuptools wheel -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create models directory
echo ""
echo "📁 Creating models directory..."
mkdir -p models
echo "✓ Models directory ready"

# Show next steps
echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1️⃣  Train models (if needed):"
echo "   python train_pipeline.py"
echo ""
echo "2️⃣  Start API:"
echo "   python start_api.py"
echo ""
echo "3️⃣  Or use uvicorn directly:"
echo "   uvicorn src.api.main:app --reload"
echo ""
echo "4️⃣  Open in browser:"
echo "   http://localhost:8000/docs"
echo ""
echo "5️⃣  Build Docker image:"
echo "   docker build -t fraud-detection:latest ."
echo ""
echo "=================================================="
