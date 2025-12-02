"""
Configuration Setup Utility
Creates initial configuration files and directories
"""

import json
import pickle
from pathlib import Path


def setup_directories():
    """Create necessary directories"""
    directories = ['config', 'models', 'logs']
    
    print("Creating directories...")
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        print(f"  ✓ {directory}/")


def setup_commands_config():
    """Create default commands configuration"""
    commands = {
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
        "accessibility": {
            "read_screen": ["read screen", "read text"],
            "navigate": ["navigate", "move"],
            "click": ["click", "select"],
            "scroll_up": ["scroll up"],
            "scroll_down": ["scroll down"],
            "zoom_in": ["zoom in", "magnify"],
            "zoom_out": ["zoom out", "shrink"]
        },
        "control": {
            "stop_listening": ["stop", "sleep", "go to sleep", "stop listening"],
            "wake_up": ["wake up", "start listening", "resume", "hello echo"]
        }
    }
    
    config_file = Path("config/commands.json")
    with open(config_file, 'w') as f:
        json.dump(commands, f, indent=2)
    
    print(f"  ✓ {config_file}")


def setup_apps_config():
    """Create empty apps configuration"""
    apps = {"apps": []}
    
    config_file = Path("config/apps.json")
    with open(config_file, 'w') as f:
        json.dump(apps, f, indent=2)
    
    print(f"  ✓ {config_file}")


def setup_user_database():
    """Create empty user database"""
    users_file = Path("config/users.pkl")
    with open(users_file, 'wb') as f:
        pickle.dump({}, f)
    
    print(f"  ✓ {users_file}")


def setup_sessions_database():
    """Create empty sessions database"""
    sessions_file = Path("config/sessions.pkl")
    with open(sessions_file, 'wb') as f:
        pickle.dump({}, f)
    
    print(f"  ✓ {sessions_file}")


def setup_settings():
    """Create default settings"""
    settings = {
        "tts": {
            "rate": 150,
            "volume": 0.9,
            "voice_index": 0
        },
        "stt": {
            "sample_rate": 16000,
            "model": "vosk-model-small-en-us-0.15"
        },
        "auth": {
            "similarity_threshold": 0.75,
            "session_timeout": 1800
        },
        "ui": {
            "theme": "dark",
            "show_waveform": true,
            "log_level": "INFO"
        }
    }
    
    config_file = Path("config/settings.json")
    with open(config_file, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"  ✓ {config_file}")


def main():
    """Main setup function"""
    print("=" * 60)
    print("EchoOS Configuration Setup")
    print("=" * 60)
    print()
    
    try:
        # Create directories
        setup_directories()
        print()
        
        # Create configuration files
        print("Creating configuration files...")
        setup_commands_config()
        setup_apps_config()
        setup_user_database()
        setup_sessions_database()
        setup_settings()
        print()
        
        print("=" * 60)
        print("✓ Configuration setup complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Run: python scripts/download_vosk_model.py")
        print("  2. Run: python scripts/discover_apps.py")
        print("  3. Run: python main.py")
        print()
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
