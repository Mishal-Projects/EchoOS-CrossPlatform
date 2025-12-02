"""
Voice Biometric Authentication Module for EchoOS
Uses Resemblyzer for voice authentication
Secure session management with encryption
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
from resemblyzer import VoiceEncoder, preprocess_wav

logger = logging.getLogger(__name__)


class Authenticator:
    """Voice biometric authentication system"""
    
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
        self.encoder = VoiceEncoder()
        self.current_user = None
        self.session_timeout = 30  # minutes
        
        # Encryption key for sessions
        self.cipher_key = self._get_or_create_key()
        self.cipher = Fernet(self.cipher_key)
        
        # Load databases
        self.users = self._load_users()
        self.sessions = self._load_sessions()
        
        logger.info("Authenticator initialized")
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = pathlib.Path("config/.key")
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
    
    def register_user(self, username: str, duration: int = 5) -> bool:
        """
        Register new user with voice sample
        
        Args:
            username: Username to register
            duration: Recording duration
            
        Returns:
            True if successful, False otherwise
        """
        if username in self.users:
            logger.warning(f"User {username} already exists")
            if self.tts:
                self.tts.speak("User already exists")
            return False
        
        try:
            # Record voice sample
            audio_data = self.record_voice_sample(duration)
            if audio_data is None:
                return False
            
            # Preprocess audio
            wav = preprocess_wav(audio_data)
            
            # Generate voice embedding
            embedding = self.encoder.embed_utterance(wav)
            
            # Store user
            self.users[username] = {
                'embedding': embedding,
                'created_at': datetime.now(),
                'last_login': None
            }
            
            self._save_users()
            
            logger.info(f"User {username} registered successfully")
            if self.tts:
                self.tts.speak(f"User {username} registered successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            if self.tts:
                self.tts.speak("Registration failed")
            return False
    
    def authenticate(self, duration: int = 3, threshold: float = 0.75) -> Optional[str]:
        """
        Authenticate user by voice
        
        Args:
            duration: Recording duration
            threshold: Similarity threshold (0-1)
            
        Returns:
            Username if authenticated, None otherwise
        """
        if not self.users:
            logger.warning("No users registered")
            if self.tts:
                self.tts.speak("No users registered")
            return None
        
        try:
            # Record voice sample
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
            
            for username, user_data in self.users.items():
                stored_embedding = user_data['embedding']
                similarity = np.dot(test_embedding, stored_embedding)
                
                logger.debug(f"Similarity with {username}: {similarity:.3f}")
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = username
            
            # Check threshold
            if best_similarity >= threshold:
                self.current_user = best_match
                self.users[best_match]['last_login'] = datetime.now()
                self._save_users()
                
                # Create session
                self._create_session(best_match)
                
                logger.info(f"User {best_match} authenticated (similarity: {best_similarity:.3f})")
                if self.tts:
                    self.tts.speak(f"Welcome {best_match}")
                
                return best_match
            else:
                logger.warning(f"Authentication failed (best similarity: {best_similarity:.3f})")
                if self.tts:
                    self.tts.speak("Authentication failed")
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
