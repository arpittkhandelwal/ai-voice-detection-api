#!/bin/bash

# Setup script for local development

echo "=================================="
echo "AI Voice Detection API - Setup"
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your API key."
else
    echo "✓ .env file already exists"
fi

# Train model
echo ""
echo "=================================="
echo "Model Training"
echo "=================================="
read -p "Do you want to train the model now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Training model (this may take 5-10 minutes)..."
    python src/ml/train.py
    echo "✓ Model training complete!"
else
    echo "⚠️  Skipping model training. You'll need to train the model later:"
    echo "   python src/ml/train.py"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API key"
echo "2. If you skipped training, run: python src/ml/train.py"
echo "3. Start the server: uvicorn src.api.main:app --host 0.0.0.0 --port 8000"
echo "4. Visit http://localhost:8000/docs to see API documentation"
echo ""
echo "Happy coding! 🚀"
