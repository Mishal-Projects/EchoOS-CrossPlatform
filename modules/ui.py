"""
User Interface Module for EchoOS
Modern GUI using PySide6
Cross-platform support for Windows and macOS
"""

import logging
import threading
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QLineEdit,
    QMessageBox, QStatusBar
)
from PySide6.QtCore import Qt, Signal, QObject, QTimer
from PySide6.QtGui import QFont, QIcon

logger = logging.getLogger(__name__)


class SignalEmitter(QObject):
    """Signal emitter for thread-safe GUI updates"""
    update_status = Signal(str)
    update_log = Signal(str)
    command_recognized = Signal(str)


class EchoMainWindow(QMainWindow):
    """Main window for EchoOS"""
    
    def __init__(self, auth, stt_manager, app_discovery, parser, executor, tts, accessibility):
        super().__init__()
        
        # Store components
        self.auth = auth
        self.stt_manager = stt_manager
        self.app_discovery = app_discovery
        self.parser = parser
        self.executor = executor
        self.tts = tts
        self.accessibility = accessibility
        
        # State
        self.is_listening = False
        self.is_authenticated = False
        
        # Signal emitter for thread-safe updates
        self.signals = SignalEmitter()
        self.signals.update_status.connect(self._update_status_label)
        self.signals.update_log.connect(self._append_log)
        self.signals.command_recognized.connect(self._handle_command)
        
        # Setup UI
        self._setup_ui()
        
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Setup user interface"""
        self.setWindowTitle("EchoOS - Voice-Controlled Operating System")
        self.setMinimumSize(800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel("🎙️ EchoOS")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Voice-Controlled Operating System")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666;")
        main_layout.addWidget(subtitle_label)
        
        # Status
        self.status_label = QLabel("Ready")
        status_font = QFont()
        status_font.setPointSize(14)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 10px; background-color: #e8f5e9; border-radius: 5px;")
        main_layout.addWidget(self.status_label)
        
        # Authentication Group
        auth_group = QGroupBox("Authentication")
        auth_layout = QVBoxLayout()
        
        # User info
        self.user_label = QLabel("Not authenticated")
        self.user_label.setStyleSheet("font-weight: bold; color: #d32f2f;")
        auth_layout.addWidget(self.user_label)
        
        # Auth buttons
        auth_buttons_layout = QHBoxLayout()
        
        self.register_btn = QPushButton("Register New User")
        self.register_btn.clicked.connect(self._register_user)
        auth_buttons_layout.addWidget(self.register_btn)
        
        self.login_btn = QPushButton("Voice Login")
        self.login_btn.clicked.connect(self._authenticate_user)
        auth_buttons_layout.addWidget(self.login_btn)
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self._logout_user)
        self.logout_btn.setEnabled(False)
        auth_buttons_layout.addWidget(self.logout_btn)
        
        auth_layout.addLayout(auth_buttons_layout)
        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)
        
        # Voice Control Group
        control_group = QGroupBox("Voice Control")
        control_layout = QVBoxLayout()
        
        # Control buttons
        control_buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🎤 Start Listening")
        self.start_btn.clicked.connect(self._start_listening)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        control_buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Listening")
        self.stop_btn.clicked.connect(self._stop_listening)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        control_buttons_layout.addWidget(self.stop_btn)
        
        control_layout.addLayout(control_buttons_layout)
        
        # Command input (manual)
        manual_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Or type a command manually...")
        self.command_input.returnPressed.connect(self._execute_manual_command)
        manual_layout.addWidget(self.command_input)
        
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self._execute_manual_command)
        manual_layout.addWidget(self.execute_btn)
        
        control_layout.addLayout(manual_layout)
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Log Group
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        # Clear log button
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        log_layout.addWidget(clear_log_btn)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # App Discovery Status
        self.apps_status = QLabel("App discovery: Not started")
        self.apps_status.setStyleSheet("color: #666; font-style: italic;")
        main_layout.addWidget(self.apps_status)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Add initial log message
        self._append_log("EchoOS initialized. Please authenticate to start.")
    
    def _update_status_label(self, text: str):
        """Update status label (thread-safe)"""
        self.status_label.setText(text)
        
        # Color based on status
        if "listening" in text.lower():
            self.status_label.setStyleSheet("padding: 10px; background-color: #e3f2fd; border-radius: 5px;")
        elif "error" in text.lower() or "failed" in text.lower():
            self.status_label.setStyleSheet("padding: 10px; background-color: #ffebee; border-radius: 5px;")
        else:
            self.status_label.setStyleSheet("padding: 10px; background-color: #e8f5e9; border-radius: 5px;")
    
    def _append_log(self, text: str):
        """Append to log (thread-safe)"""
        self.log_text.append(f"[{self._get_timestamp()}] {text}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def _register_user(self):
        """Register new user"""
        from PySide6.QtWidgets import QInputDialog
        
        username, ok = QInputDialog.getText(
            self, "Register User", "Enter username:"
        )
        
        if ok and username:
            self._append_log(f"Registering user: {username}")
            self.signals.update_status.emit("Recording voice sample...")
            
            # Run in thread to avoid blocking UI
            def register():
                success = self.auth.register_user(username, duration=5)
                if success:
                    self.signals.update_status.emit(f"User {username} registered!")
                    self.signals.update_log.emit(f"✓ User {username} registered successfully")
                else:
                    self.signals.update_status.emit("Registration failed")
                    self.signals.update_log.emit("✗ Registration failed")
            
            thread = threading.Thread(target=register)
            thread.start()
    
    def _authenticate_user(self):
        """Authenticate user by voice"""
        self._append_log("Starting voice authentication...")
        self.signals.update_status.emit("Authenticating...")
        
        def authenticate():
            username = self.auth.authenticate(duration=3, threshold=0.75)
            if username:
                self.is_authenticated = True
                self.signals.update_status.emit(f"Authenticated as {username}")
                self.signals.update_log.emit(f"✓ Authenticated as {username}")
                
                # Update UI
                self.user_label.setText(f"Logged in as: {username}")
                self.user_label.setStyleSheet("font-weight: bold; color: #388e3c;")
                self.start_btn.setEnabled(True)
                self.logout_btn.setEnabled(True)
                self.login_btn.setEnabled(False)
                self.register_btn.setEnabled(False)
            else:
                self.signals.update_status.emit("Authentication failed")
                self.signals.update_log.emit("✗ Authentication failed")
        
        thread = threading.Thread(target=authenticate)
        thread.start()
    
    def _logout_user(self):
        """Logout current user"""
        self.auth.logout()
        self.is_authenticated = False
        
        self.user_label.setText("Not authenticated")
        self.user_label.setStyleSheet("font-weight: bold; color: #d32f2f;")
        self.start_btn.setEnabled(False)
        self.logout_btn.setEnabled(False)
        self.login_btn.setEnabled(True)
        self.register_btn.setEnabled(True)
        
        self._append_log("Logged out")
        self.signals.update_status.emit("Logged out")
    
    def _start_listening(self):
        """Start voice recognition"""
        if not self.is_authenticated:
            QMessageBox.warning(self, "Not Authenticated", "Please authenticate first")
            return
        
        if not self.stt_manager.is_model_loaded():
            QMessageBox.critical(self, "Model Not Loaded", 
                               "Vosk model not loaded. Please download the model first.")
            return
        
        self.is_listening = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self._append_log("Started listening for voice commands")
        self.signals.update_status.emit("🎤 Listening...")
        
        # Start listening in thread
        def listen():
            self.stt_manager.start_listening(self._on_speech_recognized)
        
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
    
    def _stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        self.stt_manager.stop_listening()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self._append_log("Stopped listening")
        self.signals.update_status.emit("Ready")
    
    def _on_speech_recognized(self, text: str):
        """Handle recognized speech"""
        self.signals.command_recognized.emit(text)
    
    def _handle_command(self, text: str):
        """Handle recognized command"""
        self._append_log(f"Recognized: {text}")
        
        # Parse command
        command = self.parser.parse(text)
        
        if command:
            self._append_log(f"Command: {command['category']}.{command['intent']}")
            
            # Execute command
            success = self.executor.execute(command)
            
            if success:
                self._append_log("✓ Command executed successfully")
            else:
                self._append_log("✗ Command execution failed")
        else:
            self._append_log("✗ Command not recognized")
            if self.tts:
                self.tts.speak("Command not recognized")
    
    def _execute_manual_command(self):
        """Execute manually typed command"""
        text = self.command_input.text().strip()
        if text:
            self._handle_command(text)
            self.command_input.clear()
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.is_listening:
            self._stop_listening()
        
        logger.info("Main window closed")
        event.accept()
