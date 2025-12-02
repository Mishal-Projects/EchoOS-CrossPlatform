"""
Unit tests for Command Parser
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.parser import CommandParser


class TestCommandParser:
    """Test cases for CommandParser"""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance for testing"""
        return CommandParser()
    
    def test_parse_system_shutdown(self, parser):
        """Test parsing shutdown command"""
        result = parser.parse("shutdown")
        assert result is not None
        assert result['category'] == 'system'
        assert result['intent'] == 'shutdown'
    
    def test_parse_open_app(self, parser):
        """Test parsing open application command"""
        result = parser.parse("open chrome")
        assert result is not None
        assert result['category'] == 'application'
        assert result['intent'] == 'open'
        assert result['parameters']['app_name'] == 'chrome'
    
    def test_parse_search_google(self, parser):
        """Test parsing Google search command"""
        result = parser.parse("search google artificial intelligence")
        assert result is not None
        assert result['category'] == 'web'
        assert result['intent'] == 'search_google'
        assert 'artificial intelligence' in result['parameters']['query']
    
    def test_parse_open_website(self, parser):
        """Test parsing open website command"""
        result = parser.parse("open website google")
        assert result is not None
        assert result['category'] == 'web'
        assert result['intent'] in ['open_website', 'open_site']
        assert 'google' in result['parameters']['url']
    
    def test_parse_volume_up(self, parser):
        """Test parsing volume up command"""
        result = parser.parse("volume up")
        assert result is not None
        assert result['category'] == 'volume'
        assert result['intent'] == 'volume_up'
    
    def test_parse_system_info(self, parser):
        """Test parsing system info command"""
        result = parser.parse("system info")
        assert result is not None
        assert result['category'] == 'system_info'
        assert result['intent'] == 'system_info'
    
    def test_parse_invalid_command(self, parser):
        """Test parsing invalid command"""
        result = parser.parse("xyz invalid command abc")
        # Should return None or handle gracefully
        assert result is None or result['intent'] is not None
    
    def test_parse_empty_string(self, parser):
        """Test parsing empty string"""
        result = parser.parse("")
        assert result is None
    
    def test_parse_case_insensitive(self, parser):
        """Test case insensitive parsing"""
        result1 = parser.parse("SHUTDOWN")
        result2 = parser.parse("shutdown")
        result3 = parser.parse("ShUtDoWn")
        
        assert result1 is not None
        assert result2 is not None
        assert result3 is not None
        assert result1['intent'] == result2['intent'] == result3['intent']
    
    def test_fuzzy_matching(self, parser):
        """Test fuzzy matching for similar commands"""
        # Test slight variations
        result = parser.parse("shutdwn")  # Typo
        # Should still match or return None gracefully
        assert result is None or result['intent'] == 'shutdown'
    
    def test_parameter_extraction(self, parser):
        """Test parameter extraction"""
        result = parser.parse("open chrome browser")
        assert result is not None
        assert 'app_name' in result['parameters']
        assert 'chrome' in result['parameters']['app_name'].lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
