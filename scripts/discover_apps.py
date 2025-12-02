"""
Application Discovery Utility
Scans system for installed applications and updates apps.json
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.app_discovery import AppDiscovery


def main():
    """Run application discovery"""
    print("=" * 60)
    print("EchoOS Application Discovery Utility")
    print("=" * 60)
    print()
    
    print("Scanning system for installed applications...")
    print("This may take a few moments...")
    print()
    
    try:
        # Initialize app discovery
        discovery = AppDiscovery()
        
        # Discover applications
        apps = discovery.discover_applications()
        
        print(f"✓ Found {len(apps)} applications")
        print()
        
        # Display discovered apps
        print("Discovered Applications:")
        print("-" * 60)
        for app in sorted(apps, key=lambda x: x['name']):
            print(f"  • {app['name']}")
            print(f"    Path: {app['path']}")
            if app.get('aliases'):
                print(f"    Aliases: {', '.join(app['aliases'])}")
            print()
        
        # Save to config
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        apps_file = config_dir / "apps.json"
        with open(apps_file, 'w') as f:
            json.dump({"apps": apps}, f, indent=2)
        
        print("=" * 60)
        print(f"✓ Application database saved to {apps_file}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during discovery: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
