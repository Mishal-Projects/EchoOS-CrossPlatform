"""
Download Vosk Speech Recognition Model
Downloads the small English model for offline speech recognition
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

# Model URL and details
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_NAME = "vosk-model-small-en-us-0.15"
MODELS_DIR = Path("models")


def download_model():
    """Download and extract Vosk model"""
    print("=" * 60)
    print("EchoOS - Vosk Model Downloader")
    print("=" * 60)
    print()
    
    # Create models directory
    MODELS_DIR.mkdir(exist_ok=True)
    
    # Check if model already exists
    model_path = MODELS_DIR / MODEL_NAME
    if model_path.exists():
        print(f"✓ Model already exists at: {model_path}")
        print("  If you want to re-download, delete the directory first.")
        return True
    
    # Download model
    zip_path = MODELS_DIR / f"{MODEL_NAME}.zip"
    
    print(f"Downloading model from: {MODEL_URL}")
    print(f"Size: ~40 MB")
    print()
    
    try:
        def progress_hook(count, block_size, total_size):
            """Show download progress"""
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\rProgress: {percent}% ")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(MODEL_URL, zip_path, progress_hook)
        print("\n✓ Download complete!")
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        return False
    
    # Extract model
    print("\nExtracting model...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MODELS_DIR)
        
        print("✓ Extraction complete!")
        
        # Remove zip file
        zip_path.unlink()
        print("✓ Cleaned up zip file")
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✓ Model installation complete!")
    print(f"  Model location: {model_path}")
    print("=" * 60)
    print()
    print("You can now run EchoOS:")
    print("  python main.py")
    print()
    
    return True


if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
