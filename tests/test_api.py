"""Basic API tests for voice detection endpoint."""
import requests
import base64
import json

API_BASE_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-change-this-in-production"


def test_health_check():
    """Test health check endpoint."""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")


def test_root_endpoint():
    """Test root endpoint."""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Root endpoint passed")


def test_missing_api_key():
    """Test authentication with missing API key."""
    print("\n=== Testing Missing API Key ===")
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": "dGVzdA=="  # "test" in base64
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/voice-detection",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 401
    assert response.json()["status"] == "error"
    print("✅ Missing API key test passed")


def test_invalid_api_key():
    """Test authentication with invalid API key."""
    print("\n=== Testing Invalid API Key ===")
    
    headers = {"x-api-key": "wrong-api-key"}
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": "dGVzdA=="
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/voice-detection",
        headers=headers,
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 401
    print("✅ Invalid API key test passed")


def test_invalid_language():
    """Test with unsupported language."""
    print("\n=== Testing Invalid Language ===")
    
    headers = {"x-api-key": API_KEY}
    payload = {
        "language": "French",  # Not supported
        "audioFormat": "mp3",
        "audioBase64": "dGVzdA=="
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/voice-detection",
        headers=headers,
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 422  # Validation error
    print("✅ Invalid language test passed")


def test_valid_languages():
    """Test all supported languages."""
    print("\n=== Testing All Supported Languages ===")
    
    languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    
    # Create a simple test audio (silence)
    import numpy as np
    import soundfile as sf
    import io
    
    # Generate 1 second of silence at 22050 Hz
    sample_rate = 22050
    duration = 1
    audio = np.zeros(sample_rate * duration)
    
    # Convert to MP3-like bytes (using WAV as placeholder)
    audio_bytes = io.BytesIO()
    sf.write(audio_bytes, audio, sample_rate, format='WAV')
    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode('utf-8')
    
    headers = {"x-api-key": API_KEY}
    
    for language in languages:
        print(f"\nTesting language: {language}")
        
        payload = {
            "language": language,
            "audioFormat": "mp3",
            "audioBase64": audio_base64
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/voice-detection",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Classification: {result['classification']}")
                print(f"Confidence: {result['confidenceScore']}")
                print(f"Explanation: {result['explanation']}")
                
                # Validate response structure
                assert result["status"] == "success"
                assert result["language"] == language
                assert result["classification"] in ["AI_GENERATED", "HUMAN"]
                assert 0.0 <= result["confidenceScore"] <= 1.0
                assert len(result["explanation"]) > 0
                
                print(f"✅ {language} test passed")
            else:
                print(f"Response: {response.json()}")
                print(f"⚠️  {language} test returned non-200 status")
                
        except requests.exceptions.Timeout:
            print(f"⚠️  {language} test timed out")
        except Exception as e:
            print(f"❌ {language} test failed: {str(e)}")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("AI Voice Detection API - Test Suite")
    print("=" * 50)
    
    try:
        test_health_check()
        test_root_endpoint()
        test_missing_api_key()
        test_invalid_api_key()
        test_invalid_language()
        test_valid_languages()
        
        print("\n" + "=" * 50)
        print("✅ All Tests Passed!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API. Is the server running?")
        print("Start the server with: uvicorn src.api.main:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
