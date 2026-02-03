# API Examples

Code examples for using the AI Voice Detection API in various programming languages.

## Table of Contents

- [curl](#curl-examples)
- [Python](#python-example)
- [JavaScript (Node.js)](#javascript-nodejs-example)
- [JavaScript (Browser)](#javascript-browser-example)
- [cURL with Audio File](#curl-with-audio-file)

---

## curl Examples

### Basic Request

```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA..."
  }'
```

### Test All Languages

```bash
# Tamil
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{"language": "Tamil", "audioFormat": "mp3", "audioBase64": "..."}'

# English
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{"language": "English", "audioFormat": "mp3", "audioBase64": "..."}'

# Hindi
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{"language": "Hindi", "audioFormat": "mp3", "audioBase64": "..."}'

# Malayalam
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{"language": "Malayalam", "audioFormat": "mp3", "audioBase64": "..."}'

# Telugu
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{"language": "Telugu", "audioFormat": "mp3", "audioBase64": "..."}'
```

### Test Error Responses

```bash
# Missing API key
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -d '{"language": "English", "audioFormat": "mp3", "audioBase64": "test"}'

# Invalid language
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-change-this-in-production" \
  -d '{"language": "French", "audioFormat": "mp3", "audioBase64": "test"}'
```

---

## curl with Audio File

### Convert MP3 to Base64 and Send

```bash
#!/bin/bash

# Replace with your audio file and API key
AUDIO_FILE="sample.mp3"
API_KEY="your-secret-api-key-change-this-in-production"
LANGUAGE="English"

# Convert audio to base64
AUDIO_BASE64=$(base64 -i "$AUDIO_FILE" | tr -d '\n')

# Make API request
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{
    \"language\": \"$LANGUAGE\",
    \"audioFormat\": \"mp3\",
    \"audioBase64\": \"$AUDIO_BASE64\"
  }"
```

---

## Python Example

### Using requests library

```python
import requests
import base64
import json

def detect_ai_voice(audio_file_path, language="English", api_key="your-secret-api-key-change-this-in-production"):
    """
    Detect if audio is AI-generated or human.
    
    Args:
        audio_file_path: Path to MP3 audio file
        language: Language of the audio (Tamil, English, Hindi, Malayalam, Telugu)
        api_key: API key for authentication
        
    Returns:
        dict: API response with classification and confidence
    """
    # Read and encode audio file
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Prepare request
    url = "http://localhost:8000/api/voice-detection"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    # Make request
    response = requests.post(url, headers=headers, json=payload)
    
    # Handle response
    if response.status_code == 200:
        result = response.json()
        print(f"Status: {result['status']}")
        print(f"Classification: {result['classification']}")
        print(f"Confidence: {result['confidenceScore']:.2%}")
        print(f"Explanation: {result['explanation']}")
        return result
    else:
        error = response.json()
        print(f"Error: {error.get('message', 'Unknown error')}")
        return None

# Example usage
if __name__ == "__main__":
    result = detect_ai_voice("sample_audio.mp3", language="English")
```

### Async Python Example

```python
import aiohttp
import asyncio
import base64

async def detect_ai_voice_async(audio_file_path, language="English"):
    """Async version of voice detection."""
    
    # Read and encode audio
    with open(audio_file_path, 'rb') as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    url = "http://localhost:8000/api/voice-detection"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "your-secret-api-key-change-this-in-production"
    }
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error = await response.json()
                raise Exception(error.get('message'))

# Run async function
result = asyncio.run(detect_ai_voice_async("sample.mp3"))
print(result)
```

---

## JavaScript (Node.js) Example

### Using axios

```javascript
const axios = require('axios');
const fs = require('fs');

async function detectAIVoice(audioFilePath, language = 'English') {
    try {
        // Read and encode audio file
        const audioBuffer = fs.readFileSync(audioFilePath);
        const audioBase64 = audioBuffer.toString('base64');
        
        // Make API request
        const response = await axios.post(
            'http://localhost:8000/api/voice-detection',
            {
                language: language,
                audioFormat: 'mp3',
                audioBase64: audioBase64
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': 'your-secret-api-key-change-this-in-production'
                }
            }
        );
        
        // Handle response
        const result = response.data;
        console.log(`Status: ${result.status}`);
        console.log(`Classification: ${result.classification}`);
        console.log(`Confidence: ${(result.confidenceScore * 100).toFixed(2)}%`);
        console.log(`Explanation: ${result.explanation}`);
        
        return result;
        
    } catch (error) {
        if (error.response) {
            console.error(`Error: ${error.response.data.message}`);
        } else {
            console.error(`Error: ${error.message}`);
        }
        return null;
    }
}

// Example usage
detectAIVoice('sample_audio.mp3', 'English');
```

### Using fetch (Node.js 18+)

```javascript
const fs = require('fs');

async function detectAIVoice(audioFilePath, language = 'English') {
    // Read and encode audio
    const audioBuffer = fs.readFileSync(audioFilePath);
    const audioBase64 = audioBuffer.toString('base64');
    
    const response = await fetch('http://localhost:8000/api/voice-detection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': 'your-secret-api-key-change-this-in-production'
        },
        body: JSON.stringify({
            language: language,
            audioFormat: 'mp3',
            audioBase64: audioBase64
        })
    });
    
    const result = await response.json();
    
    if (response.ok) {
        console.log('Classification:', result.classification);
        console.log('Confidence:', result.confidenceScore);
        console.log('Explanation:', result.explanation);
        return result;
    } else {
        console.error('Error:', result.message);
        return null;
    }
}

detectAIVoice('sample.mp3');
```

---

## JavaScript (Browser) Example

### Using FileReader API

```html
<!DOCTYPE html>
<html>
<head>
    <title>AI Voice Detection</title>
</head>
<body>
    <h1>AI Voice Detection</h1>
    
    <input type="file" id="audioFile" accept=".mp3" />
    <select id="language">
        <option value="English">English</option>
        <option value="Tamil">Tamil</option>
        <option value="Hindi">Hindi</option>
        <option value="Malayalam">Malayalam</option>
        <option value="Telugu">Telugu</option>
    </select>
    <button onclick="detectVoice()">Detect</button>
    
    <div id="result"></div>
    
    <script>
        async function detectVoice() {
            const fileInput = document.getElementById('audioFile');
            const languageSelect = document.getElementById('language');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                alert('Please select an audio file');
                return;
            }
            
            // Read file and convert to base64
            const file = fileInput.files[0];
            const reader = new FileReader();
            
            reader.onload = async function(e) {
                const audioBase64 = btoa(
                    new Uint8Array(e.target.result)
                        .reduce((data, byte) => data + String.fromCharCode(byte), '')
                );
                
                try {
                    // Make API request
                    const response = await fetch('http://localhost:8000/api/voice-detection', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'x-api-key': 'your-secret-api-key-change-this-in-production'
                        },
                        body: JSON.stringify({
                            language: languageSelect.value,
                            audioFormat: 'mp3',
                            audioBase64: audioBase64
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <h2>Result</h2>
                            <p><strong>Classification:</strong> ${result.classification}</p>
                            <p><strong>Confidence:</strong> ${(result.confidenceScore * 100).toFixed(2)}%</p>
                            <p><strong>Explanation:</strong> ${result.explanation}</p>
                        `;
                    } else {
                        resultDiv.innerHTML = `<p style="color: red;">Error: ${result.message}</p>`;
                    }
                    
                } catch (error) {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                }
            };
            
            reader.readAsArrayBuffer(file);
        }
    </script>
</body>
</html>
```

---

## Expected Responses

### Success Response

```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.8742,
  "explanation": "Detected unnatural pitch consistency typical of AI synthesis and found robotic spectral artifacts in frequency distribution"
}
```

### Error Responses

**Missing API Key (401)**
```json
{
  "status": "error",
  "message": "Missing API key. Please provide x-api-key header."
}
```

**Invalid API Key (401)**
```json
{
  "status": "error",
  "message": "Invalid API key"
}
```

**Invalid Request (400)**
```json
{
  "status": "error",
  "message": "Invalid audio data: Failed to decode audio: ..."
}
```

---

## Testing Tips

1. **Generate Test Audio**: Use text-to-speech tools to create AI-generated samples
2. **Record Real Voice**: Use your phone to record human speech samples
3. **Test All Languages**: Verify the API accepts all 5 supported languages
4. **Test Edge Cases**: Try very short audio, very long audio, corrupted files
5. **Monitor Confidence**: Check that confidence scores are reasonable (0.0-1.0)

---

## Rate Limiting

For production deployments, consider implementing client-side rate limiting:

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=10):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_minute=10)
def detect_ai_voice(audio_path):
    # Your detection logic
    pass
```

---

**Ready to test!** 🎯

Choose your preferred language and start integrating the AI Voice Detection API!
