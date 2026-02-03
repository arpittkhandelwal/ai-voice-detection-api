"""API routes for voice detection."""
from fastapi import APIRouter, Depends, HTTPException, status
from src.api.models import VoiceDetectionRequest, VoiceDetectionResponse, ErrorResponse
from src.api.auth import verify_api_key
from src.ml.feature_extraction import AudioFeatureExtractor
from src.ml.model import VoiceDetectionModel
from src.ml.explainer import VoiceExplainer
from src.config import MODEL_PATH, SAMPLE_RATE, N_MFCC
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Initialize ML components (load once at startup)
feature_extractor = AudioFeatureExtractor(sample_rate=SAMPLE_RATE, n_mfcc=N_MFCC)
model = VoiceDetectionModel(model_path=MODEL_PATH)
explainer = VoiceExplainer()


@router.post(
    "/api/voice-detection",
    response_model=VoiceDetectionResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid or missing API key"},
        400: {"model": ErrorResponse, "description": "Bad Request - Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def detect_voice(
    request: VoiceDetectionRequest,
    api_key: str = Depends(verify_api_key)
) -> VoiceDetectionResponse:
    """
    Detect whether a voice sample is AI-generated or human.
    
    This endpoint accepts a base64-encoded MP3 audio file and returns a classification
    along with a confidence score and explanation.
    
    Args:
        request: Voice detection request containing language, audio format, and base64 audio
        api_key: Validated API key from header
        
    Returns:
        VoiceDetectionResponse with classification, confidence, and explanation
        
    Raises:
        HTTPException: For various error conditions
    """
    try:
        logger.info(f"Processing voice detection request for language: {request.language}")
        
        # Extract features from audio
        logger.info("Extracting audio features...")
        features = feature_extractor.extract_all_features(request.audioBase64)
        
        # Get MFCC for model prediction
        mfcc = features["mfcc"]
        
        # Make prediction
        logger.info("Running model inference...")
        classification, confidence_score = model.predict(mfcc)
        
        # Generate explanation
        logger.info("Generating explanation...")
        explanation = explainer.generate_explanation(
            classification=classification,
            features=features,
            confidence=confidence_score
        )
        
        # Create response
        response = VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence_score, 4),
            explanation=explanation
        )
        
        logger.info(f"Classification: {classification}, Confidence: {confidence_score:.4f}")
        
        return response
    
    except ValueError as e:
        # Handle audio decoding errors
        logger.error(f"ValueError: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid audio data: {str(e)}"
        )
    
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
