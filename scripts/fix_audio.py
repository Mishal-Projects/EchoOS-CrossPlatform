#!/usr/bin/env python3
"""
Audio Troubleshooting and Fix Script
Diagnoses and fixes common audio issues
"""

import sys
import sounddevice as sd
import numpy as np

def check_audio_devices():
    """Check available audio devices"""
    print("\n" + "="*60)
    print("CHECKING AUDIO DEVICES")
    print("="*60)
    
    try:
        devices = sd.query_devices()
        
        if not devices:
            print("❌ No audio devices found!")
            return False
        
        print(f"\n✅ Found {len(devices)} audio device(s):\n")
        
        input_devices = []
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append((i, device))
                print(f"  [{i}] {device['name']}")
                print(f"      Input Channels: {device['max_input_channels']}")
                print(f"      Sample Rate: {device['default_samplerate']} Hz")
                
                # Check if it's the default
                try:
                    default_input = sd.query_devices(kind='input')
                    if device['name'] == default_input['name']:
                        print(f"      ⭐ DEFAULT INPUT DEVICE")
                except:
                    pass
                print()
        
        if not input_devices:
            print("❌ No input devices (microphones) found!")
            return False
        
        print(f"✅ Found {len(input_devices)} input device(s)")
        return True
        
    except Exception as e:
        print(f"❌ Error checking devices: {e}")
        return False


def test_microphone(duration=3):
    """Test microphone recording"""
    print("\n" + "="*60)
    print("TESTING MICROPHONE")
    print("="*60)
    
    try:
        print(f"\n🎤 Recording for {duration} seconds...")
        print("   Please speak into your microphone NOW!")
        print()
        
        sample_rate = 16000
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32',
            blocking=False
        )
        
        # Progress indicator
        import time
        for i in range(duration):
            time.sleep(1)
            print(f"   Recording... {i+1}/{duration} seconds")
        
        sd.wait()
        
        # Analyze audio
        audio_data = np.abs(recording.flatten())
        max_level = np.max(audio_data)
        avg_level = np.mean(audio_data)
        
        print("\n" + "="*60)
        print("AUDIO ANALYSIS")
        print("="*60)
        print(f"\n  Max Level: {max_level:.6f}")
        print(f"  Avg Level: {avg_level:.6f}")
        print()
        
        # Diagnosis
        if max_level < 0.001:
            print("❌ CRITICAL: No audio detected!")
            print("\n   Possible issues:")
            print("   1. Microphone is not connected")
            print("   2. Microphone is muted")
            print("   3. Wrong microphone selected")
            print("   4. Microphone permissions denied")
            print("\n   Solutions:")
            print("   • Check microphone connection")
            print("   • Unmute microphone in system settings")
            print("   • Grant microphone permissions to Python")
            print("   • Select correct default microphone")
            return False
            
        elif max_level < 0.01:
            print("⚠️  WARNING: Audio levels very low")
            print("\n   Recommendations:")
            print("   • Speak louder")
            print("   • Move closer to microphone")
            print("   • Increase microphone volume in system settings")
            print("   • Check microphone gain settings")
            return True
            
        elif max_level > 0.9:
            print("⚠️  WARNING: Audio levels very high (clipping)")
            print("\n   Recommendations:")
            print("   • Speak softer")
            print("   • Move away from microphone")
            print("   • Reduce microphone volume in system settings")
            return True
            
        else:
            print("✅ EXCELLENT: Audio levels are good!")
            print("\n   Your microphone is working correctly.")
            return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to test microphone")
        print(f"   Error: {e}")
        return False


def set_default_device():
    """Help user set default audio device"""
    print("\n" + "="*60)
    print("SET DEFAULT AUDIO DEVICE")
    print("="*60)
    
    try:
        devices = sd.query_devices()
        input_devices = [(i, d) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
        
        if not input_devices:
            print("\n❌ No input devices found!")
            return False
        
        print("\nAvailable input devices:")
        for idx, (i, device) in enumerate(input_devices):
            print(f"  {idx + 1}. {device['name']}")
        
        try:
            choice = int(input("\nSelect device number (or 0 to skip): "))
            if choice == 0:
                return True
            
            if 1 <= choice <= len(input_devices):
                device_id = input_devices[choice - 1][0]
                sd.default.device = device_id
                print(f"\n✅ Default device set to: {input_devices[choice - 1][1]['name']}")
                return True
            else:
                print("\n❌ Invalid choice")
                return False
                
        except ValueError:
            print("\n❌ Invalid input")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def check_permissions():
    """Check microphone permissions"""
    print("\n" + "="*60)
    print("CHECKING PERMISSIONS")
    print("="*60)
    
    print("\n📋 Microphone Permission Checklist:")
    print()
    
    import platform
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("  macOS Permissions:")
        print("  1. Open System Preferences > Security & Privacy")
        print("  2. Click 'Privacy' tab")
        print("  3. Select 'Microphone' from left sidebar")
        print("  4. Ensure Python/Terminal is checked")
        print()
        
    elif system == "Windows":
        print("  Windows Permissions:")
        print("  1. Open Settings > Privacy > Microphone")
        print("  2. Ensure 'Allow apps to access microphone' is ON")
        print("  3. Ensure 'Allow desktop apps to access microphone' is ON")
        print()
        
    elif system == "Linux":
        print("  Linux Permissions:")
        print("  1. Check PulseAudio/ALSA settings")
        print("  2. Run: pactl list sources")
        print("  3. Ensure microphone is not muted")
        print()
    
    print("  ✅ After granting permissions, restart this script")


def main():
    """Main troubleshooting function"""
    print("\n" + "="*70)
    print(" "*20 + "ECHOOS AUDIO TROUBLESHOOTER")
    print("="*70)
    
    # Step 1: Check devices
    if not check_audio_devices():
        print("\n❌ FAILED: No audio devices found")
        check_permissions()
        return 1
    
    # Step 2: Test microphone
    if not test_microphone():
        print("\n❌ FAILED: Microphone test failed")
        check_permissions()
        
        # Offer to set default device
        print("\n" + "="*60)
        try:
            choice = input("\nWould you like to select a different microphone? (y/n): ")
            if choice.lower() == 'y':
                set_default_device()
                print("\nPlease run this script again to test the new device.")
        except:
            pass
        
        return 1
    
    # Success
    print("\n" + "="*70)
    print("✅ SUCCESS: Audio system is working correctly!")
    print("="*70)
    print("\nYou can now use EchoOS voice features:")
    print("  • Voice registration")
    print("  • Voice authentication")
    print("  • Voice commands")
    print("\nRun: python main_enhanced.py")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
