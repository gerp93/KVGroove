#!/usr/bin/env python3
"""
KVGroove - Music Player
A simple music player for Windows with library management, playlists, and queue.
"""

import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.auth import Auth
from ui.login_dialog import LoginDialog


def main():
    """Main entry point"""
    # Check if password is set and require authentication
    auth = Auth()
    
    if auth.is_password_set():
        # Show login dialog
        login = LoginDialog()
        if not login.run():
            # User cancelled or failed authentication
            sys.exit(0)
    
    # Import main window after authentication (keeps startup fast)
    from ui.main_window import MainWindow
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
