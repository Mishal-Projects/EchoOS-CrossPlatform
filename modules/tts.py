"""
Text-to-Speech Module for EchoOS
Provides voice feedback using pyttsx3
Cross-platform support for Windows and macOS
"""

import pyttsx3
import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)


class TTS:
    """Text-to-Speech engine wrapper"""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize TTS engine
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.rate = rate
        self.volume = volume
        self.engine = None
        self._lock = threading.Lock()
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the pyttsx3 engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Try to set a better voice if available
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice for better clarity
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def speak(self, text: str, blocking: bool = False):
        """
        Speak the given text
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete
        """
        if not text or not self.engine:
            return
        
        try:
            with self._lock:
                if blocking:
                    self.engine.say(text)
                    self.engine.runAndWait()
                else:
                    # Non-blocking speech in separate thread
                    thread = threading.Thread(target=self._speak_async, args=(text,))
                    thread.daemon = True
                    thread.start()
            
            logger.debug(f"TTS: {text}")
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def _speak_async(self, text: str):
        """Speak text asynchronously"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Async TTS error: {e}")
    
    def stop(self):
        """Stop current speech"""
        try:
            if self.engine:
                self.engine.stop()
        except Exception as e:
            logger.error(f"Error stopping TTS: {e}")
    
    def set_rate(self, rate: int):
        """Set speech rate"""
        try:
            self.rate = rate
            if self.engine:
                self.engine.setProperty('rate', rate)
        except Exception as e:
            logger.error(f"Error setting rate: {e}")
    
    def set_volume(self, volume: float):
        """Set volume level (0.0 to 1.0)"""
        try:
            self.volume = max(0.0, min(1.0, volume))
            if self.engine:
                self.engine.setProperty('volume', self.volume)
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
    
    def get_voices(self) -> list:
        """Get available voices"""
        try:
            if self.engine:
                return self.engine.getProperty('voices')
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
        return []
    
    def set_voice(self, voice_id: str):
        """Set voice by ID"""
        try:
            if self.engine:
                self.engine.setProperty('voice', voice_id)
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
