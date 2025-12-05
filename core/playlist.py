"""
KVGroove Playlist Management
Handles playlist creation, editing, and persistence
"""

import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from .library import Track


@dataclass
class Playlist:
    """Represents a playlist"""
    name: str
    tracks: List[str] = field(default_factory=list)  # List of file paths
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'tracks': self.tracks
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Playlist':
        return cls(
            name=data['name'],
            tracks=data.get('tracks', [])
        )
    
    def add_track(self, track_path: str):
        """Add a track to the playlist"""
        if track_path not in self.tracks:
            self.tracks.append(track_path)
    
    def remove_track(self, track_path: str):
        """Remove a track from the playlist"""
        if track_path in self.tracks:
            self.tracks.remove(track_path)
    
    def move_track(self, from_index: int, to_index: int):
        """Move a track within the playlist"""
        if 0 <= from_index < len(self.tracks) and 0 <= to_index < len(self.tracks):
            track = self.tracks.pop(from_index)
            self.tracks.insert(to_index, track)
    
    def clear(self):
        """Clear all tracks from the playlist"""
        self.tracks = []


class PlaylistManager:
    """Manages all playlists"""
    
    def __init__(self, data_path: str = "data/playlists.json"):
        self.data_path = Path(data_path)
        self.playlists: List[Playlist] = []
        self._load()
    
    def _load(self):
        """Load playlists from JSON file"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.playlists = [Playlist.from_dict(p) for p in data.get('playlists', [])]
        except Exception as e:
            print(f"Error loading playlists: {e}")
            self.playlists = []
    
    def _save(self):
        """Save playlists to JSON file"""
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                data = {
                    'playlists': [p.to_dict() for p in self.playlists]
                }
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving playlists: {e}")
    
    def create_playlist(self, name: str) -> Playlist:
        """Create a new playlist"""
        # Ensure unique name
        base_name = name
        counter = 1
        while any(p.name == name for p in self.playlists):
            name = f"{base_name} ({counter})"
            counter += 1
        
        playlist = Playlist(name=name)
        self.playlists.append(playlist)
        self._save()
        return playlist
    
    def delete_playlist(self, name: str) -> bool:
        """Delete a playlist by name"""
        for i, playlist in enumerate(self.playlists):
            if playlist.name == name:
                self.playlists.pop(i)
                self._save()
                return True
        return False
    
    def rename_playlist(self, old_name: str, new_name: str) -> bool:
        """Rename a playlist"""
        # Check if new name already exists
        if any(p.name == new_name for p in self.playlists):
            return False
        
        for playlist in self.playlists:
            if playlist.name == old_name:
                playlist.name = new_name
                self._save()
                return True
        return False
    
    def get_playlist(self, name: str) -> Optional[Playlist]:
        """Get a playlist by name"""
        for playlist in self.playlists:
            if playlist.name == name:
                return playlist
        return None
    
    def get_all_playlists(self) -> List[Playlist]:
        """Get all playlists"""
        return self.playlists.copy()
    
    def add_track_to_playlist(self, playlist_name: str, track_path: str) -> bool:
        """Add a track to a playlist"""
        playlist = self.get_playlist(playlist_name)
        if playlist:
            playlist.add_track(track_path)
            self._save()
            return True
        return False
    
    def remove_track_from_playlist(self, playlist_name: str, track_path: str) -> bool:
        """Remove a track from a playlist"""
        playlist = self.get_playlist(playlist_name)
        if playlist:
            playlist.remove_track(track_path)
            self._save()
            return True
        return False
    
    def save(self):
        """Manually save playlists"""
        self._save()
    
    def export_playlist_m3u(self, playlist_name: str, export_path: str) -> bool:
        """Export a playlist to M3U format"""
        playlist = self.get_playlist(playlist_name)
        if not playlist:
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n")
                for track_path in playlist.tracks:
                    f.write(f"{track_path}\n")
            return True
        except Exception as e:
            print(f"Error exporting playlist: {e}")
            return False
    
    def export_playlist_pls(self, playlist_name: str, export_path: str) -> bool:
        """Export a playlist to PLS format"""
        playlist = self.get_playlist(playlist_name)
        if not playlist:
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write("[playlist]\n")
                for i, track_path in enumerate(playlist.tracks, 1):
                    f.write(f"File{i}={track_path}\n")
                f.write(f"NumberOfEntries={len(playlist.tracks)}\n")
                f.write("Version=2\n")
            return True
        except Exception as e:
            print(f"Error exporting playlist: {e}")
            return False
    
    def import_playlist_m3u(self, import_path: str, playlist_name: Optional[str] = None) -> Optional[Playlist]:
        """Import a playlist from M3U format"""
        try:
            tracks = []
            with open(import_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Handle relative paths
                        if not Path(line).is_absolute():
                            base_dir = Path(import_path).parent
                            line = str(base_dir / line)
                        if Path(line).exists():
                            tracks.append(line)
            
            if not playlist_name:
                playlist_name = Path(import_path).stem
            
            playlist = self.create_playlist(playlist_name)
            playlist.tracks = tracks
            self._save()
            return playlist
        except Exception as e:
            print(f"Error importing playlist: {e}")
            return None
    
    def import_playlist_pls(self, import_path: str, playlist_name: Optional[str] = None) -> Optional[Playlist]:
        """Import a playlist from PLS format"""
        try:
            tracks = []
            with open(import_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.lower().startswith('file') and '=' in line:
                        path = line.split('=', 1)[1]
                        if not Path(path).is_absolute():
                            base_dir = Path(import_path).parent
                            path = str(base_dir / path)
                        if Path(path).exists():
                            tracks.append(path)
            
            if not playlist_name:
                playlist_name = Path(import_path).stem
            
            playlist = self.create_playlist(playlist_name)
            playlist.tracks = tracks
            self._save()
            return playlist
        except Exception as e:
            print(f"Error importing playlist: {e}")
            return None
    
    def export_all_playlists(self, export_dir: str) -> bool:
        """Export all playlists to a directory as JSON"""
        try:
            export_path = Path(export_dir)
            export_path.mkdir(parents=True, exist_ok=True)
            
            backup_file = export_path / "playlists_backup.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                data = {
                    'playlists': [p.to_dict() for p in self.playlists]
                }
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting playlists: {e}")
            return False
    
    def import_all_playlists(self, import_path: str, merge: bool = True) -> bool:
        """Import playlists from a backup file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                imported = [Playlist.from_dict(p) for p in data.get('playlists', [])]
                
                if merge:
                    # Merge with existing, skip duplicates
                    existing_names = {p.name for p in self.playlists}
                    for playlist in imported:
                        if playlist.name not in existing_names:
                            self.playlists.append(playlist)
                else:
                    # Replace all
                    self.playlists = imported
                
                self._save()
            return True
        except Exception as e:
            print(f"Error importing playlists: {e}")
            return False
