"""
Application Discovery Module for EchoOS
Discovers installed applications on Windows and macOS
Builds searchable database of applications
"""

import os
import json
import logging
import platform
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class AppDiscovery:
    """Discovers installed applications"""
    
    def __init__(self):
        self.platform = platform.system()
        self.apps = []
        logger.info(f"App discovery initialized for {self.platform}")
    
    def discover_apps(self) -> List[Dict]:
        """
        Discover installed applications
        
        Returns:
            List of discovered applications
        """
        logger.info("Starting application discovery...")
        
        if self.platform == 'Windows':
            self.apps = self._discover_windows_apps()
        elif self.platform == 'Darwin':
            self.apps = self._discover_macos_apps()
        else:
            self.apps = self._discover_linux_apps()
        
        logger.info(f"Discovered {len(self.apps)} applications")
        return self.apps
    
    def _discover_windows_apps(self) -> List[Dict]:
        """Discover Windows applications"""
        apps = []
        
        # Common Windows application directories
        search_paths = [
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')),
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')),
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs',
            Path(os.environ.get('APPDATA', '')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            try:
                # Search for .exe files
                for exe_file in search_path.rglob('*.exe'):
                    try:
                        app_name = exe_file.stem
                        # Skip common system files
                        if app_name.lower() in ['uninstall', 'setup', 'installer', 'update']:
                            continue
                        
                        apps.append({
                            'name': app_name,
                            'path': str(exe_file),
                            'aliases': [app_name.lower(), app_name.replace(' ', '').lower()]
                        })
                    except Exception as e:
                        logger.debug(f"Error processing {exe_file}: {e}")
            except Exception as e:
                logger.error(f"Error searching {search_path}: {e}")
        
        # Add common Windows apps
        common_apps = [
            {'name': 'Notepad', 'path': 'notepad.exe', 'aliases': ['notepad']},
            {'name': 'Calculator', 'path': 'calc.exe', 'aliases': ['calculator', 'calc']},
            {'name': 'Paint', 'path': 'mspaint.exe', 'aliases': ['paint']},
            {'name': 'Command Prompt', 'path': 'cmd.exe', 'aliases': ['cmd', 'command prompt', 'terminal']},
            {'name': 'PowerShell', 'path': 'powershell.exe', 'aliases': ['powershell']},
            {'name': 'Task Manager', 'path': 'taskmgr.exe', 'aliases': ['task manager', 'taskmgr']},
            {'name': 'File Explorer', 'path': 'explorer.exe', 'aliases': ['explorer', 'file explorer']},
        ]
        
        apps.extend(common_apps)
        return apps
    
    def _discover_macos_apps(self) -> List[Dict]:
        """Discover macOS applications"""
        apps = []
        
        # Common macOS application directories
        search_paths = [
            Path('/Applications'),
            Path.home() / 'Applications',
            Path('/System/Applications')
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            try:
                # Search for .app bundles
                for app_bundle in search_path.glob('*.app'):
                    try:
                        app_name = app_bundle.stem
                        apps.append({
                            'name': app_name,
                            'path': str(app_bundle),
                            'aliases': [app_name.lower(), app_name.replace(' ', '').lower()]
                        })
                    except Exception as e:
                        logger.debug(f"Error processing {app_bundle}: {e}")
            except Exception as e:
                logger.error(f"Error searching {search_path}: {e}")
        
        # Add common macOS apps
        common_apps = [
            {'name': 'Safari', 'path': '/Applications/Safari.app', 'aliases': ['safari']},
            {'name': 'Finder', 'path': '/System/Library/CoreServices/Finder.app', 'aliases': ['finder']},
            {'name': 'Terminal', 'path': '/System/Applications/Utilities/Terminal.app', 'aliases': ['terminal']},
            {'name': 'TextEdit', 'path': '/System/Applications/TextEdit.app', 'aliases': ['textedit', 'text edit']},
            {'name': 'Calculator', 'path': '/System/Applications/Calculator.app', 'aliases': ['calculator', 'calc']},
            {'name': 'Calendar', 'path': '/System/Applications/Calendar.app', 'aliases': ['calendar']},
            {'name': 'Mail', 'path': '/System/Applications/Mail.app', 'aliases': ['mail', 'email']},
        ]
        
        apps.extend(common_apps)
        return apps
    
    def _discover_linux_apps(self) -> List[Dict]:
        """Discover Linux applications"""
        apps = []
        
        # Common Linux application directories
        search_paths = [
            Path('/usr/share/applications'),
            Path.home() / '.local' / 'share' / 'applications'
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            try:
                # Search for .desktop files
                for desktop_file in search_path.glob('*.desktop'):
                    try:
                        # Parse .desktop file
                        with open(desktop_file, 'r') as f:
                            content = f.read()
                            
                            # Extract Name and Exec
                            name = None
                            exec_cmd = None
                            
                            for line in content.split('\n'):
                                if line.startswith('Name='):
                                    name = line.split('=', 1)[1].strip()
                                elif line.startswith('Exec='):
                                    exec_cmd = line.split('=', 1)[1].strip()
                            
                            if name and exec_cmd:
                                apps.append({
                                    'name': name,
                                    'path': exec_cmd.split()[0],  # First part of exec command
                                    'aliases': [name.lower(), name.replace(' ', '').lower()]
                                })
                    except Exception as e:
                        logger.debug(f"Error processing {desktop_file}: {e}")
            except Exception as e:
                logger.error(f"Error searching {search_path}: {e}")
        
        return apps
    
    def save_apps(self, filename: str = "config/apps.json") -> bool:
        """
        Save discovered apps to JSON file
        
        Args:
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({'apps': self.apps}, f, indent=2)
            
            logger.info(f"Saved {len(self.apps)} apps to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving apps: {e}")
            return False
    
    def discover_and_save(self, filename: str = "config/apps.json") -> List[Dict]:
        """
        Discover apps and save to file
        
        Args:
            filename: Output filename
            
        Returns:
            List of discovered apps
        """
        apps = self.discover_apps()
        self.save_apps(filename)
        return apps
    
    def search_app(self, query: str) -> List[Dict]:
        """
        Search for app by name or alias
        
        Args:
            query: Search query
            
        Returns:
            List of matching apps
        """
        query = query.lower()
        matches = []
        
        for app in self.apps:
            if query in app['name'].lower():
                matches.append(app)
            elif any(query in alias for alias in app.get('aliases', [])):
                matches.append(app)
        
        return matches
