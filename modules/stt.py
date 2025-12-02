"""
Speech-to-Text Module for EchoOS
Offline speech recognition using Vosk
Cross-platform support for Windows and macOS
"""

import json
import logging
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from typing import Optional, Callable
import pathlib

logger = logging.getLogger(__name__)


class VoskManager:
    """Manages Vosk speech recognition"""
    
    def __init__(self, tts=None, model_path: str = "models/vosk-model-small-en-us-0.15"):
        """
        Initialize Vosk speech recognition
        
        Args:
            tts: TTS instance for feedback
            model_path: Path to Vosk model directory
        """
        self.tts = tts
        self.model_path = pathlib.Path(model_path)
        self.model = None
        self.recognizer = None
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.callback = None
        self.sample_rate = 16000
        
        self._load_model()
    
    def _load_model(self):
        """Load Vosk model"""
        try:
            if not self.model_path.exists():
                logger.error(f"Vosk model not found at {self.model_path}")
                logger.info("Please download the model using: python scripts/download_vosk_model.py")
                return False
            
            logger.info(f"Loading Vosk model from {self.model_path}...")
            self.model = Model(str(self.model_path))
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            self.recognizer.SetWords(True)
            logger.info("Vosk model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load Vosk model: {e}")
            return False
    
    def audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            logger.warning(f"Audio callback status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def start_listening(self, callback: Callable[[str], None]):
        """
        Start listening for speech
        
        Args:
            callback: Function to call with recognized text
        """
        if not self.model:
            logger.error("Cannot start listening: Model not loaded")
            if self.tts:
                self.tts.speak("Speech recognition model not loaded")
            return False
        
        self.callback = callback
        self.is_listening = True
        
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                logger.info("Started listening for speech...")
                if self.tts:
                    self.tts.speak("Listening")
                
                while self.is_listening:
                    data = self.audio_queue.get()
                    
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '').strip()
                        
                        if text and self.callback:
                            logger.info(f"Recognized: {text}")
                            self.callback(text)
                    else:
                        # Partial result (optional)
                        partial = json.loads(self.recognizer.PartialResult())
                        partial_text = partial.get('partial', '')
                        if partial_text:
                            logger.debug(f"Partial: {partial_text}")
        
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            if self.tts:
                self.tts.speak("Speech recognition error")
            return False
        
        return True
    
    def stop_listening(self):
        """Stop listening for speech"""
        self.is_listening = False
        logger.info("Stopped listening")
        if self.tts:
            self.tts.speak("Stopped listening")
    
    def recognize_once(self, duration: int = 5) -> Optional[str]:
        """
        Recognize speech for a fixed duration
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Recognized text or None
        """
        if not self.model:
            logger.error("Model not loaded")
            return None
        
        try:
            logger.info(f"Recording for {duration} seconds...")
            if self.tts:
                self.tts.speak("Speak now")
            
            # Record audio
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()
            
            # Recognize
            self.recognizer.AcceptWaveform(recording.tobytes())
            result = json.loads(self.recognizer.FinalResult())
            text = result.get('text', '').strip()
            
            logger.info(f"Recognized: {text}")
            return text if text else None
            
        except Exception as e:
            logger.error(f"Error in recognize_once: {e}")
            return None
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
