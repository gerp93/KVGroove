"""
KVGroove Playlist View
Panel for managing playlists
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import Callable, Optional, List
from core.playlist import PlaylistManager, Playlist
from core.library import Library, Track


class PlaylistView(ttk.Frame):
    """Playlist management panel"""
    
    def __init__(self, parent, playlist_manager: PlaylistManager, library: Library,
                 on_track_double_click: Callable[[Track], None],
                 on_play_playlist: Callable[[List[str]], None]):
        super().__init__(parent)
        
        self.playlist_manager = playlist_manager
        self.library = library
        self.on_track_double_click = on_track_double_click
        self.on_play_playlist = on_play_playlist
        self.current_playlist: Optional[Playlist] = None
        
        self._create_widgets()
        self._refresh_playlist_list()
    
    def _create_widgets(self):
        """Create the playlist view widgets"""
        # Use a PanedWindow for resizable sections
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel: Playlist list
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Playlist list header
        list_header = ttk.Frame(left_frame)
        list_header.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(list_header, text="Playlists", 
                  font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        add_btn = ttk.Button(list_header, text="+", width=3, 
                            command=self._create_playlist)
        add_btn.pack(side=tk.RIGHT)
        
        # Playlist listbox
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.playlist_listbox = tk.Listbox(list_container, selectmode=tk.SINGLE,
                                           font=('Segoe UI', 10))
        playlist_scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL,
                                        command=self.playlist_listbox.yview)
        self.playlist_listbox.configure(yscrollcommand=playlist_scroll.set)
        
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        playlist_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_listbox.bind('<<ListboxSelect>>', self._on_playlist_select)
        self.playlist_listbox.bind('<Button-3>', self._show_playlist_context_menu)
        
        # Playlist context menu
        self.playlist_context_menu = tk.Menu(self, tearoff=0)
        self.playlist_context_menu.add_command(label="Play All", 
                                               command=self._play_current_playlist)
        self.playlist_context_menu.add_command(label="Rename", 
                                               command=self._rename_playlist)
        self.playlist_context_menu.add_separator()
        self.playlist_context_menu.add_command(label="Delete", 
                                               command=self._delete_playlist)
        
        # Right panel: Playlist tracks
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        # Track list header
        track_header = ttk.Frame(right_frame)
        track_header.pack(fill=tk.X, padx=5, pady=5)
        
        self.playlist_name_var = tk.StringVar(value="Select a playlist")
        ttk.Label(track_header, textvariable=self.playlist_name_var,
                  font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        play_all_btn = ttk.Button(track_header, text="▶ Play All",
                                  command=self._play_current_playlist)
        play_all_btn.pack(side=tk.RIGHT, padx=2)
        
        # Track list
        track_container = ttk.Frame(right_frame)
        track_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('title', 'artist', 'duration')
        self.track_tree = ttk.Treeview(track_container, columns=columns, 
                                        show='headings', selectmode='extended')
        
        self.track_tree.heading('title', text='Title')
        self.track_tree.heading('artist', text='Artist')
        self.track_tree.heading('duration', text='Duration')
        
        self.track_tree.column('title', width=200, minwidth=100)
        self.track_tree.column('artist', width=150, minwidth=80)
        self.track_tree.column('duration', width=60, minwidth=50)
        
        track_scroll = ttk.Scrollbar(track_container, orient=tk.VERTICAL,
                                     command=self.track_tree.yview)
        self.track_tree.configure(yscrollcommand=track_scroll.set)
        
        self.track_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        track_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.track_tree.bind('<Double-1>', self._on_track_double_click)
        self.track_tree.bind('<Button-3>', self._show_track_context_menu)
        self.track_tree.bind('<Delete>', lambda e: self._remove_selected_tracks())
        
        # Track context menu
        self.track_context_menu = tk.Menu(self, tearoff=0)
        self.track_context_menu.add_command(label="Play", 
                                            command=self._play_selected_track)
        self.track_context_menu.add_separator()
        self.track_context_menu.add_command(label="Remove from Playlist",
                                            command=self._remove_selected_tracks)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_label = ttk.Label(right_frame, textvariable=self.status_var,
                                 font=('Segoe UI', 9))
        status_label.pack(fill=tk.X, padx=5, pady=(0, 5))
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in mm:ss"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def _refresh_playlist_list(self):
        """Refresh the playlist list"""
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlist_manager.get_all_playlists():
            self.playlist_listbox.insert(tk.END, f"  {playlist.name}  ({len(playlist.tracks)})")
    
    def _refresh_track_list(self):
        """Refresh the track list for current playlist"""
        self.track_tree.delete(*self.track_tree.get_children())
        
        if not self.current_playlist:
            self.status_var.set("")
            return
        
        for track_path in self.current_playlist.tracks:
            track = self.library.get_track_by_path(track_path)
            if track:
                self.track_tree.insert('', tk.END, values=(
                    track.title,
                    track.artist,
                    self._format_duration(track.duration)
                ))
            else:
                # Track not in library anymore
                self.track_tree.insert('', tk.END, values=(
                    track_path.split('\\')[-1].split('/')[-1],
                    "Unknown",
                    "--:--"
                ))
        
        self.status_var.set(f"{len(self.current_playlist.tracks)} tracks")
    
    def _on_playlist_select(self, event=None):
        """Handle playlist selection"""
        selection = self.playlist_listbox.curselection()
        if selection:
            playlists = self.playlist_manager.get_all_playlists()
            if 0 <= selection[0] < len(playlists):
                self.current_playlist = playlists[selection[0]]
                self.playlist_name_var.set(self.current_playlist.name)
                self._refresh_track_list()
    
    def _create_playlist(self):
        """Create a new playlist"""
        name = simpledialog.askstring("New Playlist", "Enter playlist name:",
                                      parent=self)
        if name:
            self.playlist_manager.create_playlist(name)
            self._refresh_playlist_list()
    
    def _rename_playlist(self):
        """Rename the selected playlist"""
        if not self.current_playlist:
            return
        
        new_name = simpledialog.askstring("Rename Playlist", 
                                          "Enter new name:",
                                          initialvalue=self.current_playlist.name,
                                          parent=self)
        if new_name and new_name != self.current_playlist.name:
            if self.playlist_manager.rename_playlist(self.current_playlist.name, new_name):
                self.playlist_name_var.set(new_name)
                self._refresh_playlist_list()
            else:
                messagebox.showerror("Error", "A playlist with that name already exists.")
    
    def _delete_playlist(self):
        """Delete the selected playlist"""
        if not self.current_playlist:
            return
        
        if messagebox.askyesno("Delete Playlist", 
                               f"Delete playlist '{self.current_playlist.name}'?"):
            self.playlist_manager.delete_playlist(self.current_playlist.name)
            self.current_playlist = None
            self.playlist_name_var.set("Select a playlist")
            self._refresh_playlist_list()
            self._refresh_track_list()
    
    def _show_playlist_context_menu(self, event):
        """Show playlist context menu"""
        # Select item under cursor
        idx = self.playlist_listbox.nearest(event.y)
        if idx >= 0:
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(idx)
            self._on_playlist_select()
            self.playlist_context_menu.tk_popup(event.x_root, event.y_root)
    
    def _show_track_context_menu(self, event):
        """Show track context menu"""
        item = self.track_tree.identify_row(event.y)
        if item:
            if item not in self.track_tree.selection():
                self.track_tree.selection_set(item)
            self.track_context_menu.tk_popup(event.x_root, event.y_root)
    
    def _on_track_double_click(self, event=None):
        """Handle double-click on track"""
        if not self.current_playlist:
            return
        
        selection = self.track_tree.selection()
        if selection:
            idx = self.track_tree.index(selection[0])
            if 0 <= idx < len(self.current_playlist.tracks):
                track_path = self.current_playlist.tracks[idx]
                track = self.library.get_track_by_path(track_path)
                if track:
                    self.on_track_double_click(track)
    
    def _play_selected_track(self):
        """Play the selected track"""
        self._on_track_double_click()
    
    def _remove_selected_tracks(self):
        """Remove selected tracks from playlist"""
        if not self.current_playlist:
            return
        
        selection = self.track_tree.selection()
        if not selection:
            return
        
        # Get indices in reverse order to avoid index shifting
        indices = sorted([self.track_tree.index(item) for item in selection], 
                        reverse=True)
        
        for idx in indices:
            if 0 <= idx < len(self.current_playlist.tracks):
                track_path = self.current_playlist.tracks[idx]
                self.current_playlist.remove_track(track_path)
        
        self.playlist_manager.save()
        self._refresh_track_list()
        self._refresh_playlist_list()
    
    def _play_current_playlist(self):
        """Play all tracks in current playlist"""
        if self.current_playlist and self.current_playlist.tracks:
            self.on_play_playlist(self.current_playlist.tracks)
    
    def get_playlist_names(self) -> List[str]:
        """Get list of playlist names"""
        return [p.name for p in self.playlist_manager.get_all_playlists()]
    
    def add_track_to_playlist(self, track: Track, playlist_name: str):
        """Add a track to a playlist"""
        if self.playlist_manager.add_track_to_playlist(playlist_name, track.path):
            if self.current_playlist and self.current_playlist.name == playlist_name:
                self._refresh_track_list()
            self._refresh_playlist_list()
    
    def refresh(self):
        """Public method to refresh the view"""
        self._refresh_playlist_list()
        if self.current_playlist:
            # Re-fetch the playlist in case it was modified
            self.current_playlist = self.playlist_manager.get_playlist(
                self.current_playlist.name)
            self._refresh_track_list()
