"""Audio feature extraction module for AI voice detection."""
import base64
import io
import numpy as np
import librosa
import soundfile as sf
from typing import Dict, Tuple


class AudioFeatureExtractor:
    """Extract audio features for ML model input."""
    
    def __init__(self, sample_rate: int = 22050, n_mfcc: int = 40):
        """
        Initialize the feature extractor.
        
        Args:
            sample_rate: Target sample rate for audio processing
            n_mfcc: Number of MFCC coefficients to extract
        """
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
    
    def decode_base64_audio(self, audio_base64: str) -> Tuple[np.ndarray, int]:
        """
        Decode base64 encoded audio to numpy array.
        
        Args:
            audio_base64: Base64 encoded audio string
            
        Returns:
            Tuple of (audio array, sample rate)
        """
        try:
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(audio_base64)
            
            # Load audio from bytes
            audio_io = io.BytesIO(audio_bytes)
            audio, sr = librosa.load(audio_io, sr=self.sample_rate, mono=True)
            
            return audio, sr
        except Exception as e:
            raise ValueError(f"Failed to decode audio: {str(e)}")
    
    def extract_mfcc(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract MFCC features from audio.
        
        Args:
            audio: Audio time series
            
        Returns:
            MFCC feature matrix
        """
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc
        )
        return mfcc
    
    def extract_spectral_features(self, audio: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Extract spectral features from audio.
        
        Args:
            audio: Audio time series
            
        Returns:
            Dictionary of spectral features
        """
        # Spectral centroid - indicates where the "center of mass" of the spectrum is
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio, sr=self.sample_rate
        )[0]
        
        # Spectral rolloff - frequency below which a specified percentage of total spectral energy lies
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio, sr=self.sample_rate
        )[0]
        
        # Spectral contrast - difference between peaks and valleys in the spectrum
        spectral_contrast = librosa.feature.spectral_contrast(
            y=audio, sr=self.sample_rate
        )
        
        return {
            "spectral_centroid": spectral_centroid,
            "spectral_rolloff": spectral_rolloff,
            "spectral_contrast": spectral_contrast
        }
    
    def extract_pitch_features(self, audio: np.ndarray) -> Dict[str, float]:
        """
        Extract pitch and tempo features.
        
        Args:
            audio: Audio time series
            
        Returns:
            Dictionary of pitch/tempo features
        """
        # Extract pitch (fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=audio, sr=self.sample_rate)
        
        # Get pitch values where magnitude is significant
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        # Calculate pitch statistics
        if len(pitch_values) > 0:
            pitch_mean = np.mean(pitch_values)
            pitch_std = np.std(pitch_values)
            pitch_var = np.var(pitch_values)
        else:
            pitch_mean = pitch_std = pitch_var = 0.0
        
        # Extract tempo
        tempo, _ = librosa.beat.beat_track(y=audio, sr=self.sample_rate)
        
        return {
            "pitch_mean": float(pitch_mean),
            "pitch_std": float(pitch_std),
            "pitch_var": float(pitch_var),
            "tempo": float(tempo)
        }
    
    def extract_all_features(self, audio_base64: str) -> Dict[str, np.ndarray]:
        """
        Extract all features from base64 encoded audio.
        
        Args:
            audio_base64: Base64 encoded audio string
            
        Returns:
            Dictionary containing all extracted features
        """
        # Decode audio
        audio, _ = self.decode_base64_audio(audio_base64)
        
        # Extract features
        mfcc = self.extract_mfcc(audio)
        spectral_features = self.extract_spectral_features(audio)
        pitch_features = self.extract_pitch_features(audio)
        
        # Combine all features
        features = {
            "mfcc": mfcc,
            "spectral_centroid": spectral_features["spectral_centroid"],
            "spectral_rolloff": spectral_features["spectral_rolloff"],
            "spectral_contrast": spectral_features["spectral_contrast"],
            "pitch_mean": pitch_features["pitch_mean"],
            "pitch_std": pitch_features["pitch_std"],
            "pitch_var": pitch_features["pitch_var"],
            "tempo": pitch_features["tempo"],
            "audio": audio  # Include raw audio for model
        }
        
        return features
    
    def normalize_features(self, features: np.ndarray) -> np.ndarray:
        """
        Normalize features to zero mean and unit variance.
        
        Args:
            features: Feature matrix
            
        Returns:
            Normalized features
        """
        mean = np.mean(features, axis=0, keepdims=True)
        std = np.std(features, axis=0, keepdims=True)
        std[std == 0] = 1  # Avoid division by zero
        
        return (features - mean) / std
