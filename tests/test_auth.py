"""
Unit tests for authentication module
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.auth import Authenticator


class TestAuthenticator(unittest.TestCase):
    """Test cases for Authenticator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.users_file = Path(self.test_dir) / "users.pkl"
        self.sessions_file = Path(self.test_dir) / "sessions.pkl"
        
        # Mock TTS
        class MockTTS:
            def speak(self, text, blocking=False):
                pass
        
        self.auth = Authenticator(tts=MockTTS())
        self.auth.users_file = self.users_file
        self.auth.sessions_file = self.sessions_file
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test authenticator initialization"""
        self.assertIsNotNone(self.auth)
        self.assertIsNotNone(self.auth.model)
        self.assertIsNotNone(self.auth.cipher)
    
    def test_user_registration(self):
        """Test user registration"""
        # This would require actual audio input
        # Placeholder for integration testing
        pass
    
    def test_session_management(self):
        """Test session creation and validation"""
        # Create mock session
        test_user = "test_user"
        session_id = self.auth._create_session(test_user)
        
        self.assertIsNotNone(session_id)
        self.assertTrue(self.auth.validate_session(session_id))
    
    def test_session_expiry(self):
        """Test session expiration"""
        # This would require time manipulation
        # Placeholder for integration testing
        pass
    
    def test_invalid_session(self):
        """Test invalid session handling"""
        invalid_session = "invalid_session_id"
        self.assertFalse(self.auth.validate_session(invalid_session))


if __name__ == '__main__':
    unittest.main()
