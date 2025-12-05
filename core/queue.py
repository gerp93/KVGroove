"""
KVGroove Queue Management
Handles the play queue (up next) functionality
"""

from typing import List, Optional
from .library import Track
import random


class PlayQueue:
    """Manages the play queue"""
    
    def __init__(self):
        self._queue: List[str] = []  # List of file paths
        self._history: List[str] = []  # Played tracks for going back
        self._current_index: int = -1
        self._shuffle: bool = False
        self._repeat: str = "none"  # "none", "one", "all"
        self._original_queue: List[str] = []  # For unshuffle
    
    def add(self, track_path: str):
        """Add a track to the end of the queue"""
        self._queue.append(track_path)
        if not self._shuffle:
            self._original_queue.append(track_path)
    
    def add_next(self, track_path: str):
        """Add a track to play next (after current)"""
        insert_pos = self._current_index + 1 if self._current_index >= 0 else 0
        self._queue.insert(insert_pos, track_path)
        if not self._shuffle:
            self._original_queue.insert(insert_pos, track_path)
    
    def add_multiple(self, track_paths: List[str]):
        """Add multiple tracks to the queue"""
        self._queue.extend(track_paths)
        if not self._shuffle:
            self._original_queue.extend(track_paths)
    
    def remove(self, index: int) -> Optional[str]:
        """Remove a track from the queue by index"""
        if 0 <= index < len(self._queue):
            track = self._queue.pop(index)
            if index < self._current_index:
                self._current_index -= 1
            elif index == self._current_index:
                self._current_index = min(self._current_index, len(self._queue) - 1)
            return track
        return None
    
    def clear(self):
        """Clear the entire queue"""
        self._queue = []
        self._original_queue = []
        self._current_index = -1
        self._history = []
    
    def get_current(self) -> Optional[str]:
        """Get the current track"""
        if 0 <= self._current_index < len(self._queue):
            return self._queue[self._current_index]
        return None
    
    def get_next(self) -> Optional[str]:
        """Move to and return the next track"""
        if self._repeat == "one":
            return self.get_current()
        
        if self._current_index >= 0:
            current = self.get_current()
            if current:
                self._history.append(current)
        
        if self._current_index < len(self._queue) - 1:
            self._current_index += 1
            return self.get_current()
        elif self._repeat == "all" and len(self._queue) > 0:
            self._current_index = 0
            return self.get_current()
        
        return None
    
    def get_previous(self) -> Optional[str]:
        """Move to and return the previous track"""
        if self._history:
            current = self.get_current()
            if self._current_index > 0:
                self._current_index -= 1
            self._history.pop()
            return self.get_current()
        elif self._current_index > 0:
            self._current_index -= 1
            return self.get_current()
        elif self._repeat == "all" and len(self._queue) > 0:
            self._current_index = len(self._queue) - 1
            return self.get_current()
        
        return None
    
    def play_index(self, index: int) -> Optional[str]:
        """Play a specific track in the queue by index"""
        if 0 <= index < len(self._queue):
            if self._current_index >= 0:
                current = self.get_current()
                if current:
                    self._history.append(current)
            self._current_index = index
            return self.get_current()
        return None
    
    def set_shuffle(self, enabled: bool):
        """Enable or disable shuffle mode"""
        if enabled and not self._shuffle:
            # Shuffle the queue but keep current track position
            self._original_queue = self._queue.copy()
            current = self.get_current()
            remaining = self._queue[self._current_index + 1:] if self._current_index >= 0 else self._queue
            random.shuffle(remaining)
            if self._current_index >= 0:
                self._queue = self._queue[:self._current_index + 1] + remaining
            else:
                self._queue = remaining
        elif not enabled and self._shuffle:
            # Restore original order
            current = self.get_current()
            self._queue = self._original_queue.copy()
            if current and current in self._queue:
                self._current_index = self._queue.index(current)
        
        self._shuffle = enabled
    
    def is_shuffle(self) -> bool:
        """Check if shuffle is enabled"""
        return self._shuffle
    
    def set_repeat(self, mode: str):
        """Set repeat mode: 'none', 'one', or 'all'"""
        if mode in ("none", "one", "all"):
            self._repeat = mode
    
    def get_repeat(self) -> str:
        """Get current repeat mode"""
        return self._repeat
    
    def get_queue(self) -> List[str]:
        """Get the current queue"""
        return self._queue.copy()
    
    def get_upcoming(self) -> List[str]:
        """Get tracks after current position"""
        if self._current_index >= 0:
            return self._queue[self._current_index + 1:]
        return self._queue.copy()
    
    def move_track(self, from_index: int, to_index: int):
        """Move a track within the queue"""
        if 0 <= from_index < len(self._queue) and 0 <= to_index < len(self._queue):
            track = self._queue.pop(from_index)
            self._queue.insert(to_index, track)
            
            # Adjust current index if needed
            if from_index == self._current_index:
                self._current_index = to_index
            elif from_index < self._current_index <= to_index:
                self._current_index -= 1
            elif to_index <= self._current_index < from_index:
                self._current_index += 1
    
    def __len__(self) -> int:
        return len(self._queue)
    
    def get_current_index(self) -> int:
        """Get current track index"""
        return self._current_index
    
    def shuffle_remaining(self):
        """Shuffle only the remaining tracks (after current)"""
        if self._current_index >= 0 and self._current_index < len(self._queue) - 1:
            remaining = self._queue[self._current_index + 1:]
            random.shuffle(remaining)
            self._queue = self._queue[:self._current_index + 1] + remaining
    
    def clear_upcoming(self):
        """Clear only upcoming tracks, keep current and history"""
        if self._current_index >= 0:
            self._queue = self._queue[:self._current_index + 1]
    
    def to_list(self) -> List[str]:
        """Get queue as a simple list of paths"""
        return self._queue.copy()
