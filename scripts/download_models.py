#!/usr/bin/env python3
"""
Automated Model Downloader for EchoOS
Downloads required models for speech recognition and voice authentication
"""

import os
import sys
import zipfile
import tarfile
import requests
from pathlib import Path
from typing import Optional


def download_file(url: str, destination: Path, description: str = "file") -> bool:
    """
    Download file with progress bar
    
    Args:
        url: URL to download from
        destination: Destination file path
        description: Description for progress display
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\nDownloading {description}...")
        print(f"URL: {url}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        bar_length = 50
                        filled = int(bar_length * downloaded / total_size)
                        bar = '█' * filled + '-' * (bar_length - filled)
                        print(f'\r[{bar}] {percent:.1f}% ({downloaded}/{total_size} bytes)', end='')
        
        print(f"\n✓ Downloaded {description} successfully")
        return True
        
    except Exception as e:
        print(f"\n✗ Error downloading {description}: {e}")
        return False


def extract_archive(archive_path: Path, extract_to: Path) -> bool:
    """
    Extract zip or tar.gz archive
    
    Args:
        archive_path: Path to archive file
        extract_to: Destination directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\nExtracting {archive_path.name}...")
        
        extract_to.mkdir(parents=True, exist_ok=True)
        
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif archive_path.name.endswith('.tar.gz') or archive_path.name.endswith('.tgz'):
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_to)
        else:
            print(f"✗ Unsupported archive format: {archive_path.suffix}")
            return False
        
        print(f"✓ Extracted successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error extracting archive: {e}")
        return False


def download_vosk_model() -> bool:
    """Download Vosk speech recognition model"""
    print("\n" + "=" * 60)
    print("Downloading Vosk Speech Recognition Model")
    print("=" * 60)
    
    models_dir = Path("models")
    model_name = "vosk-model-small-en-us-0.15"
    model_path = models_dir / model_name
    
    # Check if already exists
    if model_path.exists():
        print(f"✓ Vosk model already exists at {model_path}")
        return True
    
    # Download model
    model_url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    archive_path = models_dir / f"{model_name}.zip"
    
    if not download_file(model_url, archive_path, "Vosk model"):
        return False
    
    # Extract
    if not extract_archive(archive_path, models_dir):
        return False
    
    # Clean up archive
    try:
        archive_path.unlink()
        print(f"✓ Cleaned up archive file")
    except Exception as e:
        print(f"⚠ Warning: Could not delete archive: {e}")
    
    print(f"\n✓ Vosk model installed at {model_path}")
    return True


def setup_resemblyzer() -> bool:
    """Setup Resemblyzer for voice authentication"""
    print("\n" + "=" * 60)
    print("Setting up Resemblyzer Voice Authentication")
    print("=" * 60)
    
    try:
        # Try to import resemblyzer
        import resemblyzer
        print("✓ Resemblyzer already installed")
        
        # Test if model can be loaded
        from resemblyzer import VoiceEncoder
        encoder = VoiceEncoder()
        print("✓ Resemblyzer model loaded successfully")
        return True
        
    except ImportError:
        print("⚠ Resemblyzer not installed")
        print("\nTo enable voice authentication, install resemblyzer:")
        print("  pip install resemblyzer")
        print("\nNote: Voice authentication will be disabled without it")
        return False
    except Exception as e:
        print(f"⚠ Resemblyzer installed but model loading failed: {e}")
        print("Voice authentication may not work properly")
        return False


def create_config_files() -> bool:
    """Create necessary configuration files"""
    print("\n" + "=" * 60)
    print("Creating Configuration Files")
    print("=" * 60)
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Create commands.json if not exists
    commands_file = config_dir / "commands.json"
    if not commands_file.exists():
        import json
        default_commands = {
            "system": {
                "shutdown": ["shutdown", "shut down", "power off"],
                "restart": ["restart", "reboot"],
                "sleep": ["sleep", "hibernate"],
                "lock": ["lock", "lock screen", "lock computer"]
            },
            "application": {
                "open": ["open", "launch", "start", "run"],
                "close": ["close", "exit", "quit", "terminate"],
                "minimize": ["minimize", "minimise"],
                "maximize": ["maximize", "maximise", "full screen"]
            },
            "file": {
                "open_file": ["open file", "show file"],
                "create_file": ["create file", "new file", "make file"],
                "delete_file": ["delete file", "remove file"],
                "list_files": ["list files", "show files"]
            },
            "web": {
                "open_website": ["open website", "open site", "go to", "navigate to"],
                "search_google": ["search google", "google search", "search"],
                "search_youtube": ["search youtube", "youtube search"]
            },
            "system_info": {
                "system_info": ["system info", "system information"],
                "battery": ["battery", "battery status"],
                "disk_space": ["disk space", "storage"],
                "memory": ["memory", "ram", "memory usage"],
                "cpu": ["cpu", "processor", "cpu usage"],
                "network": ["network", "network status", "wifi"]
            },
            "volume": {
                "volume_up": ["volume up", "increase volume", "louder"],
                "volume_down": ["volume down", "decrease volume", "quieter"],
                "mute": ["mute", "silence"]
            },
            "control": {
                "stop_listening": ["stop", "sleep", "go to sleep", "stop listening"],
                "wake_up": ["wake up", "start listening", "resume", "hello echo"]
            }
        }
        commands_file.write_text(json.dumps(default_commands, indent=2))
        print(f"✓ Created {commands_file}")
    
    # Create apps.json
    apps_file = config_dir / "apps.json"
    if not apps_file.exists():
        import json
        apps_file.write_text(json.dumps({"apps": []}, indent=2))
        print(f"✓ Created {apps_file}")
    
    # Create user database
    import pickle
    users_file = config_dir / "users.pkl"
    if not users_file.exists():
        with open(users_file, "wb") as f:
            pickle.dump({}, f)
        print(f"✓ Created {users_file}")
    
    # Create sessions database
    sessions_file = config_dir / "sessions.pkl"
    if not sessions_file.exists():
        with open(sessions_file, "wb") as f:
            pickle.dump({}, f)
        print(f"✓ Created {sessions_file}")
    
    print("\n✓ Configuration files created successfully")
    return True


def main():
    """Main setup function"""
    print("=" * 60)
    print("🎙️  EchoOS Model & Configuration Setup")
    print("=" * 60)
    
    success = True
    
    # Download Vosk model
    if not download_vosk_model():
        print("\n✗ Failed to download Vosk model")
        success = False
    
    # Setup Resemblyzer (optional)
    setup_resemblyzer()
    
    # Create config files
    if not create_config_files():
        print("\n✗ Failed to create configuration files")
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ Setup completed successfully!")
        print("\nYou can now run EchoOS:")
        print("  python run.py")
    else:
        print("⚠ Setup completed with warnings")
        print("\nSome components may not work properly")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
