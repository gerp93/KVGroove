"""
KVGroove UI Utilities
Shared utility functions for UI components
"""

import os
import subprocess
import platform
from datetime import datetime
from tkinter import messagebox
from typing import Optional
from core.library import Track


def format_date(timestamp: float) -> str:
    """Format timestamp as date in YYYY-MM-DD format"""
    if timestamp <= 0:
        return ""
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return ""


def open_file_location(track: Track, parent_window=None):
    """
    Open file explorer at track location.
    
    Args:
        track: The track whose location to open
        parent_window: Optional parent window for error dialogs
    """
    try:
        path = track.path
        if not os.path.exists(path):
            messagebox.showerror("Error", "File not found", parent=parent_window)
            return
        
        system = platform.system()
        if system == "Windows":
            # Use explorer with /select to highlight the file
            subprocess.Popen(['explorer', '/select,', os.path.normpath(path)])
        elif system == "Darwin":  # macOS
            subprocess.Popen(['open', '-R', path])
        else:  # Linux
            # Open the parent directory
            folder = os.path.dirname(path)
            subprocess.Popen(['xdg-open', folder])
    except (OSError, subprocess.SubprocessError) as e:
        messagebox.showerror("Error", f"Could not open file location: {e}", 
                           parent=parent_window)
