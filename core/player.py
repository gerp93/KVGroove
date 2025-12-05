"""
KVGroove Audio Player Engine
Handles audio playback using pygame mixer
"""

import pygame
from pathlib import Path
from typing import Optional, Callable
import threading
import time


class AudioPlayer:
    """Audio playback engine using pygame mixer"""
    
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        self.current_file: Optional[str] = None
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.volume: float = 0.7
        self._duration: float = 0
        self._position_offset: float = 0
        self._on_track_end: Optional[Callable] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_monitor: bool = False
        
        # Sleep timer
        self._sleep_timer: Optional[threading.Timer] = None
        self._sleep_time_remaining: float = 0
        self._sleep_start_time: float = 0
        self._on_sleep_timer_end: Optional[Callable] = None
        
        pygame.mixer.music.set_volume(self.volume)
    
    def load(self, file_path: str) -> bool:
        """Load an audio file for playback"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            pygame.mixer.music.load(str(path))
            self.current_file = str(path)
            self._position_offset = 0
            self._duration = self._get_duration(str(path))
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def _get_duration(self, file_path: str) -> float:
        """Get duration of audio file in seconds"""
        try:
            from mutagen import File
            audio = File(file_path)
            if audio is not None and audio.info:
                return audio.info.length
        except Exception:
            pass
        return 0
    
    def play(self) -> bool:
        """Start or resume playback"""
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play()
            self.is_playing = True
            self._start_monitor()
            return True
        except Exception as e:
            print(f"Error playing: {e}")
            return False
    
    def pause(self):
        """Pause playback"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
    
    def stop(self):
        """Stop playback"""
        self._stop_monitor = True
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self._position_offset = 0
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def get_volume(self) -> float:
        """Get current volume"""
        return self.volume
    
    def seek(self, position: float):
        """Seek to position in seconds"""
        if self.current_file:
            try:
                pygame.mixer.music.play(start=position)
                self._position_offset = position
                if self.is_paused:
                    pygame.mixer.music.pause()
            except Exception:
                pass
    
    def get_position(self) -> float:
        """Get current position in seconds"""
        if self.is_playing or self.is_paused:
            pos = pygame.mixer.music.get_pos() / 1000.0
            if pos >= 0:
                return self._position_offset + pos
        return 0
    
    def get_duration(self) -> float:
        """Get duration of current track in seconds"""
        return self._duration
    
    def is_track_playing(self) -> bool:
        """Check if track is currently playing"""
        return pygame.mixer.music.get_busy()
    
    def set_on_track_end(self, callback: Callable):
        """Set callback for when track ends"""
        self._on_track_end = callback
    
    def _start_monitor(self):
        """Start monitoring thread for track end"""
        self._stop_monitor = False
        if self._monitor_thread is None or not self._monitor_thread.is_alive():
            self._monitor_thread = threading.Thread(target=self._monitor_playback, daemon=True)
            self._monitor_thread.start()
    
    def _monitor_playback(self):
        """Monitor playback and call callback when track ends"""
        while not self._stop_monitor:
            time.sleep(0.1)
            if self.is_playing and not pygame.mixer.music.get_busy() and not self.is_paused:
                self.is_playing = False
                if self._on_track_end:
                    self._on_track_end()
                break
    
    def cleanup(self):
        """Clean up resources"""
        self._stop_monitor = True
        self.cancel_sleep_timer()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    
    # Sleep Timer Methods
    def set_sleep_timer(self, minutes: float, callback: Optional[Callable] = None):
        """Set a sleep timer to stop playback after X minutes"""
        self.cancel_sleep_timer()
        if minutes > 0:
            self._sleep_time_remaining = minutes * 60
            self._sleep_start_time = time.time()
            self._on_sleep_timer_end = callback
            self._sleep_timer = threading.Timer(minutes * 60, self._on_sleep_timer_triggered)
            self._sleep_timer.daemon = True
            self._sleep_timer.start()
    
    def cancel_sleep_timer(self):
        """Cancel the sleep timer"""
        if self._sleep_timer:
            self._sleep_timer.cancel()
            self._sleep_timer = None
        self._sleep_time_remaining = 0
        self._sleep_start_time = 0
    
    def get_sleep_timer_remaining(self) -> float:
        """Get remaining sleep timer time in seconds"""
        if self._sleep_timer and self._sleep_start_time > 0:
            elapsed = time.time() - self._sleep_start_time
            remaining = self._sleep_time_remaining - elapsed
            return max(0, remaining)
        return 0
    
    def is_sleep_timer_active(self) -> bool:
        """Check if sleep timer is active"""
        return self._sleep_timer is not None and self.get_sleep_timer_remaining() > 0
    
    def _on_sleep_timer_triggered(self):
        """Called when sleep timer expires"""
        self.stop()
        self._sleep_timer = None
        self._sleep_time_remaining = 0
        if self._on_sleep_timer_end:
            self._on_sleep_timer_end()
