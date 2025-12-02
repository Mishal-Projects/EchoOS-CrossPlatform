"""
Command Parser Module for EchoOS
Parses voice commands and extracts intent and parameters
Uses fuzzy matching for robust command recognition
"""

import json
import logging
import pathlib
from typing import Dict, Optional, Tuple, List
from rapidfuzz import fuzz, process

logger = logging.getLogger(__name__)


class CommandParser:
    """Parses voice commands into actionable intents"""
    
    def __init__(self, tts=None, commands_file: str = "config/commands.json"):
        """
        Initialize command parser
        
        Args:
            tts: TTS instance for feedback
            commands_file: Path to commands configuration
        """
        self.tts = tts
        self.commands_file = pathlib.Path(commands_file)
        self.commands = self._load_commands()
        self.fuzzy_threshold = 70  # Minimum similarity score
        
        logger.info("Command parser initialized")
    
    def _load_commands(self) -> Dict:
        """Load command mappings from file"""
        try:
            if self.commands_file.exists():
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    commands = json.load(f)
                logger.info(f"Loaded {len(commands)} command categories")
                return commands
        except Exception as e:
            logger.error(f"Error loading commands: {e}")
        return {}
    
    def parse(self, text: str) -> Optional[Dict]:
        """
        Parse voice command text
        
        Args:
            text: Voice command text
            
        Returns:
            Dictionary with intent, category, and parameters
        """
        if not text:
            return None
        
        text = text.lower().strip()
        logger.info(f"Parsing command: '{text}'")
        
        # Try exact and fuzzy matching
        result = self._match_command(text)
        
        if result:
            intent, category, params = result
            logger.info(f"Matched: {category}.{intent} with params: {params}")
            return {
                'intent': intent,
                'category': category,
                'parameters': params,
                'raw_text': text
            }
        else:
            logger.warning(f"No match found for: '{text}'")
            return None
    
    def _match_command(self, text: str) -> Optional[Tuple[str, str, Dict]]:
        """
        Match command using exact and fuzzy matching
        
        Returns:
            Tuple of (intent, category, parameters) or None
        """
        best_match = None
        best_score = 0
        
        # Iterate through all command categories
        for category, intents in self.commands.items():
            for intent, patterns in intents.items():
                for pattern in patterns:
                    # Check if pattern matches start of text
                    if text.startswith(pattern):
                        # Extract parameters (text after pattern)
                        params_text = text[len(pattern):].strip()
                        params = self._extract_parameters(intent, params_text)
                        return (intent, category, params)
                    
                    # Fuzzy matching
                    score = fuzz.partial_ratio(pattern, text)
                    if score > best_score and score >= self.fuzzy_threshold:
                        best_score = score
                        params_text = text.replace(pattern, '').strip()
                        params = self._extract_parameters(intent, params_text)
                        best_match = (intent, category, params)
        
        return best_match
    
    def _extract_parameters(self, intent: str, params_text: str) -> Dict:
        """
        Extract parameters from command text
        
        Args:
            intent: Command intent
            params_text: Remaining text after command pattern
            
        Returns:
            Dictionary of parameters
        """
        params = {}
        
        if not params_text:
            return params
        
        # Intent-specific parameter extraction
        if intent in ['open', 'close']:
            params['app_name'] = params_text
        
        elif intent in ['open_website', 'open_site']:
            # Clean up website URL
            url = params_text.replace('www.', '').replace('.com', '')
            params['url'] = url
        
        elif intent in ['search_google', 'search_youtube']:
            params['query'] = params_text
        
        elif intent in ['open_file', 'create_file', 'delete_file']:
            params['filename'] = params_text
        
        elif intent in ['volume_up', 'volume_down']:
            # Try to extract percentage
            words = params_text.split()
            for word in words:
                if word.isdigit():
                    params['amount'] = int(word)
                    break
            if 'amount' not in params:
                params['amount'] = 10  # Default
        
        elif intent in ['scroll_up', 'scroll_down']:
            # Extract scroll amount
            words = params_text.split()
            for word in words:
                if word.isdigit():
                    params['amount'] = int(word)
                    break
            if 'amount' not in params:
                params['amount'] = 3  # Default
        
        else:
            # Generic parameter
            params['text'] = params_text
        
        return params
    
    def get_command_suggestions(self, partial_text: str, limit: int = 5) -> List[str]:
        """
        Get command suggestions for partial text
        
        Args:
            partial_text: Partial command text
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested commands
        """
        all_patterns = []
        
        for category, intents in self.commands.items():
            for intent, patterns in intents.items():
                all_patterns.extend(patterns)
        
        # Use fuzzy matching to find similar commands
        matches = process.extract(
            partial_text,
            all_patterns,
            scorer=fuzz.partial_ratio,
            limit=limit
        )
        
        return [match[0] for match in matches if match[1] >= 60]
    
    def add_command(self, category: str, intent: str, patterns: List[str]) -> bool:
        """
        Add new command pattern
        
        Args:
            category: Command category
            intent: Command intent
            patterns: List of voice patterns
            
        Returns:
            True if successful
        """
        try:
            if category not in self.commands:
                self.commands[category] = {}
            
            self.commands[category][intent] = patterns
            
            # Save to file
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(self.commands, f, indent=2)
            
            logger.info(f"Added command: {category}.{intent}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding command: {e}")
            return False
    
    def get_all_commands(self) -> Dict:
        """Get all available commands"""
        return self.commands
    
    def reload_commands(self):
        """Reload commands from file"""
        self.commands = self._load_commands()
        logger.info("Commands reloaded")
