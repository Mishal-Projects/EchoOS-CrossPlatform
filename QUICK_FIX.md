# 🚨 Quick Fix: Registration/Authentication Failed

## Problem
You're seeing:
- ❌ "Registration failed"
- ❌ "Authentication failed"
- ❌ "No audio detected"

## Solution (30 seconds)

### Step 1: Run This Command
```bash
python scripts/fix_audio.py
```

### Step 2: Follow the Instructions
The script will:
1. Check your microphone
2. Test audio recording
3. Tell you exactly what's wrong
4. Provide specific solutions

### Step 3: Common Quick Fixes

#### If "No audio detected":
**Windows:**
```
Settings > Privacy > Microphone > Allow apps to access microphone: ON
```

**macOS:**
```
System Preferences > Security & Privacy > Privacy > Microphone > Check Python/Terminal
```

**Linux:**
```bash
pactl set-source-mute @DEFAULT_SOURCE@ 0
```

#### If "Audio levels very low":
1. Speak LOUDER
2. Move closer to microphone (6-12 inches)
3. Increase microphone volume in system settings

#### If "Wrong microphone":
1. Check which microphone is default
2. Select correct microphone in system settings
3. Restart EchoOS

---

## Still Not Working?

### Check These:
- [ ] Microphone is plugged in
- [ ] Microphone is not muted
- [ ] Microphone permissions granted
- [ ] Correct microphone selected
- [ ] Volume > 50%

### Run Full Diagnostics:
```bash
python scripts/test_microphone.py
```

### Read Full Guide:
See [AUDIO_TROUBLESHOOTING.md](AUDIO_TROUBLESHOOTING.md)

---

## Expected Behavior

### Registration:
```
1. Click "Register New User"
2. Enter username
3. See "RECORDING IN 2 SECONDS..."
4. See "RECORDING NOW - SPEAK!"
5. Speak clearly for 5 seconds
6. See "Recording complete!"
7. See "User registered successfully!"
```

### If You See:
- ❌ "No audio detected" → Run `python scripts/fix_audio.py`
- ⚠️ "Audio levels very low" → Speak louder or increase volume
- ✅ "User registered successfully" → You're good to go!

---

## Quick Test

Test your microphone right now:
```bash
python scripts/fix_audio.py
```

If it says "Audio levels are good", try registration again!

---

**Need more help?** See [AUDIO_TROUBLESHOOTING.md](AUDIO_TROUBLESHOOTING.md)
