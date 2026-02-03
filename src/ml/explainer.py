"""Explainability module for voice detection predictions."""
import numpy as np
from typing import Dict


class VoiceExplainer:
    """Generate human-readable explanations for predictions."""
    
    def __init__(self):
        """Initialize the explainer."""
        pass
    
    def analyze_pitch_consistency(self, pitch_std: float, pitch_var: float) -> str:
        """
        Analyze pitch consistency patterns.
        
        Args:
            pitch_std: Standard deviation of pitch
            pitch_var: Variance of pitch
            
        Returns:
            Explanation text
        """
        # AI-generated voices often have very consistent pitch
        if pitch_std < 20:
            return "unnatural pitch consistency typical of AI synthesis"
        elif pitch_std > 80:
            return "natural pitch variation expected in human speech"
        else:
            return "moderate pitch variation"
    
    def analyze_spectral_pattern(self, spectral_features: Dict) -> str:
        """
        Analyze spectral patterns for artifacts.
        
        Args:
            spectral_features: Dictionary of spectral features
            
        Returns:
            Explanation text
        """
        # Analyze spectral centroid variance
        centroid_var = np.var(spectral_features.get("spectral_centroid", [0]))
        
        if centroid_var < 100000:
            return "robotic spectral artifacts in frequency distribution"
        else:
            return "natural spectral variation in voice timbre"
    
    def analyze_prosody(self, tempo: float, pitch_mean: float) -> str:
        """
        Analyze prosody patterns.
        
        Args:
            tempo: Detected tempo
            pitch_mean: Mean pitch
            
        Returns:
            Explanation text
        """
        # AI voices can have overly regular tempo
        if tempo > 0 and tempo < 80:
            return "synthetic prosody with regular tempo patterns"
        elif tempo > 140:
            return "natural prosodic rhythm"
        else:
            return "moderate prosodic variation"
    
    def detect_micro_pauses(self, audio: np.ndarray, sample_rate: int = 22050) -> str:
        """
        Detect presence of micro-pauses in speech.
        
        Args:
            audio: Audio time series
            sample_rate: Sample rate
            
        Returns:
            Explanation text
        """
        # Calculate zero-crossing rate (indicator of pauses)
        zcr = np.sum(np.abs(np.diff(np.sign(audio)))) / (2 * len(audio))
        
        if zcr < 0.05:
            return "lack of natural micro-pauses between words"
        else:
            return "natural breathing patterns and micro-pauses detected"
    
    def generate_explanation(
        self,
        classification: str,
        features: Dict[str, any],
        confidence: float
    ) -> str:
        """
        Generate comprehensive explanation for the prediction.
        
        Args:
            classification: Predicted class (AI_GENERATED or HUMAN)
            features: Extracted audio features
            confidence: Confidence score
            
        Returns:
            Human-readable explanation
        """
        explanations = []
        
        # Analyze pitch
        pitch_std = features.get("pitch_std", 0)
        pitch_var = features.get("pitch_var", 0)
        pitch_explanation = self.analyze_pitch_consistency(pitch_std, pitch_var)
        
        # Analyze spectral patterns
        spectral_features = {
            "spectral_centroid": features.get("spectral_centroid", []),
            "spectral_rolloff": features.get("spectral_rolloff", []),
        }
        spectral_explanation = self.analyze_spectral_pattern(spectral_features)
        
        # Analyze prosody
        tempo = features.get("tempo", 0)
        pitch_mean = features.get("pitch_mean", 0)
        prosody_explanation = self.analyze_prosody(tempo, pitch_mean)
        
        # Analyze micro-pauses
        audio = features.get("audio", np.array([]))
        if len(audio) > 0:
            pause_explanation = self.detect_micro_pauses(audio)
        else:
            pause_explanation = "unable to analyze pause patterns"
        
        # Build explanation based on classification
        if classification == "AI_GENERATED":
            # Focus on AI-like patterns
            if "unnatural" in pitch_explanation or "consistent" in pitch_explanation:
                explanations.append(f"Detected {pitch_explanation}")
            
            if "robotic" in spectral_explanation or "artifacts" in spectral_explanation:
                explanations.append(f"Found {spectral_explanation}")
            
            if "lack of" in pause_explanation:
                explanations.append(f"Observed {pause_explanation}")
            
            if "synthetic" in prosody_explanation:
                explanations.append(f"Identified {prosody_explanation}")
            
            # Default if no specific patterns found
            if not explanations:
                explanations.append("Multiple AI-generated voice indicators detected in audio patterns")
        
        else:  # HUMAN
            # Focus on human-like patterns
            if "natural" in pitch_explanation:
                explanations.append(f"Detected {pitch_explanation}")
            
            if "natural" in spectral_explanation:
                explanations.append(f"Found {spectral_explanation}")
            
            if "natural" in pause_explanation or "breathing" in pause_explanation:
                explanations.append(f"Observed {pause_explanation}")
            
            if "natural" in prosody_explanation:
                explanations.append(f"Identified {prosody_explanation}")
            
            # Default if no specific patterns found
            if not explanations:
                explanations.append("Multiple human voice characteristics detected in speech patterns")
        
        # Combine explanations
        if len(explanations) > 2:
            explanation = f"{explanations[0]} and {explanations[1]}"
        elif len(explanations) > 0:
            explanation = explanations[0]
        else:
            explanation = "Analysis based on comprehensive audio feature patterns"
        
        # Capitalize first letter
        explanation = explanation[0].upper() + explanation[1:]
        
        return explanation
