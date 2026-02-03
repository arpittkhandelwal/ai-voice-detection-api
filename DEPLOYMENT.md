# Deployment Guide

Complete deployment instructions for the AI Voice Detection API on various cloud platforms.

## Prerequisites

Before deploying, ensure you have:

- ✅ Trained model file (`models/voice_classifier.pth`)
- ✅ GitHub repository with your code
- ✅ Secret API key for authentication

## Option 1: Render (Recommended) ⭐

Render provides easy deployment with free tier options.

### Step-by-Step Guide

1. **Prepare Your Repository**

```bash
# Ensure all code is committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Create Render Account**

   - Go to [render.com](https://render.com)
   - Sign up or log in

3. **Create New Web Service**

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:

```yaml
Name: ai-voice-detection-api
Environment: Python 3
Region: Oregon (US West) # or closest to your target users
Branch: main
Build Command: pip install -r requirements.txt && python src/ml/train.py
Start Command: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

4. **Set Environment Variables**

   Add these in the Render dashboard under "Environment":

```
API_KEY=your-production-api-key-here
MODEL_PATH=models/voice_classifier.pth
HOST=0.0.0.0
PORT=10000
```

5. **Deploy**

   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your API will be live at: `https://your-app-name.onrender.com`

### Health Check Configuration

```
Health Check Path: /health
```

### Render Free Tier Limitations

- Spins down after 15 minutes of inactivity
- First request after spin-down may take 30 seconds
- 750 hours/month free

---

## Option 2: Railway

Railway offers simple deployment with generous free tier.

### Step-by-Step Guide

1. **Install Railway CLI**

```bash
npm install -g @railway/cli
```

2. **Login to Railway**

```bash
railway login
```

3. **Initialize Project**

```bash
cd /Users/arpitkhandelwal/.gemini/antigravity/scratch/ai-voice-detection-api
railway init
```

4. **Add Environment Variables**

```bash
railway variables set API_KEY=your-production-api-key-here
railway variables set MODEL_PATH=models/voice_classifier.pth
```

5. **Create Procfile**

Create a file named `Procfile` in the root directory:

```
web: python src/ml/train.py && uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

6. **Deploy**

```bash
railway up
```

7. **Generate Domain**

```bash
railway domain
```

Your API will be live at: `https://your-project.up.railway.app`

---

## Option 3: AWS EC2

For full control and scalability, deploy on AWS EC2.

### Step-by-Step Guide

1. **Launch EC2 Instance**

   - Go to AWS Console → EC2
   - Click "Launch Instance"
   - Choose **Ubuntu Server 22.04 LTS**
   - Instance type: **t2.medium** (minimum for ML workloads)
   - Configure security group:
     - SSH (port 22): Your IP
     - HTTP (port 80): Anywhere
     - Custom TCP (port 8000): Anywhere

2. **Connect to Instance**

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

3. **Install Dependencies**

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Install system dependencies for audio processing
sudo apt install libsndfile1 ffmpeg -y
```

4. **Clone Repository**

```bash
git clone https://github.com/your-username/ai-voice-detection-api.git
cd ai-voice-detection-api
```

5. **Setup Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure Environment**

```bash
cp .env.example .env
nano .env  # Edit with your API key
```

7. **Train Model**

```bash
python src/ml/train.py
```

8. **Install and Configure Nginx**

```bash
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/voice-api
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or use EC2 public IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/voice-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. **Setup Systemd Service**

Create a systemd service for auto-restart:

```bash
sudo nano /etc/systemd/system/voice-api.service
```

Add this configuration:

```ini
[Unit]
Description=AI Voice Detection API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-voice-detection-api
Environment="PATH=/home/ubuntu/ai-voice-detection-api/venv/bin"
ExecStart=/home/ubuntu/ai-voice-detection-api/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start voice-api
sudo systemctl enable voice-api
sudo systemctl status voice-api
```

10. **Test Deployment**

```bash
curl http://your-ec2-public-ip/health
```

---

## Option 4: Docker Deployment

For containerized deployment, create a Dockerfile.

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Train model on first run
RUN python src/ml/train.py

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t ai-voice-detection-api .

# Run container
docker run -d -p 8000:8000 \
  -e API_KEY=your-secret-key \
  ai-voice-detection-api
```

---

## Post-Deployment Checklist

- [ ] Health check endpoint responds: `/health`
- [ ] API documentation accessible: `/docs`
- [ ] Authentication working with API key
- [ ] Test voice detection endpoint with sample audio
- [ ] Monitor logs for errors
- [ ] Set up monitoring/alerts (optional)

## Monitoring

### Check Logs

**Render**: Dashboard → Logs tab

**Railway**: `railway logs`

**EC2**: `sudo journalctl -u voice-api -f`

**Docker**: `docker logs <container-id> -f`

### Health Checks

Set up automated health checks:

```bash
# Cron job to ping health endpoint
*/5 * * * * curl https://your-api-url.com/health
```

## Scaling Considerations

For production workloads:

1. **Use managed ML services** (AWS SageMaker, Google AI Platform)
2. **Add load balancer** for multiple instances
3. **Use CDN** for global distribution
4. **Implement caching** for common predictions
5. **Add rate limiting** to prevent abuse

## Troubleshooting

### Issue: Model file not found

**Solution**: Ensure model is trained before deployment or include pre-trained model in repo

### Issue: Audio processing errors

**Solution**: Verify system dependencies (libsndfile1, ffmpeg) are installed

### Issue: High latency

**Solution**: 
- Use larger instance type
- Optimize model (quantization, pruning)
- Cache predictions for common inputs

## Security Recommendations

1. **Use strong API keys**: Generate cryptographically secure keys
2. **Enable HTTPS**: Use SSL certificates (Let's Encrypt)
3. **Rate limiting**: Implement request throttling
4. **Input validation**: Already implemented via Pydantic
5. **Monitor logs**: Set up alerts for suspicious activity

## Support

For deployment issues, check:
- Application logs
- System resource usage (CPU, memory)
- Network connectivity
- Environment variables

---

**Deployment Complete!** 🚀

Your AI Voice Detection API is now live and ready for hackathon submission!
