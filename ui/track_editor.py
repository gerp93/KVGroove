"""
KVGroove Track Editor Dialog
Edit track metadata (title, artist, album) and optionally save to file
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from pathlib import Path

from core.library import Track, Library


class TrackEditorDialog:
    """Dialog for editing track metadata"""
    
    def __init__(self, parent: tk.Tk, track: Track, library: Library,
                 on_save: Optional[Callable[[Track], None]] = None):
        self.track = track
        self.library = library
        self.on_save = on_save
        self.parent = parent
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Track")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 450) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 350) // 2
        self.dialog.geometry(f"450x350+{x}+{y}")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Edit Track Metadata",
                                font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # File path (read-only)
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(path_frame, text="File:", width=8).pack(side=tk.LEFT)
        path_label = ttk.Label(path_frame, text=self._truncate_path(self.track.path),
                               font=('Segoe UI', 9), foreground='gray')
        path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Title field
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(title_frame, text="Title:", width=8).pack(side=tk.LEFT)
        self.title_var = tk.StringVar(value=self.track.title)
        ttk.Entry(title_frame, textvariable=self.title_var, 
                  font=('Segoe UI', 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Artist field
        artist_frame = ttk.Frame(main_frame)
        artist_frame.pack(fill=tk.X, pady=5)
        ttk.Label(artist_frame, text="Artist:", width=8).pack(side=tk.LEFT)
        self.artist_var = tk.StringVar(value=self.track.artist)
        ttk.Entry(artist_frame, textvariable=self.artist_var,
                  font=('Segoe UI', 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Album field
        album_frame = ttk.Frame(main_frame)
        album_frame.pack(fill=tk.X, pady=5)
        ttk.Label(album_frame, text="Album:", width=8).pack(side=tk.LEFT)
        self.album_var = tk.StringVar(value=self.track.album)
        ttk.Entry(album_frame, textvariable=self.album_var,
                  font=('Segoe UI', 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Save to file checkbox
        self.save_to_file_var = tk.BooleanVar(value=True)
        save_check = ttk.Checkbutton(main_frame, 
                                     text="Also save changes to the audio file metadata",
                                     variable=self.save_to_file_var)
        save_check.pack(anchor=tk.W, pady=(15, 5))
        
        # Note about file metadata
        note_label = ttk.Label(main_frame, 
                               text="Note: Saving to file modifies the actual audio file's ID3/metadata tags.",
                               font=('Segoe UI', 8), foreground='gray')
        note_label.pack(anchor=tk.W)
        
        # Buttons - use tk.Frame to avoid ttk styling issues
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(25, 10))
        
        save_btn = tk.Button(btn_frame, text="Save", width=12, font=('Segoe UI', 9),
                             command=self._on_save)
        save_btn.pack(side=tk.RIGHT, padx=(5, 0), ipady=3)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", width=12, font=('Segoe UI', 9),
                               command=self.dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, ipady=3)
    
    def _truncate_path(self, path: str, max_len: int = 50) -> str:
        """Truncate path for display"""
        if len(path) <= max_len:
            return path
        return "..." + path[-(max_len - 3):]
    
    def _on_save(self):
        """Save changes"""
        new_title = self.title_var.get().strip()
        new_artist = self.artist_var.get().strip()
        new_album = self.album_var.get().strip()
        
        if not new_title:
            messagebox.showwarning("Title Required", 
                                   "Title cannot be empty.",
                                   parent=self.dialog)
            return
        
        # Check if anything changed
        changed = (new_title != self.track.title or 
                   new_artist != self.track.artist or 
                   new_album != self.track.album)
        
        if not changed:
            self.dialog.destroy()
            return
        
        # Save to file if requested
        if self.save_to_file_var.get():
            success = self._save_to_file(new_title, new_artist, new_album)
            if not success:
                if not messagebox.askyesno("File Update Failed",
                                           "Could not update the audio file metadata.\n"
                                           "Save changes to library only?",
                                           parent=self.dialog):
                    return
        
        # Update track object
        self.track.title = new_title
        self.track.artist = new_artist
        self.track.album = new_album
        
        # Update library
        self._update_library()
        
        # Call callback
        if self.on_save:
            self.on_save(self.track)
        
        messagebox.showinfo("Saved", "Track metadata updated successfully!",
                           parent=self.dialog)
        self.dialog.destroy()
    
    def _save_to_file(self, title: str, artist: str, album: str) -> bool:
        """Save metadata to the actual audio file"""
        try:
            from mutagen import File
            from mutagen.easyid3 import EasyID3
            from mutagen.mp3 import MP3
            from mutagen.flac import FLAC
            from mutagen.id3 import ID3, TIT2, TPE1, TALB
            
            path = Path(self.track.path)
            suffix = path.suffix.lower()
            
            if suffix == '.mp3':
                try:
                    audio = EasyID3(self.track.path)
                except Exception:
                    # No ID3 tag, create one
                    audio = MP3(self.track.path)
                    audio.add_tags()
                    audio.save()
                    audio = EasyID3(self.track.path)
                
                audio['title'] = title
                audio['artist'] = artist
                audio['album'] = album
                audio.save()
                
            elif suffix == '.flac':
                audio = FLAC(self.track.path)
                audio['title'] = title
                audio['artist'] = artist
                audio['album'] = album
                audio.save()
                
            elif suffix in ('.ogg', '.m4a'):
                audio = File(self.track.path)
                if audio is not None and audio.tags is not None:
                    # Try common tag names
                    audio.tags['title'] = title
                    audio.tags['artist'] = artist
                    audio.tags['album'] = album
                    audio.save()
                else:
                    return False
            else:
                # Unsupported format for writing
                return False
            
            return True
            
        except Exception as e:
            print(f"Error saving metadata to file: {e}")
            return False
    
    def _update_library(self):
        """Update the track in the library"""
        for i, t in enumerate(self.library.tracks):
            if t.path == self.track.path:
                self.library.tracks[i] = self.track
                break
        self.library._save()
