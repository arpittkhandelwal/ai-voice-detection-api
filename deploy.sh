#!/bin/bash

# Quick deployment script for hackathon submission

echo "=========================================="
echo "AI Voice Detection API - Deploy Script"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - AI Voice Detection API for Hackathon"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

echo ""
echo "=========================================="
echo "Next Steps for Deployment:"
echo "=========================================="
echo ""
echo "1️⃣  Create GitHub Repository"
echo "   - Go to: https://github.com/new"
echo "   - Name: ai-voice-detection-api"
echo "   - Create repository (don't initialize with README)"
echo ""
echo "2️⃣  Push to GitHub"
echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection-api.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Deploy to Render"
echo "   - Go to: https://render.com"
echo "   - New Web Service → Connect your GitHub repo"
echo "   - Build Command: pip install -r requirements.txt && python src/ml/train.py"
echo "   - Start Command: uvicorn src.api.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "4️⃣  Set Environment Variables in Render"
echo "   API_KEY=HACKATHON_API_KEY_JXFgVg0p7kOIEI2Uw6EfR_hYSsPysiXTZFjJ6mkHJXg"
echo "   MODEL_PATH=models/voice_classifier.pth"
echo ""
echo "5️⃣  Get Your Deployed URL"
echo "   Render will provide: https://ai-voice-detection-api-xxxx.onrender.com"
echo ""
echo "=========================================="
echo "📋 For Submission Form:"
echo "=========================================="
echo ""
echo "API Key: HACKATHON_API_KEY_JXFgVg0p7kOIEI2Uw6EfR_hYSsPysiXTZFjJ6mkHJXg"
echo ""
echo "Deployed URL: (Get from Render after deployment)"
echo ""
echo "=========================================="
