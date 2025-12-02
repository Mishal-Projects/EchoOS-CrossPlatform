"""
Microphone Testing Utility
Tests microphone input and audio levels
"""

import sounddevice as sd
import numpy as np
import sys


def list_audio_devices():
    """List all available audio devices"""
    print("=" * 60)
    print("Available Audio Devices")
    print("=" * 60)
    print()
    
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")
        print(f"  Max Input Channels: {device['max_input_channels']}")
        print(f"  Max Output Channels: {device['max_output_channels']}")
        print(f"  Default Sample Rate: {device['default_samplerate']}")
        print()


def test_microphone(duration=5):
    """Test microphone input"""
    print("=" * 60)
    print("Microphone Test")
    print("=" * 60)
    print()
    print(f"Recording for {duration} seconds...")
    print("Speak into your microphone!")
    print()
    
    try:
        # Record audio
        sample_rate = 16000
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        
        # Analyze audio levels
        audio_data = np.abs(recording.flatten())
        max_level = np.max(audio_data)
        avg_level = np.mean(audio_data)
        
        print("Recording complete!")
        print()
        print("Audio Analysis:")
        print(f"  Max Level: {max_level}")
        print(f"  Average Level: {avg_level:.2f}")
        print()
        
        if max_level < 100:
            print("⚠️  Warning: Audio levels are very low!")
            print("   Check your microphone volume settings.")
        elif max_level > 30000:
            print("⚠️  Warning: Audio levels are very high!")
            print("   Consider reducing microphone gain.")
        else:
            print("✓ Audio levels look good!")
        
        print()
        
    except Exception as e:
        print(f"❌ Error testing microphone: {e}")
        sys.exit(1)


def main():
    """Main function"""
    print()
    print("EchoOS Microphone Testing Utility")
    print()
    
    # List devices
    list_audio_devices()
    
    # Test microphone
    try:
        duration = int(input("Enter test duration in seconds (default 5): ") or "5")
    except ValueError:
        duration = 5
    
    test_microphone(duration)
    
    print("=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
