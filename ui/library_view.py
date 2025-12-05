"""
KVGroove Library View
Panel for browsing and managing the music library
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional, List
from core.library import Library, Track
from core.settings import SettingsManager
from ui.track_editor import TrackEditorDialog


class LibraryView(ttk.Frame):
    """Library browser panel"""
    
    def __init__(self, parent, library: Library, 
                 on_track_double_click: Callable[[Track], None],
                 on_add_to_queue: Callable[[Track], None],
                 on_add_to_playlist: Callable[[Track, str], None],
                 get_playlists: Callable[[], List[str]],
                 settings: Optional[SettingsManager] = None):
        super().__init__(parent)
        
        self.library = library
        self.on_track_double_click = on_track_double_click
        self.on_add_to_queue = on_add_to_queue
        self.on_add_to_playlist = on_add_to_playlist
        self.get_playlists = get_playlists
        self.settings = settings
        self.displayed_tracks: List[Track] = []
        self.current_view = "all"  # "all", "favorites", "recent", "folder"
        self.current_folder = None
        
        self._create_widgets()
        self._refresh_list()
    
    def _create_widgets(self):
        """Create the library view widgets"""
        # Header with controls
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header, text="Library", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Add folder button
        add_btn = ttk.Button(header, text="+ Add Folder", command=self._add_folder)
        add_btn.pack(side=tk.RIGHT, padx=2)
        
        # Refresh button
        refresh_btn = ttk.Button(header, text="↻ Refresh", command=self._refresh_library)
        refresh_btn.pack(side=tk.RIGHT, padx=2)
        
        # More options menu button
        more_btn = ttk.Menubutton(header, text="☰")
        more_btn.pack(side=tk.RIGHT, padx=2)
        
        more_menu = tk.Menu(more_btn, tearoff=0)
        more_btn['menu'] = more_menu
        more_menu.add_command(label="Find Duplicates...", command=self._show_duplicates)
        more_menu.add_command(label="Find Missing Files...", command=self._show_missing)
        more_menu.add_separator()
        more_menu.add_command(label="Remove Missing Files", command=self._remove_missing)
        
        # View filter buttons
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.view_var = tk.StringVar(value="all")
        
        ttk.Radiobutton(filter_frame, text="All", value="all", 
                       variable=self.view_var, command=self._on_view_change).pack(side=tk.LEFT)
        ttk.Radiobutton(filter_frame, text="★ Favorites", value="favorites",
                       variable=self.view_var, command=self._on_view_change).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(filter_frame, text="⏱ Recent", value="recent",
                       variable=self.view_var, command=self._on_view_change).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(filter_frame, text="📁 Folders", value="folder",
                       variable=self.view_var, command=self._on_view_change).pack(side=tk.LEFT, padx=(10, 0))
        
        # Search bar
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._on_search())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(5, 0))
        
        clear_btn = ttk.Button(search_frame, text="✕", width=3, 
                               command=lambda: self.search_var.set(""))
        clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Folder browser (hidden by default)
        self.folder_frame = ttk.Frame(self)
        
        folder_list_frame = ttk.Frame(self.folder_frame)
        folder_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.folder_listbox = tk.Listbox(folder_list_frame, height=6)
        folder_scroll = ttk.Scrollbar(folder_list_frame, orient=tk.VERTICAL,
                                      command=self.folder_listbox.yview)
        self.folder_listbox.configure(yscrollcommand=folder_scroll.set)
        self.folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        folder_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.folder_listbox.bind('<<ListboxSelect>>', self._on_folder_select)
        
        # Track list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for tracks
        columns = ('fav', 'title', 'artist', 'album', 'duration')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                  selectmode='extended')
        
        self.tree.heading('fav', text='★', command=lambda: self._sort_by('fav'))
        self.tree.heading('title', text='Title', command=lambda: self._sort_by('title'))
        self.tree.heading('artist', text='Artist', command=lambda: self._sort_by('artist'))
        self.tree.heading('album', text='Album', command=lambda: self._sort_by('album'))
        self.tree.heading('duration', text='Duration', command=lambda: self._sort_by('duration'))
        
        self.tree.column('fav', width=30, minwidth=30)
        self.tree.column('title', width=200, minwidth=100)
        self.tree.column('artist', width=150, minwidth=80)
        self.tree.column('album', width=150, minwidth=80)
        self.tree.column('duration', width=60, minwidth=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bindings
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<Return>', self._on_double_click)
        self.tree.bind('<Button-3>', self._show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Play", command=self._play_selected)
        self.context_menu.add_command(label="Add to Queue", command=self._add_selected_to_queue)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="★ Toggle Favorite", command=self._toggle_favorite)
        self.context_menu.add_separator()
        self.playlist_menu = tk.Menu(self.context_menu, tearoff=0)
        self.context_menu.add_cascade(label="Add to Playlist", menu=self.playlist_menu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit Track Info...", command=self._edit_selected_track)
        
        # Sort state
        self._sort_column = 'title'
        self._sort_reverse = False
        
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
    
    def _on_view_change(self):
        """Handle view mode change"""
        view = self.view_var.get()
        self.current_view = view
        
        if view == "folder":
            self.folder_frame.pack(fill=tk.X, padx=5, pady=(0, 5), before=self.tree.master)
            self._populate_folders()
        else:
            self.folder_frame.pack_forget()
        
        self._refresh_list()
    
    def _populate_folders(self):
        """Populate folder list"""
        self.folder_listbox.delete(0, tk.END)
        folders = self.library.get_folder_structure()
        for folder in sorted(folders.keys()):
            count = len(folders[folder])
            # Show just the folder name, not full path
            from pathlib import Path
            name = Path(folder).name or folder
            self.folder_listbox.insert(tk.END, f"📁 {name} ({count})")
        self._folder_paths = list(sorted(folders.keys()))
    
    def _on_folder_select(self, event=None):
        """Handle folder selection"""
        selection = self.folder_listbox.curselection()
        if selection and hasattr(self, '_folder_paths'):
            idx = selection[0]
            if 0 <= idx < len(self._folder_paths):
                self.current_folder = self._folder_paths[idx]
                self._refresh_list()
    
    def _refresh_list(self, tracks: Optional[List[Track]] = None):
        """Refresh the track list display"""
        self.tree.delete(*self.tree.get_children())
        
        if tracks is None:
            view = self.current_view
            
            if view == "favorites" and self.settings:
                fav_paths = self.settings.get_favorites()
                tracks = self.library.get_tracks_by_paths(fav_paths)
            elif view == "recent" and self.settings:
                recent_paths = self.settings.get_recently_played()
                tracks = self.library.get_tracks_by_paths(recent_paths)
            elif view == "folder" and self.current_folder:
                tracks = self.library.get_tracks_by_folder(self.current_folder)
            else:
                tracks = self.library.get_all_tracks()
        
        self.displayed_tracks = tracks
        
        for track in tracks:
            is_fav = self.settings.is_favorite(track.path) if self.settings else False
            fav_icon = "★" if is_fav else ""
            self.tree.insert('', tk.END, values=(
                fav_icon,
                track.title,
                track.artist,
                track.album,
                self._format_duration(track.duration)
            ))
        
        self.status_var.set(f"{len(tracks)} tracks")
    
    def _toggle_favorite(self):
        """Toggle favorite status for selected tracks"""
        if not self.settings:
            return
        for track in self._get_selected_tracks():
            self.settings.toggle_favorite(track.path)
        self._refresh_list()
    
    def _show_duplicates(self):
        """Show duplicate tracks dialog"""
        duplicates = self.library.find_duplicates()
        if not duplicates:
            messagebox.showinfo("No Duplicates", "No duplicate tracks found.",
                              parent=self.winfo_toplevel())
            return
        
        msg = f"Found {len(duplicates)} potential duplicate groups:\n\n"
        for i, group in enumerate(duplicates[:10], 1):
            msg += f"{i}. {group[0].title} - {group[0].artist}\n"
            for track in group:
                msg += f"   • {track.path}\n"
            msg += "\n"
        
        if len(duplicates) > 10:
            msg += f"... and {len(duplicates) - 10} more groups"
        
        messagebox.showinfo("Duplicate Tracks", msg, parent=self.winfo_toplevel())
    
    def _show_missing(self):
        """Show missing files dialog"""
        missing = self.library.find_missing_files()
        if not missing:
            messagebox.showinfo("No Missing Files", "All files are accessible.",
                              parent=self.winfo_toplevel())
            return
        
        msg = f"Found {len(missing)} missing files:\n\n"
        for track in missing[:20]:
            msg += f"• {track.title} - {track.path}\n"
        
        if len(missing) > 20:
            msg += f"\n... and {len(missing) - 20} more"
        
        messagebox.showwarning("Missing Files", msg, parent=self.winfo_toplevel())
    
    def _remove_missing(self):
        """Remove missing files from library"""
        missing = self.library.find_missing_files()
        if not missing:
            messagebox.showinfo("No Missing Files", "All files are accessible.",
                              parent=self.winfo_toplevel())
            return
        
        if messagebox.askyesno("Remove Missing Files",
                              f"Remove {len(missing)} missing files from library?",
                              parent=self.winfo_toplevel()):
            removed = self.library.remove_missing_files()
            self._refresh_list()
            messagebox.showinfo("Removed", f"Removed {removed} missing files.",
                              parent=self.winfo_toplevel())
    
    def _add_folder(self):
        """Open folder dialog and add to library"""
        folder = filedialog.askdirectory(title="Select Music Folder")
        if folder:
            added = self.library.add_folder(folder)
            self._refresh_list()
            messagebox.showinfo("Library Updated", 
                              f"Added {added} tracks from folder.")
    
    def _refresh_library(self):
        """Refresh the entire library"""
        self.library.refresh()
        self._refresh_list()
    
    def _on_search(self):
        """Handle search input"""
        query = self.search_var.get().strip()
        if query:
            tracks = self.library.search(query)
        else:
            tracks = self.library.get_all_tracks()
        self._refresh_list(tracks)
    
    def _sort_by(self, column: str):
        """Sort the list by column"""
        if self._sort_column == column:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_column = column
            self._sort_reverse = False
        
        tracks = self.displayed_tracks.copy()
        
        if column == 'duration':
            tracks.sort(key=lambda t: t.duration, reverse=self._sort_reverse)
        else:
            tracks.sort(key=lambda t: getattr(t, column, '').lower(), 
                       reverse=self._sort_reverse)
        
        self._refresh_list(tracks)
    
    def _get_selected_tracks(self) -> List[Track]:
        """Get currently selected tracks"""
        selected = []
        for item in self.tree.selection():
            idx = self.tree.index(item)
            if 0 <= idx < len(self.displayed_tracks):
                selected.append(self.displayed_tracks[idx])
        return selected
    
    def _on_double_click(self, event=None):
        """Handle double-click on track"""
        tracks = self._get_selected_tracks()
        if tracks:
            self.on_track_double_click(tracks[0])
    
    def _show_context_menu(self, event):
        """Show right-click context menu"""
        # Select item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            if item not in self.tree.selection():
                self.tree.selection_set(item)
            
            # Update playlist submenu
            self.playlist_menu.delete(0, tk.END)
            for playlist_name in self.get_playlists():
                self.playlist_menu.add_command(
                    label=playlist_name,
                    command=lambda name=playlist_name: self._add_to_playlist(name)
                )
            
            self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def _play_selected(self):
        """Play selected track"""
        tracks = self._get_selected_tracks()
        if tracks:
            self.on_track_double_click(tracks[0])
    
    def _add_selected_to_queue(self):
        """Add selected tracks to queue"""
        for track in self._get_selected_tracks():
            self.on_add_to_queue(track)
    
    def _add_to_playlist(self, playlist_name: str):
        """Add selected tracks to a playlist"""
        for track in self._get_selected_tracks():
            self.on_add_to_playlist(track, playlist_name)
    
    def _edit_selected_track(self):
        """Open edit dialog for selected track"""
        tracks = self._get_selected_tracks()
        if tracks:
            # Get the parent window (main window root)
            parent = self.winfo_toplevel()
            TrackEditorDialog(parent, tracks[0], self.library, 
                            on_save=lambda t: self._refresh_list())
    
    def refresh(self):
        """Public method to refresh the view"""
        self._refresh_list()
