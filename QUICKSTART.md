# Quick Start Guide

Get up and running in 5 minutes!

## 1. Setup (One-time)

```bash
cd /Users/arpitkhandelwal/.gemini/antigravity/scratch/ai-voice-detection-api

# Run automated setup
chmod +x setup.sh
./setup.sh
```

OR manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and set your API_KEY
```

## 2. Train Model

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Train the CNN model (~5-10 minutes)
python src/ml/train.py
```

Expected output:
```
Generating 1000 synthetic voice samples...
Training for 50 epochs...
Epoch [50/50]
  Train Loss: 0.0234, Train Acc: 99.20%
  Val Loss: 0.0456, Val Acc: 98.50%
Training Complete! Best Val Loss: 0.0456
Model saved to: models/voice_classifier.pth
```

## 3. Verify Installation

```bash
python verify.py
```

All checks should pass ✅

## 4. Start API Server

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Server will start at: http://localhost:8000

## 5. Test the API

### Option A: Interactive Docs

Visit: http://localhost:8000/docs

1. Click "Authorize" and enter your API key
2. Try the `/api/voice-detection` endpoint
3. Paste a base64 encoded MP3 audio

### Option B: curl Command

```bash
# First, encode an MP3 file to base64
AUDIO_BASE64=$(base64 -i your_audio.mp3 | tr -d '\n')

# Make API request
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d "{
    \"language\": \"English\",
    \"audioFormat\": \"mp3\",
    \"audioBase64\": \"$AUDIO_BASE64\"
  }"
```

### Option C: Run Tests

```bash
# Make sure server is running first!
python tests/test_api.py
```

## 6. Deploy (Optional)

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment to:
- Render (recommended)
- Railway
- AWS EC2
- Docker

---

## Troubleshooting

### "Model not found" error
```bash
python src/ml/train.py
```

### "Could not connect to API"
```bash
# Make sure server is running
uvicorn src.api.main:app --port 8000
```

### "Invalid API key"
```bash
# Check your .env file
cat .env
# Make sure API_KEY matches the header value
```

---

**That's it! You're ready to detect AI voices! 🎯**
