"""
Voice Biometric Authentication Module for EchoOS
Uses Resemblyzer for voice authentication (optional)
Secure session management with encryption
Falls back to password authentication if Resemblyzer unavailable
"""

import pickle
import hashlib
import logging
import pathlib
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from cryptography.fernet import Fernet
import sounddevice as sd

logger = logging.getLogger(__name__)

# Try to import Resemblyzer (optional dependency)
try:
    from resemblyzer import VoiceEncoder, preprocess_wav
    RESEMBLYZER_AVAILABLE = True
    logger.info("Resemblyzer available - voice biometric authentication enabled")
except ImportError:
    RESEMBLYZER_AVAILABLE = False
    logger.warning("Resemblyzer not available - falling back to password authentication")


class Authenticator:
    """Voice biometric authentication system with password fallback"""
    
    def __init__(self, tts=None, users_file: str = "config/users.pkl",
                 sessions_file: str = "config/sessions.pkl"):
        """
        Initialize authenticator
        
        Args:
            tts: TTS instance for feedback
            users_file: Path to users database
            sessions_file: Path to sessions database
        """
        self.tts = tts
        self.users_file = pathlib.Path(users_file)
        self.sessions_file = pathlib.Path(sessions_file)
        self.current_user = None
        self.session_timeout = 30  # minutes
        
        # Initialize voice encoder if available
        if RESEMBLYZER_AVAILABLE:
            try:
                self.encoder = VoiceEncoder()
                self.voice_auth_enabled = True
                logger.info("Voice encoder initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize voice encoder: {e}")
                self.encoder = None
                self.voice_auth_enabled = False
        else:
            self.encoder = None
            self.voice_auth_enabled = False
        
        # Encryption key for sessions
        self.cipher_key = self._get_or_create_key()
        self.cipher = Fernet(self.cipher_key)
        
        # Load databases
        self.users = self._load_users()
        self.sessions = self._load_sessions()
        
        logger.info(f"Authenticator initialized (Voice auth: {self.voice_auth_enabled})")
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = pathlib.Path("config/.key")
        key_file.parent.mkdir(parents=True, exist_ok=True)
        
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            return key
    
    def _load_users(self) -> Dict:
        """Load users database"""
        try:
            if self.users_file.exists():
                with open(self.users_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading users: {e}")
        return {}
    
    def _save_users(self):
        """Save users database"""
        try:
            self.users_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.users_file, 'wb') as f:
                pickle.dump(self.users, f)
            logger.info("Users database saved")
        except Exception as e:
            logger.error(f"Error saving users: {e}")
    
    def _load_sessions(self) -> Dict:
        """Load sessions database"""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading sessions: {e}")
        return {}
    
    def _save_sessions(self):
        """Save sessions database"""
        try:
            self.sessions_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.sessions_file, 'wb') as f:
                pickle.dump(self.sessions, f)
        except Exception as e:
            logger.error(f"Error saving sessions: {e}")
    
    def record_voice_sample(self, duration: int = 5, sample_rate: int = 16000) -> Optional[np.ndarray]:
        """
        Record voice sample for registration/authentication
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate
            
        Returns:
            Audio data as numpy array or None
        """
        if not self.voice_auth_enabled:
            logger.warning("Voice authentication not available")
            return None
        
        try:
            logger.info(f"Recording voice sample for {duration} seconds...")
            if self.tts:
                self.tts.speak(f"Please speak clearly for {duration} seconds")
            
            # Record audio
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            
            # Flatten to 1D array
            audio_data = recording.flatten()
            
            logger.info("Voice sample recorded successfully")
            return audio_data
            
        except Exception as e:
            logger.error(f"Error recording voice sample: {e}")
            if self.tts:
                self.tts.speak("Error recording voice sample")
            return None
    
    def register_user(self, username: str, password: Optional[str] = None, duration: int = 5) -> bool:
        """
        Register new user with voice sample or password
        
        Args:
            username: Username to register
            password: Password (used if voice auth unavailable)
            duration: Recording duration for voice sample
            
        Returns:
            True if successful, False otherwise
        """
        if username in self.users:
            logger.warning(f"User {username} already exists")
            if self.tts:
                self.tts.speak("User already exists")
            return False
        
        try:
            user_data = {
                'created_at': datetime.now(),
                'last_login': None
            }
            
            # Try voice authentication first
            if self.voice_auth_enabled:
                audio_data = self.record_voice_sample(duration)
                if audio_data is not None:
                    # Preprocess audio
                    wav = preprocess_wav(audio_data)
                    
                    # Generate voice embedding
                    embedding = self.encoder.embed_utterance(wav)
                    user_data['embedding'] = embedding
                    user_data['auth_type'] = 'voice'
                else:
                    logger.warning("Voice recording failed, falling back to password")
                    if not password:
                        if self.tts:
                            self.tts.speak("Voice recording failed and no password provided")
                        return False
                    user_data['password_hash'] = hashlib.sha256(password.encode()).hexdigest()
                    user_data['auth_type'] = 'password'
            else:
                # Use password authentication
                if not password:
                    if self.tts:
                        self.tts.speak("Password required for authentication")
                    return False
                user_data['password_hash'] = hashlib.sha256(password.encode()).hexdigest()
                user_data['auth_type'] = 'password'
            
            # Store user
            self.users[username] = user_data
            self._save_users()
            
            logger.info(f"User {username} registered successfully ({user_data['auth_type']} auth)")
            if self.tts:
                self.tts.speak(f"User {username} registered successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            if self.tts:
                self.tts.speak("Registration failed")
            return False
    
    def authenticate(self, username: Optional[str] = None, password: Optional[str] = None, 
                    duration: int = 3, threshold: float = 0.75) -> Optional[str]:
        """
        Authenticate user by voice or password
        
        Args:
            username: Username (required for password auth)
            password: Password (for password auth)
            duration: Recording duration (for voice auth)
            threshold: Similarity threshold (0-1) for voice auth
            
        Returns:
            Username if authenticated, None otherwise
        """
        if not self.users:
            logger.warning("No users registered")
            if self.tts:
                self.tts.speak("No users registered")
            return None
        
        try:
            # Password authentication
            if username and password:
                if username not in self.users:
                    logger.warning(f"User {username} not found")
                    if self.tts:
                        self.tts.speak("User not found")
                    return None
                
                user_data = self.users[username]
                if user_data.get('auth_type') == 'password':
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    if password_hash == user_data.get('password_hash'):
                        self.current_user = username
                        self.users[username]['last_login'] = datetime.now()
                        self._save_users()
                        self._create_session(username)
                        
                        logger.info(f"User {username} authenticated (password)")
                        if self.tts:
                            self.tts.speak(f"Welcome {username}")
                        return username
                    else:
                        logger.warning("Invalid password")
                        if self.tts:
                            self.tts.speak("Invalid password")
                        return None
            
            # Voice authentication
            if self.voice_auth_enabled:
                audio_data = self.record_voice_sample(duration)
                if audio_data is None:
                    return None
                
                # Preprocess audio
                wav = preprocess_wav(audio_data)
                
                # Generate embedding
                test_embedding = self.encoder.embed_utterance(wav)
                
                # Compare with all users
                best_match = None
                best_similarity = 0.0
                
                for user, user_data in self.users.items():
                    if user_data.get('auth_type') != 'voice':
                        continue
                    
                    stored_embedding = user_data.get('embedding')
                    if stored_embedding is None:
                        continue
                    
                    similarity = np.dot(test_embedding, stored_embedding)
                    
                    logger.debug(f"Similarity with {user}: {similarity:.3f}")
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = user
                
                # Check threshold
                if best_similarity >= threshold:
                    self.current_user = best_match
                    self.users[best_match]['last_login'] = datetime.now()
                    self._save_users()
                    
                    # Create session
                    self._create_session(best_match)
                    
                    logger.info(f"User {best_match} authenticated (voice, similarity: {best_similarity:.3f})")
                    if self.tts:
                        self.tts.speak(f"Welcome {best_match}")
                    
                    return best_match
                else:
                    logger.warning(f"Authentication failed (best similarity: {best_similarity:.3f})")
                    if self.tts:
                        self.tts.speak("Authentication failed")
                    return None
            else:
                if self.tts:
                    self.tts.speak("Please provide username and password")
                return None
                
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            if self.tts:
                self.tts.speak("Authentication error")
            return None
    
    def _create_session(self, username: str):
        """Create encrypted session for user"""
        session_id = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()
        session_data = {
            'username': username,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=self.session_timeout)
        }
        
        # Encrypt session data
        encrypted_data = self.cipher.encrypt(pickle.dumps(session_data))
        self.sessions[session_id] = encrypted_data
        self._save_sessions()
        
        logger.info(f"Session created for {username}")
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            logger.info(f"User {self.current_user} logged out")
            if self.tts:
                self.tts.speak("Logged out")
            self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[str]:
        """Get current authenticated user"""
        return self.current_user
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.now()
        expired = []
        
        for session_id, encrypted_data in self.sessions.items():
            try:
                session_data = pickle.loads(self.cipher.decrypt(encrypted_data))
                if session_data['expires_at'] < now:
                    expired.append(session_id)
            except Exception as e:
                logger.error(f"Error checking session: {e}")
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            self._save_sessions()
            logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def list_users(self) -> list:
        """Get list of registered users"""
        return list(self.users.keys())
    
    def delete_user(self, username: str) -> bool:
        """Delete user"""
        if username in self.users:
            del self.users[username]
            self._save_users()
            logger.info(f"User {username} deleted")
            return True
        return False
    
    def is_voice_auth_available(self) -> bool:
        """Check if voice authentication is available"""
        return self.voice_auth_enabled
