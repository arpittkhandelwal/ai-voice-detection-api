"""Model training script for AI voice detection."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import librosa
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ml.model import VoiceClassifierCNN, VoiceDetectionModel
from config import MODEL_PATH, SAMPLE_RATE, N_MFCC


class SyntheticVoiceDataset(Dataset):
    """Generate synthetic voice data for training."""
    
    def __init__(self, num_samples: int = 1000, duration: float = 3.0, sample_rate: int = 22050):
        """
        Initialize synthetic dataset.
        
        Args:
            num_samples: Number of samples to generate
            duration: Duration of each sample in seconds
            sample_rate: Audio sample rate
        """
        self.num_samples = num_samples
        self.duration = duration
        self.sample_rate = sample_rate
        self.n_mfcc = 40
        self.target_length = 128
        
        # Generate all samples upfront
        self.data = []
        self.labels = []
        self._generate_dataset()
    
    def _generate_ai_sample(self) -> np.ndarray:
        """
        Generate synthetic AI-like audio.
        
        AI characteristics:
        - Very consistent pitch
        - Lack of natural pauses
        - Robotic spectral patterns
        - Regular rhythm
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        
        # Consistent fundamental frequency (very little variation)
        f0 = 200 + np.random.randn() * 5  # Very small variation
        
        # Generate base signal with harmonics
        signal = np.sin(2 * np.pi * f0 * t)
        signal += 0.5 * np.sin(2 * np.pi * 2 * f0 * t)  # Second harmonic
        signal += 0.3 * np.sin(2 * np.pi * 3 * f0 * t)  # Third harmonic
        
        # Add very small amount of noise (AI is cleaner)
        signal += np.random.randn(len(t)) * 0.02
        
        # No natural pauses (continuous signal)
        # Regular amplitude
        amplitude = 0.5 + 0.1 * np.sin(2 * np.pi * 2 * t)
        signal *= amplitude
        
        return signal
    
    def _generate_human_sample(self) -> np.ndarray:
        """
        Generate synthetic human-like audio.
        
        Human characteristics:
        - Natural pitch variation
        - Micro-pauses
        - Varied spectral content
        - Natural prosody
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        
        # Variable fundamental frequency (natural pitch variation)
        f0_base = 150 + np.random.randn() * 30
        f0_variation = 20 * np.sin(2 * np.pi * 0.5 * t) + np.random.randn(len(t)) * 10
        f0 = f0_base + f0_variation
        
        # Generate signal with time-varying frequency
        phase = 2 * np.pi * np.cumsum(f0) / self.sample_rate
        signal = np.sin(phase)
        
        # Add harmonics with variation
        signal += 0.4 * np.sin(2 * phase + np.random.randn(len(t)) * 0.1)
        signal += 0.2 * np.sin(3 * phase + np.random.randn(len(t)) * 0.1)
        
        # Add natural noise
        signal += np.random.randn(len(t)) * 0.1
        
        # Add micro-pauses (simulate breathing/breaks)
        num_pauses = np.random.randint(2, 5)
        for _ in range(num_pauses):
            pause_start = np.random.randint(0, len(signal) - 2000)
            pause_duration = np.random.randint(500, 2000)
            signal[pause_start:pause_start + pause_duration] *= 0.1
        
        # Natural amplitude variation (prosody)
        amplitude = 0.3 + 0.3 * np.random.randn(len(t)).cumsum() / 100
        amplitude = np.clip(amplitude, 0.2, 0.8)
        signal *= amplitude
        
        return signal
    
    def _audio_to_mfcc(self, audio: np.ndarray) -> np.ndarray:
        """Convert audio to MFCC features."""
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc
        )
        
        # Pad or truncate to target length
        if mfcc.shape[1] < self.target_length:
            pad_width = self.target_length - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
        else:
            mfcc = mfcc[:, :self.target_length]
        
        return mfcc
    
    def _generate_dataset(self):
        """Generate the complete dataset."""
        print(f"Generating {self.num_samples} synthetic voice samples...")
        
        for i in range(self.num_samples):
            # Generate equal numbers of AI and Human samples
            if i % 2 == 0:
                audio = self._generate_ai_sample()
                label = 0  # AI_GENERATED
            else:
                audio = self._generate_human_sample()
                label = 1  # HUMAN
            
            # Convert to MFCC
            mfcc = self._audio_to_mfcc(audio)
            
            self.data.append(mfcc)
            self.labels.append(label)
            
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1}/{self.num_samples} samples")
        
        print("Dataset generation complete!")
    
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        mfcc = torch.FloatTensor(self.data[idx])
        label = torch.LongTensor([self.labels[idx]])
        return mfcc, label


def train_model(num_epochs: int = 50, batch_size: int = 32, learning_rate: float = 0.001):
    """
    Train the voice detection model.
    
    Args:
        num_epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Learning rate
    """
    print("=" * 50)
    print("AI Voice Detection Model Training")
    print("=" * 50)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nUsing device: {device}")
    
    # Generate dataset
    print("\n--- Generating Training Data ---")
    train_dataset = SyntheticVoiceDataset(num_samples=1000, duration=3.0)
    val_dataset = SyntheticVoiceDataset(num_samples=200, duration=3.0)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model
    print("\n--- Initializing Model ---")
    model = VoiceClassifierCNN(input_channels=40, num_classes=2)
    model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)
    
    # Training loop
    print(f"\n--- Training for {num_epochs} Epochs ---")
    best_val_loss = float('inf')
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.squeeze().to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Statistics
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += target.size(0)
            train_correct += (predicted == target).sum().item()
        
        avg_train_loss = train_loss / len(train_loader)
        train_accuracy = 100 * train_correct / train_total
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.squeeze().to(device)
                outputs = model(data)
                loss = criterion(outputs, target)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += target.size(0)
                val_correct += (predicted == target).sum().item()
        
        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = 100 * val_correct / val_total
        
        # Learning rate scheduling
        scheduler.step(avg_val_loss)
        
        # Print progress
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}]")
            print(f"  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.2f}%")
            print(f"  Val Loss: {avg_val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")
        
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            save_path = Path(MODEL_PATH)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            checkpoint = {
                'model_state_dict': model.state_dict(),
                'epoch': epoch,
                'loss': best_val_loss
            }
            torch.save(checkpoint, save_path)
    
    print("\n" + "=" * 50)
    print(f"Training Complete! Best Val Loss: {best_val_loss:.4f}")
    print(f"Model saved to: {MODEL_PATH}")
    print("=" * 50)


if __name__ == "__main__":
    # Train the model
    train_model(num_epochs=50, batch_size=32, learning_rate=0.001)
