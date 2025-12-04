# 🎤 Audio Troubleshooting Guide

## Problem: Registration/Authentication Failed

If you're seeing "Registration failed" or "Authentication failed" errors, it's likely an audio issue.

---

## Quick Fix (Run This First!)

```bash
python scripts/fix_audio.py
```

This script will:
1. ✅ Check if microphone is detected
2. ✅ Test microphone recording
3. ✅ Analyze audio levels
4. ✅ Provide specific solutions

---

## Common Issues & Solutions

### Issue 1: No Audio Detected

**Symptoms:**
- "No audio detected" error
- "Registration failed" immediately
- Max audio level: 0.000

**Solutions:**

#### Windows:
1. **Check Microphone Connection**
   - Ensure microphone is plugged in
   - Try a different USB port
   - Check if microphone LED is on

2. **Grant Permissions**
   - Open Settings > Privacy > Microphone
   - Enable "Allow apps to access microphone"
   - Enable "Allow desktop apps to access microphone"

3. **Set Default Device**
   - Right-click speaker icon in taskbar
   - Select "Sounds"
   - Go to "Recording" tab
   - Right-click your microphone
   - Select "Set as Default Device"

4. **Unmute Microphone**
   - Right-click speaker icon
   - Select "Open Sound settings"
   - Click "Sound Control Panel"
   - Recording tab > Right-click microphone > Properties
   - Levels tab > Ensure not muted and volume > 50%

#### macOS:
1. **Grant Permissions**
   - System Preferences > Security & Privacy
   - Privacy tab > Microphone
   - Check the box next to Terminal/Python

2. **Check Input Device**
   - System Preferences > Sound
   - Input tab
   - Select your microphone
   - Speak and watch input level bars

3. **Increase Input Volume**
   - System Preferences > Sound > Input
   - Drag "Input volume" slider to right

#### Linux:
1. **Check PulseAudio**
   ```bash
   pactl list sources
   ```

2. **Unmute Microphone**
   ```bash
   pactl set-source-mute @DEFAULT_SOURCE@ 0
   ```

3. **Set Volume**
   ```bash
   pactl set-source-volume @DEFAULT_SOURCE@ 80%
   ```

4. **Check ALSA**
   ```bash
   alsamixer
   ```
   - Press F4 to show capture devices
   - Use arrow keys to adjust levels
   - Press M to unmute

---

### Issue 2: Audio Levels Too Low

**Symptoms:**
- "Audio levels very low" warning
- Authentication fails with low similarity
- Max audio level: < 0.01

**Solutions:**

1. **Speak Louder**
   - Speak clearly and loudly
   - Don't whisper

2. **Move Closer**
   - Position microphone 6-12 inches from mouth
   - Reduce distance to microphone

3. **Increase Microphone Volume**
   - **Windows**: Sound settings > Input > Device properties > Volume slider
   - **macOS**: System Preferences > Sound > Input > Input volume
   - **Linux**: `alsamixer` or PulseAudio Volume Control

4. **Boost Microphone**
   - **Windows**: Sound settings > Input > Device properties > Additional device properties > Levels > Microphone Boost
   - Set to +10dB or +20dB

5. **Reduce Background Noise**
   - Close windows
   - Turn off fans/AC
   - Move to quieter room

---

### Issue 3: Wrong Microphone Selected

**Symptoms:**
- Built-in mic works but headset doesn't
- No audio when using specific microphone

**Solutions:**

1. **Check Default Device**
   ```bash
   python scripts/fix_audio.py
   ```
   - Select option to set default device

2. **Manual Selection (Windows)**
   - Settings > System > Sound
   - Input > Choose your input device
   - Select correct microphone

3. **Manual Selection (macOS)**
   - System Preferences > Sound > Input
   - Select correct microphone from list

4. **Test Each Device**
   ```bash
   python scripts/test_microphone.py
   ```

---

### Issue 4: Resemblyzer Not Available

**Symptoms:**
- "Voice authentication not available"
- "Resemblyzer not available" in logs

**Solutions:**

1. **Install Resemblyzer**
   ```bash
   pip install resemblyzer
   ```

2. **Install Dependencies**
   ```bash
   pip install torch
   pip install numpy
   ```

3. **Verify Installation**
   ```python
   python -c "from resemblyzer import VoiceEncoder; print('OK')"
   ```

4. **Use Password Authentication (Alternative)**
   - Modify code to use password instead of voice
   - See `modules/auth.py` for password auth

---

### Issue 5: Audio Clipping (Too Loud)

**Symptoms:**
- "Audio levels very high" warning
- Distorted audio
- Max audio level: > 0.9

**Solutions:**

1. **Speak Softer**
   - Use normal speaking voice
   - Don't shout

2. **Move Away**
   - Increase distance from microphone
   - Position 12-18 inches away

3. **Reduce Microphone Volume**
   - Lower input volume in system settings
   - Disable microphone boost

---

## Step-by-Step Diagnosis

### Step 1: Run Audio Troubleshooter
```bash
python scripts/fix_audio.py
```

### Step 2: Check Output
- ✅ **"Audio levels are good"** → Proceed to registration
- ⚠️ **"Audio levels very low"** → Increase volume, speak louder
- ❌ **"No audio detected"** → Check permissions and connections

### Step 3: Test Microphone
```bash
python scripts/test_microphone.py
```

### Step 4: Try Registration Again
```bash
python main_enhanced.py
```

---

## Testing Commands

### Test Microphone
```bash
python scripts/test_microphone.py
```

### Fix Audio Issues
```bash
python scripts/fix_audio.py
```

### Check Devices
```python
import sounddevice as sd
print(sd.query_devices())
```

### Test Recording
```python
import sounddevice as sd
import numpy as np

# Record 3 seconds
recording = sd.rec(48000, samplerate=16000, channels=1, dtype='float32')
sd.wait()

# Check levels
print(f"Max: {np.max(np.abs(recording))}")
print(f"Avg: {np.mean(np.abs(recording))}")
```

---

## Expected Audio Levels

| Level | Max Value | Status |
|-------|-----------|--------|
| **Silent** | < 0.001 | ❌ No audio |
| **Too Low** | 0.001 - 0.01 | ⚠️ Increase volume |
| **Good** | 0.01 - 0.5 | ✅ Perfect |
| **High** | 0.5 - 0.9 | ✅ OK |
| **Clipping** | > 0.9 | ⚠️ Reduce volume |

---

## Platform-Specific Notes

### Windows
- **Default Sample Rate**: 48000 Hz (will be resampled to 16000 Hz)
- **Permissions**: Required for desktop apps
- **Best Practice**: Use USB microphone or headset

### macOS
- **Permissions**: Must grant in System Preferences
- **Restart Required**: After granting permissions
- **Best Practice**: Use built-in mic or USB device

### Linux
- **Audio System**: PulseAudio or ALSA
- **Permissions**: Usually not required
- **Best Practice**: Check `pavucontrol` for device selection

---

## Still Having Issues?

### 1. Check Logs
```bash
cat echoos.log | grep -i "audio\|microphone\|recording"
```

### 2. Verify Dependencies
```bash
pip list | grep -i "sounddevice\|numpy\|resemblyzer"
```

### 3. Test with Different Microphone
- Try built-in microphone
- Try USB microphone
- Try headset microphone

### 4. Restart Application
```bash
# Close EchoOS
# Restart
python main_enhanced.py
```

### 5. Restart Computer
- Sometimes audio drivers need restart
- Especially after granting permissions

---

## Success Checklist

Before trying registration again:

- [ ] Microphone is connected and detected
- [ ] Microphone permissions granted
- [ ] Correct microphone selected as default
- [ ] Microphone is not muted
- [ ] Microphone volume > 50%
- [ ] `python scripts/fix_audio.py` shows "Audio levels are good"
- [ ] Background noise is minimal
- [ ] You can speak clearly for 5 seconds

---

## Quick Reference

### Good Audio Setup:
```
✅ Microphone connected
✅ Permissions granted
✅ Volume 50-80%
✅ Not muted
✅ Quiet environment
✅ 6-12 inches from mic
✅ Clear speech
```

### Registration Process:
```
1. Click "Register New User"
2. Enter username
3. Wait for "RECORDING NOW"
4. Speak clearly for 5 seconds
5. Wait for "Recording complete"
6. See "User registered successfully"
```

### If Registration Fails:
```
1. Run: python scripts/fix_audio.py
2. Fix any issues found
3. Try registration again
4. If still fails, check logs
```

---

## Contact Support

If none of these solutions work:

1. **Check Logs**: `echoos.log`
2. **Run Diagnostics**: `python scripts/fix_audio.py`
3. **Create Issue**: Include log output and diagnostic results
4. **GitHub**: https://github.com/Mishal-Projects/EchoOS-CrossPlatform/issues

---

**Last Updated**: December 2025  
**Version**: 2.1 Enhanced
