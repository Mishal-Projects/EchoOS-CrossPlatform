"""
EchoOS - Cross-Platform Voice-Controlled Operating System
Main entry point for the application

Author: M A Mohammed Mishal
License: MIT
"""

import sys
import pathlib
import json
import pickle
import logging
from datetime import datetime

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from modules.ui import EchoMainWindow
from modules.stt import VoskManager
from modules.tts import TTS
from modules.auth import Authenticator
from modules.app_discovery import AppDiscovery
from modules.parser import CommandParser
from modules.executor import Executor
from modules.accessibility import AccessibilityManager
from modules.config import ConfigManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('echoos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def initialize_config():
    """Initialize configuration directories and files"""
    config_dir = pathlib.Path("config")
    config_dir.mkdir(exist_ok=True)
    
    models_dir = pathlib.Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Initialize default commands if not exists
    commands_file = config_dir / "commands.json"
    if not commands_file.exists():
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
        commands_file.write_text(json.dumps(default_commands, indent=2))
    
    # Initialize apps.json
    apps_file = config_dir / "apps.json"
    if not apps_file.exists():
        apps_file.write_text(json.dumps({"apps": []}, indent=2))
    
    # Initialize user database
    users_file = config_dir / "users.pkl"
    if not users_file.exists():
        with open(users_file, "wb") as f:
            pickle.dump({}, f)
    
    # Initialize sessions database
    sessions_file = config_dir / "sessions.pkl"
    if not sessions_file.exists():
        with open(sessions_file, "wb") as f:
            pickle.dump({}, f)
    
    logger.info("Configuration initialized successfully")


def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("Starting EchoOS - Voice-Controlled Operating System")
    logger.info(f"Version: 2.0 | Platform: {sys.platform}")
    logger.info(f"Python: {sys.version}")
    logger.info("=" * 60)
    
    try:
        # Initialize configuration
        initialize_config()
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("EchoOS")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("EchoOS")
        
        # Initialize core components
        logger.info("Initializing core components...")
        
        # Text-to-Speech
        logger.info("→ Initializing TTS engine...")
        tts = TTS()
        
        # Authentication System
        logger.info("→ Initializing authentication system...")
        auth = Authenticator(tts=tts)
        
        # Speech-to-Text
        logger.info("→ Initializing speech recognition...")
        stt_manager = VoskManager(tts=tts)
        
        # Application Discovery
        logger.info("→ Initializing app discovery...")
        app_discovery = AppDiscovery()
        
        # Command Parser
        logger.info("→ Initializing command parser...")
        parser = CommandParser(tts=tts)
        
        # Command Executor
        logger.info("→ Initializing command executor...")
        executor = Executor(tts=tts, auth=auth)
        
        # Accessibility Manager
        logger.info("→ Initializing accessibility features...")
        accessibility = AccessibilityManager(tts=tts)
        
        # Clean up expired sessions
        auth.cleanup_expired_sessions()
        
        # Create main window
        logger.info("→ Creating main window...")
        main_window = EchoMainWindow(
            auth=auth,
            stt_manager=stt_manager,
            app_discovery=app_discovery,
            parser=parser,
            executor=executor,
            tts=tts,
            accessibility=accessibility
        )
        
        # Show window
        main_window.show()
        
        # Setup periodic session cleanup (every 5 minutes)
        cleanup_timer = QTimer()
        cleanup_timer.timeout.connect(auth.cleanup_expired_sessions)
        cleanup_timer.start(300000)
        
        logger.info("✓ EchoOS started successfully!")
        logger.info("")
        logger.info("Available voice commands:")
        logger.info("  • System: shutdown, restart, sleep, lock")
        logger.info("  • Apps: open [app], close [app]")
        logger.info("  • Files: open file, create file, list files")
        logger.info("  • Web: open website, search google")
        logger.info("  • Info: system info, battery, disk space")
        logger.info("  • Volume: volume up, volume down, mute")
        logger.info("  • Accessibility: read screen, navigate, click")
        logger.info("")
        logger.info("Ready for voice commands! 🎤")
        
        # Start application event loop
        exit_code = app.exec()
        
        logger.info("EchoOS shutdown complete")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"Failed to start EchoOS: {e}", exc_info=True)
        print(f"\n❌ Error starting EchoOS: {e}")
        print("Check echoos.log for details")
        sys.exit(1)


if __name__ == "__main__":
    main()
