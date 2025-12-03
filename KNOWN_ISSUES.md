# Known Issues & Solutions

## 🐛 Known Issues

### 1. PyAudio Installation Failure

**Issue**: `pip install pyaudio` fails on Windows/macOS

**Solution**:
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### 2. Vosk Model Not Found

**Issue**: "Vosk model not found" error on startup

**Solution**:
```bash
python scripts/download_vosk_model.py
```

Ensure model is in: `models/vosk-model-small-en-us-0.15/`

### 3. Microphone Not Detected

**Issue**: No audio input detected

**Solution**:
- **Windows**: Settings → Privacy → Microphone → Enable
- **macOS**: System Preferences → Security & Privacy → Microphone → Grant permission
- Check default input device in system settings

### 4. Resemblyzer Installation Issues

**Issue**: Resemblyzer fails to install

**Solution**:
```bash
# Install from source
pip install git+https://github.com/resemble-ai/Resemblyzer.git
```

### 5. Volume Control Not Working

**Issue**: Volume commands don't work

**Solution**:
- **Windows**: Install [NirCmd](https://www.nirsoft.net/utils/nircmd.html)
- **macOS**: Should work out of box
- **Linux**: Install `alsa-utils`

### 6. Import Error: ConfigManager

**Issue**: `ConfigManager` imported but not used

**Solution**: This is harmless, but can be removed from `main.py` line 28

### 7. GUI Not Showing

**Issue**: Window doesn't appear

**Solution**:
```bash
# Reinstall PySide6
pip uninstall PySide6
pip install PySide6
```

### 8. Authentication Always Fails

**Issue**: Voice authentication never succeeds

**Solution**:
- Re-register in quiet environment
- Speak naturally, not too loud/soft
- Lower threshold in code: `threshold=0.65` instead of `0.75`

### 9. Commands Not Recognized

**Issue**: Voice commands not working

**Solution**:
- Speak clearly and at normal pace
- Check `config/commands.json` for exact phrases
- Try manual command input first
- Reduce background noise

### 10. High Memory Usage

**Issue**: Application uses too much RAM

**Solution**:
- Normal: 315MB is expected
- Close other applications
- Use smaller Vosk model (already using small)

---

## ⚡ Quick Fixes

### Fix 1: Update requirements.txt for better compatibility

Add version constraints:
```txt
PySide6>=6.5.0,<7.0.0
vosk>=0.3.45,<0.4.0
```

### Fix 2: Add fallback for missing dependencies

The code already handles optional dependencies gracefully:
- PyAutoGUI (accessibility)
- PyTesseract (screen reading)

### Fix 3: Improve error messages

All modules have try-except blocks with logging.

---

## 🔧 Pre-Run Checklist

Before running `python main.py`:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Vosk model downloaded (run download script)
- [ ] Microphone connected and working
- [ ] Microphone permissions granted
- [ ] Audio drivers up to date

---

## 🆘 Troubleshooting Steps

### If application won't start:

1. Check `echoos.log` for errors
2. Verify Python version: `python --version`
3. Verify dependencies: `pip list`
4. Test microphone: `python -m sounddevice`
5. Run in verbose mode: `python main.py --verbose`

### If voice recognition fails:

1. Test microphone in system settings
2. Check microphone is default input
3. Reduce background noise
4. Try manual command input
5. Check Vosk model exists

### If authentication fails:

1. Delete `config/users.pkl`
2. Re-register user
3. Speak naturally during registration
4. Lower similarity threshold in code

---

## 📝 Reporting Issues

If you encounter issues:

1. Check this document first
2. Review `echoos.log`
3. Try solutions above
4. Open GitHub issue with:
   - OS and version
   - Python version
   - Error message
   - Log file contents
   - Steps to reproduce

---

## ✅ Verified Working On

- ✅ Windows 10/11
- ✅ macOS Monterey/Ventura
- ⚠️ Linux (Ubuntu 20.04+) - Requires additional setup

---

Last Updated: December 2, 2025
