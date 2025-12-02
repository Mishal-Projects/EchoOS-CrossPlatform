"""
Accessibility Module for EchoOS
Provides screen reading, navigation, and accessibility features
Cross-platform support for Windows and macOS
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AccessibilityManager:
    """Manages accessibility features"""
    
    def __init__(self, tts=None):
        """
        Initialize accessibility manager
        
        Args:
            tts: TTS instance for feedback
        """
        self.tts = tts
        self.pyautogui_available = False
        self.pytesseract_available = False
        
        # Try to import optional dependencies
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.pyautogui_available = True
            logger.info("PyAutoGUI available")
        except ImportError:
            logger.warning("PyAutoGUI not available - install for full accessibility features")
        
        try:
            import pytesseract
            self.pytesseract = pytesseract
            self.pytesseract_available = True
            logger.info("PyTesseract available")
        except ImportError:
            logger.warning("PyTesseract not available - install for screen reading")
        
        logger.info("Accessibility manager initialized")
    
    def read_screen(self) -> bool:
        """Read text from screen using OCR"""
        if not self.pytesseract_available or not self.pyautogui_available:
            if self.tts:
                self.tts.speak("Screen reading not available. Please install pytesseract and pyautogui")
            return False
        
        try:
            # Take screenshot
            screenshot = self.pyautogui.screenshot()
            
            # Extract text using OCR
            text = self.pytesseract.image_to_string(screenshot)
            
            if text.strip():
                if self.tts:
                    # Read first few lines
                    lines = text.strip().split('\n')[:5]
                    self.tts.speak(' '.join(lines))
                logger.info(f"Screen text: {text[:200]}")
                return True
            else:
                if self.tts:
                    self.tts.speak("No text found on screen")
                return False
                
        except Exception as e:
            logger.error(f"Error reading screen: {e}")
            if self.tts:
                self.tts.speak("Error reading screen")
            return False
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Click at position or current mouse position
        
        Args:
            x: X coordinate (optional)
            y: Y coordinate (optional)
        """
        if not self.pyautogui_available:
            if self.tts:
                self.tts.speak("Click not available")
            return False
        
        try:
            if x is not None and y is not None:
                self.pyautogui.click(x, y)
            else:
                self.pyautogui.click()
            
            if self.tts:
                self.tts.speak("Clicked")
            return True
        except Exception as e:
            logger.error(f"Error clicking: {e}")
            return False
    
    def scroll(self, direction: str = 'down', amount: int = 3) -> bool:
        """
        Scroll in direction
        
        Args:
            direction: 'up' or 'down'
            amount: Scroll amount
        """
        if not self.pyautogui_available:
            if self.tts:
                self.tts.speak("Scroll not available")
            return False
        
        try:
            scroll_amount = amount * 100 if direction == 'up' else -amount * 100
            self.pyautogui.scroll(scroll_amount)
            
            if self.tts:
                self.tts.speak(f"Scrolled {direction}")
            return True
        except Exception as e:
            logger.error(f"Error scrolling: {e}")
            return False
    
    def move_mouse(self, x: int, y: int) -> bool:
        """Move mouse to position"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.moveTo(x, y)
            return True
        except Exception as e:
            logger.error(f"Error moving mouse: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """Press keyboard key"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.press(key)
            if self.tts:
                self.tts.speak(f"Pressed {key}")
            return True
        except Exception as e:
            logger.error(f"Error pressing key: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """Type text"""
        if not self.pyautogui_available:
            return False
        
        try:
            self.pyautogui.write(text)
            if self.tts:
                self.tts.speak("Text typed")
            return True
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False
    
    def get_screen_size(self) -> tuple:
        """Get screen dimensions"""
        if not self.pyautogui_available:
            return (0, 0)
        
        try:
            return self.pyautogui.size()
        except Exception as e:
            logger.error(f"Error getting screen size: {e}")
            return (0, 0)
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position"""
        if not self.pyautogui_available:
            return (0, 0)
        
        try:
            return self.pyautogui.position()
        except Exception as e:
            logger.error(f"Error getting mouse position: {e}")
            return (0, 0)
