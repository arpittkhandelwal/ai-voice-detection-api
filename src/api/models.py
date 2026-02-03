"""Pydantic models for API request and response validation."""
from pydantic import BaseModel, Field, validator
from typing import Literal
from src.config import SUPPORTED_LANGUAGES


class VoiceDetectionRequest(BaseModel):
    """Request model for voice detection endpoint."""
    
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"] = Field(
        ...,
        description="Language of the audio sample"
    )
    audioFormat: Literal["mp3"] = Field(
        ...,
        description="Audio format (currently only mp3 is supported)"
    )
    audioBase64: str = Field(
        ...,
        description="Base64 encoded MP3 audio file"
    )
    
    @validator("language")
    def validate_language(cls, v):
        """Validate that language is supported."""
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language must be one of: {', '.join(SUPPORTED_LANGUAGES)}")
        return v
    
    @validator("audioBase64")
    def validate_audio_base64(cls, v):
        """Validate that audioBase64 is not empty."""
        if not v or len(v) < 100:
            raise ValueError("audioBase64 must be a valid base64 encoded audio file")
        return v


class VoiceDetectionResponse(BaseModel):
    """Response model for successful voice detection."""
    
    status: Literal["success"] = "success"
    language: str = Field(..., description="Language from the request")
    classification: Literal["AI_GENERATED", "HUMAN"] = Field(
        ...,
        description="Classification result"
    )
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0"
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the classification"
    )


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    status: Literal["error"] = "error"
    message: str = Field(..., description="Error message")
