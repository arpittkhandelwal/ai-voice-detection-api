"""
Quick verification script to test the complete API flow.
Run this after training the model to verify everything works.
"""
import subprocess
import time
import sys
import os

def check_dependencies():
    """Check if all dependencies are installed."""
    print("=" * 50)
    print("Checking Dependencies")
    print("=" * 50)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'librosa',
        'torch',
        'numpy',
        'pydantic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed")
    return True


def check_model_exists():
    """Check if trained model exists."""
    print("\n" + "=" * 50)
    print("Checking Model File")
    print("=" * 50)
    
    model_path = "models/voice_classifier.pth"
    
    if os.path.exists(model_path):
        size = os.path.getsize(model_path)
        print(f"✓ Model found: {model_path}")
        print(f"  Size: {size / 1024:.2f} KB")
        return True
    else:
        print(f"✗ Model not found: {model_path}")
        print("\nTrain the model first:")
        print("  python src/ml/train.py")
        return False


def check_env_file():
    """Check if .env file exists."""
    print("\n" + "=" * 50)
    print("Checking Configuration")
    print("=" * 50)
    
    if os.path.exists('.env'):
        print("✓ .env file found")
        
        # Read API key
        with open('.env', 'r') as f:
            content = f.read()
            if 'API_KEY=' in content:
                print("✓ API_KEY configured")
            else:
                print("⚠️  API_KEY not found in .env")
        return True
    else:
        print("⚠️  .env file not found")
        print("Creating from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ .env created from .env.example")
            print("  Please edit .env and set your API key")
        return False


def test_feature_extraction():
    """Test audio feature extraction."""
    print("\n" + "=" * 50)
    print("Testing Feature Extraction")
    print("=" * 50)
    
    try:
        from src.ml.feature_extraction import AudioFeatureExtractor
        import numpy as np
        import base64
        import soundfile as sf
        import io
        
        # Create test audio (1 second of 440Hz tone)
        sample_rate = 22050
        duration = 1
        t = np.linspace(0, duration, sample_rate * duration)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        # Convert to bytes
        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, audio, sample_rate, format='WAV')
        audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode('utf-8')
        
        # Test extraction
        extractor = AudioFeatureExtractor()
        features = extractor.extract_all_features(audio_base64)
        
        print("✓ Audio decoding successful")
        print(f"✓ MFCC shape: {features['mfcc'].shape}")
        print(f"✓ Pitch mean: {features['pitch_mean']:.2f} Hz")
        print(f"✓ Tempo: {features['tempo']:.2f} BPM")
        
        return True
        
    except Exception as e:
        print(f"✗ Feature extraction failed: {e}")
        return False


def test_model_loading():
    """Test model loading."""
    print("\n" + "=" * 50)
    print("Testing Model Loading")
    print("=" * 50)
    
    try:
        from src.ml.model import VoiceDetectionModel
        from src.config import MODEL_PATH
        import numpy as np
        
        model = VoiceDetectionModel(model_path=MODEL_PATH)
        print("✓ Model loaded successfully")
        
        # Test prediction with dummy MFCC
        dummy_mfcc = np.random.randn(40, 128).astype(np.float32)
        classification, confidence = model.predict(dummy_mfcc)
        
        print(f"✓ Model inference successful")
        print(f"  Classification: {classification}")
        print(f"  Confidence: {confidence:.4f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print(" AI Voice Detection API - Verification Script")
    print("=" * 60)
    
    results = []
    
    # Run checks
    results.append(("Dependencies", check_dependencies()))
    results.append(("Configuration", check_env_file()))
    results.append(("Model File", check_model_exists()))
    results.append(("Feature Extraction", test_feature_extraction()))
    results.append(("Model Loading", test_model_loading()))
    
    # Summary
    print("\n" + "=" * 60)
    print(" Verification Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:10} {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All checks passed!")
        print("\nReady to start the API server:")
        print("  uvicorn src.api.main:app --host 0.0.0.0 --port 8000")
        print("\nThen visit:")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - Health Check: http://localhost:8000/health")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
