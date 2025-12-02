"""
Unit tests for command executor module
"""

import unittest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.executor import Executor


class TestExecutor(unittest.TestCase):
    """Test cases for Executor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock TTS
        class MockTTS:
            def speak(self, text, blocking=False):
                self.last_message = text
        
        self.executor = Executor(tts=MockTTS())
    
    def test_initialization(self):
        """Test executor initialization"""
        self.assertIsNotNone(self.executor)
        self.assertIsNotNone(self.executor.platform)
    
    def test_system_info_commands(self):
        """Test system information commands"""
        commands = [
            {'category': 'system_info', 'intent': 'system_info', 'parameters': {}},
            {'category': 'system_info', 'intent': 'battery', 'parameters': {}},
            {'category': 'system_info', 'intent': 'disk_space', 'parameters': {}},
            {'category': 'system_info', 'intent': 'memory', 'parameters': {}},
            {'category': 'system_info', 'intent': 'cpu', 'parameters': {}},
        ]
        
        for cmd in commands:
            result = self.executor.execute(cmd)
            self.assertIsInstance(result, bool)
    
    def test_web_commands(self):
        """Test web operation commands"""
        cmd = {
            'category': 'web',
            'intent': 'search_google',
            'parameters': {'query': 'test query'}
        }
        
        # Note: This will actually open browser in test
        # In production, mock webbrowser module
        result = self.executor.execute(cmd)
        self.assertIsInstance(result, bool)
    
    def test_invalid_command(self):
        """Test handling of invalid commands"""
        cmd = {
            'category': 'invalid',
            'intent': 'invalid',
            'parameters': {}
        }
        
        result = self.executor.execute(cmd)
        self.assertFalse(result)
    
    def test_empty_command(self):
        """Test handling of empty commands"""
        result = self.executor.execute(None)
        self.assertFalse(result)
        
        result = self.executor.execute({})
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
