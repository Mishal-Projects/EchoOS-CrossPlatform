#!/usr/bin/env python3
"""
EchoOS Launcher Script
Performs pre-flight checks and launches EchoOS
"""

import sys
import os
import subprocess
from pathlib import Path
import json
import pickle


def print_header():
    """Print application header"""
    print("=" * 60)
    print("🎙️  EchoOS - Voice-Controlled Operating System")
    print("=" * 60)
    print()


def check_python_version():
    """Check Python version"""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro}")
        print("  Error: Python 3.8 or higher required")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...", end=" ")
    
    required_packages = [
        'PySide6',
        'vosk',
        'resemblyzer',
        'pyttsx3',
        'sounddevice',
        'numpy',
        'psutil',
        'rapidfuzz',
        'cryptography'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if not missing:
        print("✓ All dependencies installed")
        return True
    else:
        print(f"✗ Missing: {', '.join(missing)}")
        print()
        print("  Install missing dependencies:")
        print("  pip install -r requirements.txt")
        return False


def check_vosk_model():
    """Check if Vosk model is downloaded"""
    print("Checking Vosk model...", end=" ")
    
    models_dir = Path("models")
    if not models_dir.exists():
        print("✗ Models directory not found")
        print()
        print("  Download Vosk model:")
        print("  python scripts/download_vosk_model.py")
        return False
    
    # Check for any vosk model
    model_found = False
    for item in models_dir.iterdir():
        if item.is_dir() and item.name.startswith('vosk-model'):
            model_found = True
            print(f"✓ {item.name}")
            break
    
    if not model_found:
        print("✗ No Vosk model found")
        print()
        print("  Download Vosk model:")
        print("  python scripts/download_vosk_model.py")
        return False
    
    return True


def check_config():
    """Check if configuration files exist"""
    print("Checking configuration...", end=" ")
    
    config_dir = Path("config")
    if not config_dir.exists():
        print("✗ Config directory not found")
        print()
        print("  Setup configuration:")
        print("  python scripts/setup_config.py")
        return False
    
    required_files = [
        'commands.json',
        'apps.json',
        'users.pkl',
        'sessions.pkl'
    ]
    
    missing = []
    for filename in required_files:
        if not (config_dir / filename).exists():
            missing.append(filename)
    
    if not missing:
        print("✓ Configuration ready")
        return True
    else:
        print(f"✗ Missing: {', '.join(missing)}")
        print()
        print("  Setup configuration:")
        print("  python scripts/setup_config.py")
        return False


def check_microphone():
    """Check if microphone is available"""
    print("Checking microphone...", end=" ")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        # Check for input devices
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        
        if input_devices:
            print(f"✓ {len(input_devices)} input device(s) found")
            return True
        else:
            print("✗ No input devices found")
            print()
            print("  Please connect a microphone")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def setup_first_time():
    """Run first-time setup"""
    print()
    print("=" * 60)
    print("First-Time Setup Required")
    print("=" * 60)
    print()
    
    response = input("Run setup now? (y/n): ").lower()
    if response != 'y':
        print("Setup cancelled. Run manually:")
        print("  python scripts/setup_config.py")
        print("  python scripts/download_vosk_model.py")
        return False
    
    print()
    print("Running setup...")
    print()
    
    # Setup configuration
    print("1. Setting up configuration...")
    result = subprocess.run([sys.executable, "scripts/setup_config.py"])
    if result.returncode != 0:
        print("Configuration setup failed")
        return False
    
    print()
    
    # Download Vosk model
    print("2. Downloading Vosk model...")
    result = subprocess.run([sys.executable, "scripts/download_vosk_model.py"])
    if result.returncode != 0:
        print("Model download failed")
        return False
    
    print()
    print("=" * 60)
    print("✓ Setup complete!")
    print("=" * 60)
    print()
    
    return True


def run_echoos():
    """Launch EchoOS"""
    print()
    print("=" * 60)
    print("Launching EchoOS...")
    print("=" * 60)
    print()
    
    try:
        # Import and run main
        from main import main
        main()
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("EchoOS stopped by user")
        print("=" * 60)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"Error: {e}")
        print("=" * 60)
        print()
        print("Check echoos.log for details")
        return False
    
    return True


def main():
    """Main launcher function"""
    print_header()
    
    # Run pre-flight checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Vosk Model", check_vosk_model),
        ("Configuration", check_config),
        ("Microphone", check_microphone)
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    print()
    
    if not all_passed:
        print("=" * 60)
        print("⚠️  Pre-flight checks failed")
        print("=" * 60)
        print()
        
        # Offer to run setup if config/model missing
        if not Path("config").exists() or not Path("models").exists():
            if setup_first_time():
                # Re-run checks
                print()
                print("Re-running checks...")
                print()
                all_passed = all([check() for _, check in checks])
            else:
                return 1
        else:
            print("Please fix the issues above and try again")
            return 1
    
    if all_passed:
        print("=" * 60)
        print("✓ All checks passed")
        print("=" * 60)
        
        # Launch EchoOS
        if not run_echoos():
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
