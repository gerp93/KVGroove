"""
KVGroove Library Management
Handles music library indexing and metadata
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


SUPPORTED_FORMATS = {'.mp3', '.flac', '.wav', '.ogg', '.m4a', '.wma'}


@dataclass
class Track:
    """Represents a music track"""
    path: str
    title: str
    artist: str
    album: str
    duration: float  # seconds
    created: float = 0.0  # file creation timestamp
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Track':
        # Handle old tracks without 'created' field
        if 'created' not in data:
            data['created'] = 0.0
        return cls(**data)
    
    def __eq__(self, other):
        if isinstance(other, Track):
            return self.path == other.path
        return False
    
    def __hash__(self):
        return hash(self.path)


class Library:
    """Music library manager"""
    
    def __init__(self, data_path: str = "data/library.json"):
        self.data_path = Path(data_path)
        self.folders: List[str] = []
        self.tracks: List[Track] = []
        self._load()
    
    def _load(self):
        """Load library from JSON file"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.folders = data.get('folders', [])
                    self.tracks = [Track.from_dict(t) for t in data.get('tracks', [])]
        except Exception as e:
            print(f"Error loading library: {e}")
            self.folders = []
            self.tracks = []
    
    def _save(self):
        """Save library to JSON file"""
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                data = {
                    'folders': self.folders,
                    'tracks': [t.to_dict() for t in self.tracks]
                }
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving library: {e}")
    
    def add_folder(self, folder_path: str) -> int:
        """Add a folder to the library and scan for tracks. Returns number of tracks added."""
        folder = str(Path(folder_path).resolve())
        if folder not in self.folders:
            self.folders.append(folder)
        
        added = self._scan_folder(folder)
        self._save()
        return added
    
    def remove_folder(self, folder_path: str):
        """Remove a folder from the library"""
        folder = str(Path(folder_path).resolve())
        if folder in self.folders:
            self.folders.remove(folder)
            # Remove tracks from this folder
            self.tracks = [t for t in self.tracks if not t.path.startswith(folder)]
            self._save()
    
    def _scan_folder(self, folder_path: str) -> int:
        """Scan a folder for audio files. Returns number of tracks added."""
        added = 0
        folder = Path(folder_path)
        
        if not folder.exists():
            return 0
        
        existing_paths = {t.path for t in self.tracks}
        
        for file_path in folder.rglob('*'):
            if file_path.suffix.lower() in SUPPORTED_FORMATS:
                path_str = str(file_path)
                if path_str not in existing_paths:
                    track = self._extract_metadata(path_str)
                    if track:
                        self.tracks.append(track)
                        added += 1
        
        return added
    
    def _extract_metadata(self, file_path: str) -> Optional[Track]:
        """Extract metadata from an audio file"""
        try:
            path = Path(file_path)
            audio = File(file_path)
            
            title = path.stem
            artist = "Unknown Artist"
            album = "Unknown Album"
            duration = 0.0
            
            # Get file creation time
            created = os.path.getctime(file_path)
            
            if audio is not None:
                if audio.info:
                    duration = audio.info.length
                
                # Try to get tags
                if hasattr(audio, 'tags') and audio.tags:
                    tags = audio.tags
                    
                    # Handle different tag formats
                    if isinstance(audio, MP3):
                        try:
                            id3 = EasyID3(file_path)
                            title = id3.get('title', [title])[0]
                            artist = id3.get('artist', [artist])[0]
                            album = id3.get('album', [album])[0]
                        except Exception:
                            pass
                    elif isinstance(audio, FLAC):
                        title = tags.get('title', [title])[0]
                        artist = tags.get('artist', [artist])[0]
                        album = tags.get('album', [album])[0]
                    else:
                        # Generic approach
                        if 'title' in tags:
                            title = str(tags['title'][0]) if isinstance(tags['title'], list) else str(tags['title'])
                        if 'artist' in tags:
                            artist = str(tags['artist'][0]) if isinstance(tags['artist'], list) else str(tags['artist'])
                        if 'album' in tags:
                            album = str(tags['album'][0]) if isinstance(tags['album'], list) else str(tags['album'])
            
            return Track(
                path=file_path,
                title=title,
                artist=artist,
                album=album,
                duration=duration,
                created=created
            )
        except Exception as e:
            print(f"Error extracting metadata from {file_path}: {e}")
            return None
    
    def refresh(self):
        """Refresh the library by rescanning all folders"""
        self.tracks = []
        for folder in self.folders:
            self._scan_folder(folder)
        self._save()
    
    def get_all_tracks(self) -> List[Track]:
        """Get all tracks in the library"""
        return self.tracks.copy()
    
    def search(self, query: str) -> List[Track]:
        """Search tracks by title, artist, or album"""
        query = query.lower()
        return [
            t for t in self.tracks
            if query in t.title.lower() or 
               query in t.artist.lower() or 
               query in t.album.lower()
        ]
    
    def get_track_by_path(self, path: str) -> Optional[Track]:
        """Get a track by its file path"""
        for track in self.tracks:
            if track.path == path:
                return track
        return None
    
    def get_tracks_by_paths(self, paths: List[str]) -> List[Track]:
        """Get multiple tracks by their file paths"""
        path_set = set(paths)
        return [t for t in self.tracks if t.path in path_set]
    
    def get_tracks_by_folder(self, folder_path: str) -> List[Track]:
        """Get all tracks in a specific folder"""
        folder = str(Path(folder_path).resolve())
        return [t for t in self.tracks if t.path.startswith(folder)]
    
    def get_folder_structure(self) -> Dict[str, List[Track]]:
        """Get tracks organized by folder"""
        structure = {}
        for track in self.tracks:
            folder = str(Path(track.path).parent)
            if folder not in structure:
                structure[folder] = []
            structure[folder].append(track)
        return structure
    
    def get_all_artists(self) -> List[str]:
        """Get list of unique artists"""
        artists = set()
        for track in self.tracks:
            if track.artist and track.artist != "Unknown Artist":
                artists.add(track.artist)
        return sorted(artists)
    
    def get_all_albums(self) -> List[str]:
        """Get list of unique albums"""
        albums = set()
        for track in self.tracks:
            if track.album and track.album != "Unknown Album":
                albums.add(track.album)
        return sorted(albums)
    
    def get_tracks_by_artist(self, artist: str) -> List[Track]:
        """Get all tracks by an artist"""
        return [t for t in self.tracks if t.artist.lower() == artist.lower()]
    
    def get_tracks_by_album(self, album: str) -> List[Track]:
        """Get all tracks in an album"""
        return [t for t in self.tracks if t.album.lower() == album.lower()]
    
    def find_duplicates(self) -> List[List[Track]]:
        """Find potential duplicate tracks (same title and artist)"""
        from collections import defaultdict
        groups = defaultdict(list)
        for track in self.tracks:
            key = (track.title.lower().strip(), track.artist.lower().strip())
            groups[key].append(track)
        return [tracks for tracks in groups.values() if len(tracks) > 1]
    
    def find_missing_files(self) -> List[Track]:
        """Find tracks whose files no longer exist"""
        missing = []
        for track in self.tracks:
            if not Path(track.path).exists():
                missing.append(track)
        return missing
    
    def remove_missing_files(self) -> int:
        """Remove tracks whose files no longer exist, returns count removed"""
        missing = self.find_missing_files()
        missing_paths = {t.path for t in missing}
        self.tracks = [t for t in self.tracks if t.path not in missing_paths]
        if missing:
            self._save()
        return len(missing)
