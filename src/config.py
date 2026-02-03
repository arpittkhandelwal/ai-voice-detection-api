"""Configuration management for the AI Voice Detection API."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# API Configuration
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-this-in-production")

# Model Configuration
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "voice_classifier.pth"))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Supported languages
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# Audio processing settings
SAMPLE_RATE = 22050  # Standard sample rate for librosa
N_MFCC = 40  # Number of MFCC coefficients
MAX_AUDIO_DURATION = 30  # Maximum audio duration in seconds
