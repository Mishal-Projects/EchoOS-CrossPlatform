# EchoOS API Documentation

## Overview

This document provides detailed API documentation for EchoOS modules and classes.

## Table of Contents

1. [Authentication Module](#authentication-module)
2. [Speech-to-Text Module](#speech-to-text-module)
3. [Text-to-Speech Module](#text-to-speech-module)
4. [Command Parser](#command-parser)
5. [Command Executor](#command-executor)
6. [Application Discovery](#application-discovery)
7. [Accessibility Manager](#accessibility-manager)
8. [Configuration Manager](#configuration-manager)

---

## Authentication Module

**Module**: `modules.auth`

### Class: `Authenticator`

Voice biometric authentication system using Resemblyzer.

#### Constructor

```python
Authenticator(tts=None)
```

**Parameters**:
- `tts` (TTS, optional): Text-to-speech instance for feedback

#### Methods

##### `register_user(username: str, audio_data: np.ndarray) -> bool`

Register a new user with voice sample.

**Parameters**:
- `username` (str): Unique username
- `audio_data` (np.ndarray): Audio sample for voice profile

**Returns**:
- `bool`: True if registration successful

**Example**:
```python
auth = Authenticator()
success = auth.register_user("john_doe", audio_sample)
```

##### `authenticate(audio_data: np.ndarray) -> Optional[str]`

Authenticate user by voice.

**Parameters**:
- `audio_data` (np.ndarray): Audio sample for authentication

**Returns**:
- `str`: Username if authenticated, None otherwise

**Example**:
```python
username = auth.authenticate(audio_sample)
if username:
    print(f"Authenticated as {username}")
```

##### `validate_session(session_id: str) -> bool`

Validate active session.

**Parameters**:
- `session_id` (str): Session identifier

**Returns**:
- `bool`: True if session valid

##### `logout(session_id: str) -> bool`

End user session.

**Parameters**:
- `session_id` (str): Session to terminate

**Returns**:
- `bool`: True if logout successful

---

## Speech-to-Text Module

**Module**: `modules.stt`

### Class: `VoskManager`

Offline speech recognition using Vosk.

#### Constructor

```python
VoskManager(model_path: str = None, tts=None)
```

**Parameters**:
- `model_path` (str, optional): Path to Vosk model
- `tts` (TTS, optional): Text-to-speech instance

#### Methods

##### `recognize_once() -> Optional[str]`

Recognize single voice command.

**Returns**:
- `str`: Recognized text, None if failed

**Example**:
```python
stt = VoskManager()
text = stt.recognize_once()
print(f"Recognized: {text}")
```

##### `start_continuous_recognition(callback: Callable)`

Start continuous speech recognition.

**Parameters**:
- `callback` (Callable): Function called with recognized text

**Example**:
```python
def on_speech(text):
    print(f"Heard: {text}")

stt.start_continuous_recognition(on_speech)
```

##### `stop_continuous_recognition()`

Stop continuous recognition.

---

## Text-to-Speech Module

**Module**: `modules.tts`

### Class: `TTS`

Text-to-speech synthesis using pyttsx3.

#### Constructor

```python
TTS()
```

#### Methods

##### `speak(text: str, blocking: bool = False)`

Speak text aloud.

**Parameters**:
- `text` (str): Text to speak
- `blocking` (bool): Wait for speech to complete

**Example**:
```python
tts = TTS()
tts.speak("Hello, world!")
```

##### `set_rate(rate: int)`

Set speech rate.

**Parameters**:
- `rate` (int): Words per minute (50-300)

##### `set_volume(volume: float)`

Set speech volume.

**Parameters**:
- `volume` (float): Volume level (0.0-1.0)

##### `get_voices() -> List[Dict]`

Get available voices.

**Returns**:
- `List[Dict]`: Available voice information

---

## Command Parser

**Module**: `modules.parser`

### Class: `CommandParser`

Parse voice commands into structured format.

#### Constructor

```python
CommandParser(commands_file: str = "config/commands.json", tts=None)
```

**Parameters**:
- `commands_file` (str): Path to commands configuration
- `tts` (TTS, optional): Text-to-speech instance

#### Methods

##### `parse(text: str) -> Optional[Dict]`

Parse voice command text.

**Parameters**:
- `text` (str): Voice command text

**Returns**:
- `Dict`: Parsed command with category, intent, parameters

**Example**:
```python
parser = CommandParser()
command = parser.parse("open chrome")
# Returns: {
#   'category': 'application',
#   'intent': 'open',
#   'parameters': {'app_name': 'chrome'}
# }
```

##### `add_custom_command(category: str, intent: str, patterns: List[str])`

Add custom command pattern.

**Parameters**:
- `category` (str): Command category
- `intent` (str): Command intent
- `patterns` (List[str]): Voice patterns

---

## Command Executor

**Module**: `modules.executor`

### Class: `Executor`

Execute parsed commands.

#### Constructor

```python
Executor(tts=None, auth=None)
```

**Parameters**:
- `tts` (TTS, optional): Text-to-speech instance
- `auth` (Authenticator, optional): Authentication instance

#### Methods

##### `execute(command: Dict) -> bool`

Execute parsed command.

**Parameters**:
- `command` (Dict): Parsed command dictionary

**Returns**:
- `bool`: True if execution successful

**Example**:
```python
executor = Executor()
command = {'category': 'system', 'intent': 'lock', 'parameters': {}}
success = executor.execute(command)
```

---

## Application Discovery

**Module**: `modules.app_discovery`

### Class: `AppDiscovery`

Discover installed applications.

#### Constructor

```python
AppDiscovery()
```

#### Methods

##### `discover_applications() -> List[Dict]`

Scan system for installed applications.

**Returns**:
- `List[Dict]`: Discovered applications

**Example**:
```python
discovery = AppDiscovery()
apps = discovery.discover_applications()
for app in apps:
    print(f"{app['name']}: {app['path']}")
```

##### `add_application(name: str, path: str, aliases: List[str] = None)`

Manually add application.

**Parameters**:
- `name` (str): Application name
- `path` (str): Application path
- `aliases` (List[str], optional): Alternative names

---

## Accessibility Manager

**Module**: `modules.accessibility`

### Class: `AccessibilityManager`

Accessibility features for screen reading and navigation.

#### Constructor

```python
AccessibilityManager(tts=None)
```

**Parameters**:
- `tts` (TTS, optional): Text-to-speech instance

#### Methods

##### `read_screen() -> str`

Read screen content using OCR.

**Returns**:
- `str`: Extracted text

##### `navigate(direction: str)`

Navigate screen.

**Parameters**:
- `direction` (str): Direction (up, down, left, right)

##### `click()`

Perform mouse click.

##### `scroll(direction: str, amount: int = 3)`

Scroll screen.

**Parameters**:
- `direction` (str): Direction (up, down)
- `amount` (int): Scroll amount

---

## Configuration Manager

**Module**: `modules.config`

### Class: `ConfigManager`

Manage application configuration.

#### Constructor

```python
ConfigManager(config_dir: str = "config")
```

**Parameters**:
- `config_dir` (str): Configuration directory path

#### Methods

##### `load_config(filename: str) -> Dict`

Load configuration file.

**Parameters**:
- `filename` (str): Configuration filename

**Returns**:
- `Dict`: Configuration data

##### `save_config(filename: str, data: Dict)`

Save configuration file.

**Parameters**:
- `filename` (str): Configuration filename
- `data` (Dict): Configuration data

---

## Error Handling

All modules use Python's logging system. Errors are logged to `echoos.log`.

### Exception Types

- `AuthenticationError`: Authentication failures
- `RecognitionError`: Speech recognition failures
- `ExecutionError`: Command execution failures

### Example Error Handling

```python
try:
    command = parser.parse(text)
    executor.execute(command)
except Exception as e:
    logger.error(f"Error: {e}")
    tts.speak("Command failed")
```

---

## Events and Callbacks

### Speech Recognition Events

```python
def on_recognition(text: str):
    """Called when speech is recognized"""
    pass

def on_error(error: Exception):
    """Called on recognition error"""
    pass

stt.start_continuous_recognition(
    callback=on_recognition,
    error_callback=on_error
)
```

### Authentication Events

```python
def on_auth_success(username: str):
    """Called on successful authentication"""
    pass

def on_auth_failure():
    """Called on authentication failure"""
    pass
```

---

## Data Structures

### Command Dictionary

```python
{
    'category': str,      # Command category
    'intent': str,        # Command intent
    'parameters': dict,   # Command parameters
    'confidence': float   # Recognition confidence
}
```

### Application Dictionary

```python
{
    'name': str,          # Application name
    'path': str,          # Application path
    'aliases': list,      # Alternative names
    'icon': str           # Icon path (optional)
}
```

### User Dictionary

```python
{
    'username': str,      # Username
    'embedding': array,   # Voice embedding
    'created_at': str,    # Registration timestamp
    'last_login': str     # Last login timestamp
}
```

---

**Version**: 2.0  
**Last Updated**: December 2025
