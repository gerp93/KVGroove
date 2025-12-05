"""
KVGroove Settings Manager
Handles application settings and preferences
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class AppSettings:
    """Application settings"""
    # Playback
    volume: float = 0.7
    shuffle: bool = False
    repeat: str = "none"  # "none", "one", "all"
    crossfade_seconds: float = 0.0
    playback_speed: float = 1.0
    
    # Equalizer (bass, mid, treble as multipliers 0.0-2.0, 1.0 is neutral)
    eq_bass: float = 1.0
    eq_mid: float = 1.0
    eq_treble: float = 1.0
    eq_enabled: bool = False
    
    # UI
    theme: str = "light"  # "light", "dark", "system"
    window_width: int = 1200
    window_height: int = 700
    mini_player: bool = False
    show_waveform: bool = False
    show_spectrum: bool = False
    
    # Library
    library_sort_column: str = "title"
    library_sort_reverse: bool = False
    library_view_mode: str = "list"  # "list", "folder"
    auto_rescan: bool = False
    auto_rescan_interval: int = 60  # minutes
    
    # Folders to watch
    watch_folders: List[str] = field(default_factory=list)
    
    # Recently played (track paths)
    recently_played: List[str] = field(default_factory=list)
    recently_played_max: int = 50
    
    # Favorites (track paths)
    favorites: List[str] = field(default_factory=list)
    
    # Last state
    last_folder: str = ""
    last_track: str = ""
    last_position: float = 0.0


class SettingsManager:
    """Manages application settings"""
    
    def __init__(self, data_path: str = "data/settings.json"):
        self.data_path = Path(data_path)
        self.settings = AppSettings()
        self._load()
    
    def _load(self):
        """Load settings from file"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Update settings with loaded data
                    for key, value in data.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save(self):
        """Save settings to file"""
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.save()
    
    def add_to_recently_played(self, track_path: str):
        """Add a track to recently played"""
        if track_path in self.settings.recently_played:
            self.settings.recently_played.remove(track_path)
        self.settings.recently_played.insert(0, track_path)
        # Trim to max size
        self.settings.recently_played = self.settings.recently_played[:self.settings.recently_played_max]
        self.save()
    
    def get_recently_played(self) -> List[str]:
        """Get recently played tracks"""
        return self.settings.recently_played.copy()
    
    def clear_recently_played(self):
        """Clear recently played history"""
        self.settings.recently_played = []
        self.save()
    
    def add_favorite(self, track_path: str):
        """Add a track to favorites"""
        if track_path not in self.settings.favorites:
            self.settings.favorites.append(track_path)
            self.save()
    
    def remove_favorite(self, track_path: str):
        """Remove a track from favorites"""
        if track_path in self.settings.favorites:
            self.settings.favorites.remove(track_path)
            self.save()
    
    def is_favorite(self, track_path: str) -> bool:
        """Check if a track is a favorite"""
        return track_path in self.settings.favorites
    
    def get_favorites(self) -> List[str]:
        """Get favorite tracks"""
        return self.settings.favorites.copy()
    
    def toggle_favorite(self, track_path: str) -> bool:
        """Toggle favorite status, returns new status"""
        if self.is_favorite(track_path):
            self.remove_favorite(track_path)
            return False
        else:
            self.add_favorite(track_path)
            return True
    
    def export_settings(self, export_path: str) -> bool:
        """Export all settings to a file"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_path: str) -> bool:
        """Import settings from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)
            self.save()
            return True
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
