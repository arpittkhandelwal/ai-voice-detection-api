"""CNN-based model for AI voice detection."""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from pathlib import Path
from typing import Tuple


class VoiceClassifierCNN(nn.Module):
    """1D CNN for classifying AI-generated vs human voice."""
    
    def __init__(self, input_channels: int = 40, num_classes: int = 2):
        """
        Initialize the CNN model.
        
        Args:
            input_channels: Number of input feature channels (e.g., MFCC coefficients)
            num_classes: Number of output classes (2: AI_GENERATED, HUMAN)
        """
        super(VoiceClassifierCNN, self).__init__()
        
        # Convolutional layers for temporal feature learning
        self.conv1 = nn.Conv1d(input_channels, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(64)
        self.pool1 = nn.MaxPool1d(2)
        
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(128)
        self.pool2 = nn.MaxPool1d(2)
        
        self.conv3 = nn.Conv1d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(256)
        self.pool3 = nn.MaxPool1d(2)
        
        # Global average pooling
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        
        # Fully connected layers
        self.fc1 = nn.Linear(256, 128)
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 64)
        self.dropout2 = nn.Dropout(0.3)
        self.fc3 = nn.Linear(64, num_classes)
    
    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x: Input tensor of shape (batch_size, input_channels, time_steps)
            
        Returns:
            Output logits of shape (batch_size, num_classes)
        """
        # Convolutional blocks
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        
        # Global pooling
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        
        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.dropout1(x)
        x = F.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        
        return x


class VoiceDetectionModel:
    """Wrapper class for model loading and inference."""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the model.
        
        Args:
            model_path: Path to saved model weights
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = VoiceClassifierCNN()
        self.model.to(self.device)
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        
        self.model.eval()
    
    def load_model(self, model_path: str):
        """
        Load model weights from file.
        
        Args:
            model_path: Path to model weights
        """
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Warning: Could not load model from {model_path}: {e}")
            print("Using randomly initialized weights.")
    
    def save_model(self, model_path: str, epoch: int = 0, loss: float = 0.0):
        """
        Save model weights to file.
        
        Args:
            model_path: Path to save model weights
            epoch: Training epoch number
            loss: Training loss
        """
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'epoch': epoch,
            'loss': loss
        }
        torch.save(checkpoint, model_path)
        print(f"Model saved to {model_path}")
    
    def preprocess_mfcc(self, mfcc: np.ndarray, target_length: int = 128) -> torch.Tensor:
        """
        Preprocess MFCC features for model input.
        
        Args:
            mfcc: MFCC feature matrix (n_mfcc, time_steps)
            target_length: Target time dimension
            
        Returns:
            Preprocessed tensor
        """
        # Pad or truncate to target length
        if mfcc.shape[1] < target_length:
            # Pad with zeros
            pad_width = target_length - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
        else:
            # Truncate
            mfcc = mfcc[:, :target_length]
        
        # Convert to tensor
        mfcc_tensor = torch.FloatTensor(mfcc).unsqueeze(0)  # Add batch dimension
        
        return mfcc_tensor
    
    def predict(self, mfcc: np.ndarray) -> Tuple[str, float]:
        """
        Predict whether audio is AI-generated or human.
        
        Args:
            mfcc: MFCC features
            
        Returns:
            Tuple of (classification, confidence_score)
        """
        self.model.eval()
        
        with torch.no_grad():
            # Preprocess input
            mfcc_tensor = self.preprocess_mfcc(mfcc)
            mfcc_tensor = mfcc_tensor.to(self.device)
            
            # Forward pass
            outputs = self.model(mfcc_tensor)
            probabilities = F.softmax(outputs, dim=1)
            
            # Get prediction
            confidence, predicted = torch.max(probabilities, 1)
            
            # Map to classification
            classification = "AI_GENERATED" if predicted.item() == 0 else "HUMAN"
            confidence_score = float(confidence.item())
            
            return classification, confidence_score
