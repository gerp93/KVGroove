"""
KVGroove Queue View
Panel for managing the play queue
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, List
from core.queue import PlayQueue
from core.library import Library, Track


class QueueView(ttk.Frame):
    """Queue management panel"""
    
    def __init__(self, parent, queue: PlayQueue, library: Library,
                 on_track_double_click: Callable[[int], None]):
        super().__init__(parent)
        
        self.queue = queue
        self.library = library
        self.on_track_double_click = on_track_double_click
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the queue view widgets"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header, text="Up Next", 
                  font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        clear_btn = ttk.Button(header, text="Clear", command=self._clear_queue)
        clear_btn.pack(side=tk.RIGHT, padx=2)
        
        # Now playing indicator
        now_playing_frame = ttk.Frame(self)
        now_playing_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        ttk.Label(now_playing_frame, text="Now Playing:", 
                  font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        self.now_playing_var = tk.StringVar(value="Nothing playing")
        now_playing_label = ttk.Label(now_playing_frame, 
                                      textvariable=self.now_playing_var,
                                      font=('Segoe UI', 9, 'italic'))
        now_playing_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Queue list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('index', 'title', 'artist')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings',
                                  selectmode='extended')
        
        self.tree.heading('index', text='#')
        self.tree.heading('title', text='Title')
        self.tree.heading('artist', text='Artist')
        
        self.tree.column('index', width=30, minwidth=30)
        self.tree.column('title', width=180, minwidth=100)
        self.tree.column('artist', width=120, minwidth=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bindings
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<Button-3>', self._show_context_menu)
        self.tree.bind('<Delete>', lambda e: self._remove_selected())
        
        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Play", command=self._play_selected)
        self.context_menu.add_command(label="Play Next", 
                                      command=self._move_to_next)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Remove", 
                                      command=self._remove_selected)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var,
                                 font=('Segoe UI', 9))
        status_label.pack(fill=tk.X, padx=5, pady=(0, 5))
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in mm:ss"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def refresh(self):
        """Refresh the queue display"""
        self.tree.delete(*self.tree.get_children())
        
        queue_tracks = self.queue.get_queue()
        current_idx = self.queue.get_current_index()
        
        for i, track_path in enumerate(queue_tracks):
            track = self.library.get_track_by_path(track_path)
            
            # Determine display index (relative to current)
            if i == current_idx:
                display_idx = "▶"
            elif i > current_idx:
                display_idx = str(i - current_idx)
            else:
                display_idx = ""
            
            if track:
                title = track.title
                artist = track.artist
            else:
                title = track_path.split('\\')[-1].split('/')[-1]
                artist = "Unknown"
            
            item = self.tree.insert('', tk.END, values=(display_idx, title, artist))
            
            # Highlight current track
            if i == current_idx:
                self.tree.item(item, tags=('current',))
        
        # Configure tag styling
        self.tree.tag_configure('current', background='#e3f2fd')
        
        # Update status
        upcoming = len(self.queue.get_upcoming())
        self.status_var.set(f"{upcoming} tracks in queue")
        
        # Update now playing
        current = self.queue.get_current()
        if current:
            track = self.library.get_track_by_path(current)
            if track:
                self.now_playing_var.set(f"{track.title} - {track.artist}")
            else:
                self.now_playing_var.set(current.split('\\')[-1].split('/')[-1])
        else:
            self.now_playing_var.set("Nothing playing")
    
    def _on_double_click(self, event=None):
        """Handle double-click on track"""
        selection = self.tree.selection()
        if selection:
            idx = self.tree.index(selection[0])
            self.on_track_double_click(idx)
    
    def _show_context_menu(self, event):
        """Show context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            if item not in self.tree.selection():
                self.tree.selection_set(item)
            self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def _play_selected(self):
        """Play selected track"""
        selection = self.tree.selection()
        if selection:
            idx = self.tree.index(selection[0])
            self.on_track_double_click(idx)
    
    def _move_to_next(self):
        """Move selected track to play next"""
        selection = self.tree.selection()
        if selection:
            idx = self.tree.index(selection[0])
            current_idx = self.queue.get_current_index()
            if idx > current_idx + 1:
                self.queue.move_track(idx, current_idx + 1)
                self.refresh()
    
    def _remove_selected(self):
        """Remove selected tracks from queue"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get indices in reverse order
        indices = sorted([self.tree.index(item) for item in selection],
                        reverse=True)
        
        for idx in indices:
            self.queue.remove(idx)
        
        self.refresh()
    
    def _clear_queue(self):
        """Clear the queue"""
        # Keep current track, clear the rest
        current = self.queue.get_current()
        self.queue.clear()
        if current:
            self.queue.add(current)
            self.queue.play_index(0)
        self.refresh()
    
    def set_now_playing(self, track: Optional[Track]):
        """Update the now playing display"""
        if track:
            self.now_playing_var.set(f"{track.title} - {track.artist}")
        else:
            self.now_playing_var.set("Nothing playing")
