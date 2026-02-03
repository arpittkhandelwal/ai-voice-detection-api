# Hackathon Submission Guide

## 📝 Submission Information

### Generated API Key (Production)
```
HACKATHON_API_KEY_JXFgVg0p7kOIEI2Uw6EfR_hYSsPysiXTZFjJ6mkHJXg
```

**⚠️ IMPORTANT**: This is your production API key. Use this for deployment and submission.

---

## 🚀 Quick Deployment to Render (5 Minutes)

### Step 1: Prepare Repository

```bash
cd /Users/arpitkhandelwal/.gemini/antigravity/scratch/ai-voice-detection-api

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - AI Voice Detection API"

# Create GitHub repository and push
# (Replace with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection-api.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign up/Login**: Use GitHub account for easy integration
3. **New Web Service**: Click "New +" → "Web Service"
4. **Connect Repository**: Select your `ai-voice-detection-api` repository
5. **Configure Service**:

   ```yaml
   Name: ai-voice-detection-api
   Environment: Python 3
   Region: Oregon (US West)
   Branch: main
   Build Command: pip install -r requirements.txt && python src/ml/train.py
   Start Command: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
   ```

6. **Environment Variables**: Click "Advanced" and add:

   ```
   API_KEY=HACKATHON_API_KEY_[your_generated_key]
   MODEL_PATH=models/voice_classifier.pth
   ```

7. **Create Web Service**: Click the button and wait 5-10 minutes

### Step 3: Get Your Deployed URL

After deployment completes, Render will provide a URL like:
```
https://ai-voice-detection-api-xxxx.onrender.com
```

This is your **Deployed URL** for submission!

---

## ✅ Test Your Deployment

### Quick Test

```bash
# Replace with your actual deployed URL
DEPLOYED_URL="https://ai-voice-detection-api-xxxx.onrender.com"
API_KEY="HACKATHON_API_KEY_[your_key]"

# Test health check
curl $DEPLOYED_URL/health

# Test voice detection (you'll need a real audio file)
AUDIO_BASE64=$(base64 -i sample.mp3 | tr -d '\n')

curl -X POST $DEPLOYED_URL/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{
    \"language\": \"English\",
    \"audioFormat\": \"mp3\",
    \"audioBase64\": \"$AUDIO_BASE64\"
  }"
```

---

## 📋 Submission Form

Fill out your hackathon submission form with:

### 1. Deployed URL
```
https://ai-voice-detection-api-xxxx.onrender.com
```
*(Replace with your actual Render URL)*

### 2. API Key
```
HACKATHON_API_KEY_[your_generated_key]
```

### 3. Example Request

```bash
curl -X POST https://ai-voice-detection-api-xxxx.onrender.com/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: HACKATHON_API_KEY_[your_key]" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2..."
  }'
```

### 4. API Documentation
```
https://ai-voice-detection-api-xxxx.onrender.com/docs
```

### 5. GitHub Repository
```
https://github.com/YOUR_USERNAME/ai-voice-detection-api
```

---

## 🔥 Alternative: Deploy in 2 Minutes with Railway

If Render is slow, try Railway:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd /Users/arpitkhandelwal/.gemini/antigravity/scratch/ai-voice-detection-api
railway init
railway variables set API_KEY=HACKATHON_API_KEY_[your_key]
railway up

# Get URL
railway domain
```

---

## 📝 Hackathon Submission Checklist

- [ ] Generate secure API key
- [ ] Push code to GitHub
- [ ] Deploy to Render or Railway
- [ ] Test deployed API with health check
- [ ] Test voice detection endpoint
- [ ] Copy deployed URL
- [ ] Copy API key
- [ ] Submit form with URL and API key
- [ ] Include link to GitHub repo
- [ ] Include link to API docs (/docs endpoint)

---

## 🆘 Troubleshooting

### Deployment fails during training

If the build times out during model training, you can:

1. Pre-train the model locally:
   ```bash
   python src/ml/train.py
   git add models/voice_classifier.pth
   git commit -m "Add pre-trained model"
   git push
   ```

2. Update Render build command to:
   ```
   pip install -r requirements.txt
   ```

### First request is slow

Render free tier spins down after 15 minutes. First request after spin-down takes ~30 seconds. This is normal.

### API key not working

Make sure you set the environment variable in Render:
- Go to Render Dashboard → Your Service → Environment
- Add: `API_KEY=HACKATHON_API_KEY_[your_key]`
- Save changes and redeploy

---

## 🎯 Ready to Submit!

Your submission should include:

1. ✅ **Deployed URL**: `https://your-app.onrender.com`
2. ✅ **API Key**: `HACKATHON_API_KEY_[generated]`
3. ✅ **GitHub Repo**: `https://github.com/yourname/ai-voice-detection-api`
4. ✅ **Working API**: Tested and verified

**Good luck with your submission!** 🚀
