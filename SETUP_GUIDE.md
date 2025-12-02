# 🚀 EchoOS Complete Setup Guide

This guide will help you set up EchoOS without any errors.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB free space
- **Microphone**: Required for voice commands

### Check Python Version
```bash
python --version
# or
python3 --version
```

If Python is not installed or version is < 3.8:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

---

## 🔧 Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

#### Core Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Platform-Specific Notes

**Windows:**
- No additional steps needed

**macOS:**
```bash
# Install PortAudio for audio support
brew install portaudio

# PyObjC frameworks install automatically
```

**Linux (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-dev portaudio19-dev libportaudio2 \
    libportaudiocpp0 ffmpeg libsndfile1

# For accessibility features
sudo apt install -y python3-tk python3-dev
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install -y python3-devel portaudio-devel \
    ffmpeg libsndfile
```

### Step 4: Download Models and Setup Configuration
```bash
python scripts/download_models.py
```

This will:
- Download Vosk speech recognition model (~40MB)
- Create configuration files
- Set up user database
- Check for optional dependencies

**Note**: If download fails, manually download from:
- Vosk Model: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
- Extract to `models/` directory

### Step 5: Verify Installation
```bash
python run.py
```

This will run pre-flight checks and launch EchoOS if everything is ready.

---

## 🎯 Quick Start (Automated)

For a fully automated setup:

```bash
# Clone and enter directory
git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform

# Run automated setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python scripts/download_models.py

# Launch
python run.py
```

---

## 🔍 Troubleshooting

### Issue: "No module named 'PySide6'"
**Solution:**
```bash
pip install PySide6
```

### Issue: "Vosk model not found"
**Solution:**
```bash
python scripts/download_models.py
```

Or manually:
1. Download: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
2. Extract to `models/vosk-model-small-en-us-0.15/`

### Issue: "No input devices found"
**Solution:**
- Check microphone is connected
- Grant microphone permissions to terminal/Python
- **macOS**: System Preferences → Security & Privacy → Microphone
- **Windows**: Settings → Privacy → Microphone

### Issue: "PortAudio library not found"
**Solution:**

**macOS:**
```bash
brew install portaudio
```

**Linux:**
```bash
sudo apt install portaudio19-dev
```

**Windows:**
- Usually not needed, but if error persists:
```bash
pip install --upgrade sounddevice
```

### Issue: "Voice authentication not working"
**Solution:**

Voice authentication requires Resemblyzer (optional). If not installed, EchoOS falls back to password authentication.

To enable voice auth:
```bash
pip install resemblyzer
```

**Note**: Resemblyzer requires additional dependencies and may take time to install.

### Issue: "Permission denied" for system commands
**Solution:**

Some system commands (shutdown, restart) require administrator privileges:

**Windows**: Run terminal as Administrator

**macOS/Linux**: Commands will prompt for password when needed

### Issue: "CI/CD tests failing"
**Solution:**

For development:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest tests/ -v
```

---

## 🎤 First Run

### 1. Launch EchoOS
```bash
python run.py
```

### 2. Register User

**With Voice Authentication (if Resemblyzer installed):**
- Click "Register" in the GUI
- Enter username
- Speak clearly for 5 seconds when prompted
- User registered with voice biometrics

**With Password Authentication (fallback):**
- Click "Register"
- Enter username and password
- User registered with password

### 3. Authenticate
- Click "Login"
- Speak (voice auth) or enter password
- Start using voice commands!

### 4. Test Voice Commands

Try these commands:
- "Open Chrome"
- "What's the battery status?"
- "Search Google for Python tutorials"
- "System information"
- "Volume up"

---

## 📦 Optional Features

### Voice Authentication (Resemblyzer)
```bash
pip install resemblyzer
```

**Benefits:**
- Biometric voice authentication
- No passwords needed
- More secure

**Note**: Large download (~200MB) and requires additional dependencies.

### Development Tools
```bash
pip install -r requirements-dev.txt
```

Includes:
- pytest (testing)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)

---

## 🖥️ Platform-Specific Features

### Windows
- Full system control (shutdown, restart, sleep, lock)
- Volume control (requires nircmd - optional)
- Native application launching

### macOS
- System control via AppleScript
- Native volume control
- Application launching via `open -a`

### Linux
- Systemd integration for system control
- Multiple desktop environment support
- XDG standards compliance

---

## 🔐 Security Notes

1. **Voice Samples**: Stored locally in `config/users.pkl`
2. **Sessions**: Encrypted with Fernet encryption
3. **No Cloud**: All processing happens offline
4. **Permissions**: Grant only necessary permissions

---

## 📊 Performance Tips

1. **Use SSD**: Faster model loading
2. **Close Background Apps**: Better speech recognition
3. **Good Microphone**: Improves accuracy
4. **Quiet Environment**: Reduces noise interference

---

## 🆘 Getting Help

### Check Logs
```bash
cat echoos.log
```

### Run Diagnostics
```bash
python scripts/test_microphone.py
```

### Report Issues
- GitHub Issues: https://github.com/Mishal-Projects/EchoOS-CrossPlatform/issues
- Include:
  - OS and Python version
  - Error message
  - echoos.log file

---

## 🎓 Next Steps

1. **Read User Manual**: `docs/USER_MANUAL.md`
2. **Explore Commands**: `config/commands.json`
3. **Customize**: Edit configuration files
4. **Contribute**: See `CONTRIBUTING.md`

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip list`)
- [ ] Vosk model downloaded (check `models/` directory)
- [ ] Configuration files exist (check `config/` directory)
- [ ] Microphone connected and working
- [ ] Microphone permissions granted
- [ ] Virtual environment activated (if using)
- [ ] Latest code pulled from repository

---

## 🚀 You're Ready!

If all checks pass, you're ready to use EchoOS!

```bash
python run.py
```

Enjoy voice-controlled computing! 🎙️
