"""
KVGroove Main Window
Main application window layout and controls
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from typing import Optional
import json
from pathlib import Path

from core.player import AudioPlayer
from core.library import Library, Track
from core.playlist import PlaylistManager
from core.queue import PlayQueue
from core.settings import SettingsManager
from ui.library_view import LibraryView
from ui.playlist_view import PlaylistView
from ui.queue_view import QueueView
from ui.login_dialog import PasswordSettingsDialog
from ui.dialogs import SettingsDialog, SleepTimerDialog, KeyboardShortcutsDialog, BackupRestoreDialog
from ui.themes import apply_theme, get_theme_list, THEMES


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KVGroove")
        self.root.geometry("1200x700")
        self.root.minsize(800, 500)
        
        # Set app icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except Exception:
            pass
        
        # Initialize core components
        self.player = AudioPlayer()
        self.library = Library()
        self.playlist_manager = PlaylistManager()
        self.queue = PlayQueue()
        self.settings_manager = SettingsManager()
        
        # Load settings
        self.settings = self._load_settings()
        self.player.set_volume(self.settings.get('volume', 0.7))
        self.queue.set_shuffle(self.settings.get('shuffle', False))
        self.queue.set_repeat(self.settings.get('repeat', 'none'))
        
        # Current track info
        self.current_track: Optional[Track] = None
        self.is_muted: bool = False
        self.pre_mute_volume: float = 0.7
        
        # Theme
        self.current_theme = self.settings_manager.get('theme', 'light')
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        self._setup_bindings()
        self._apply_theme()
        
        # Set callback for track end
        self.player.set_on_track_end(self._on_track_end)
        
        # Start position update loop
        self._update_position()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _load_settings(self) -> dict:
        """Load settings from file"""
        try:
            settings_path = Path("data/settings.json")
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            'volume': 0.7,
            'shuffle': False,
            'repeat': 'none'
        }
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            settings_path = Path("data/settings.json")
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings = {
                'volume': self.player.get_volume(),
                'shuffle': self.queue.is_shuffle(),
                'repeat': self.queue.get_repeat(),
                'window_width': self.root.winfo_width(),
                'window_height': self.root.winfo_height()
            }
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5')
        style.configure('TButton', padding=5)
        style.configure('Control.TButton', padding=10, font=('Segoe UI', 14))
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Create menu bar
        self._create_menu_bar()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top: Playback controls and now playing
        self._create_control_bar(main_container)
        
        # Middle: Content area with tabs
        self._create_content_area(main_container)
    
    def _create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Rescan Library", command=self._rescan_library)
        file_menu.add_separator()
        file_menu.add_command(label="Import Playlist...", command=self._import_playlist)
        file_menu.add_command(label="Export Playlist...", command=self._export_playlist)
        file_menu.add_separator()
        file_menu.add_command(label="Backup Data...", command=self._show_backup_restore)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        
        # Playback menu
        playback_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Playback", menu=playback_menu)
        playback_menu.add_command(label="Play/Pause", command=self._toggle_play, accelerator="Space")
        playback_menu.add_command(label="Stop", command=self._stop)
        playback_menu.add_command(label="Next Track", command=self._next_track, accelerator="Ctrl+Right")
        playback_menu.add_command(label="Previous Track", command=self._previous_track, accelerator="Ctrl+Left")
        playback_menu.add_separator()
        playback_menu.add_command(label="Mute/Unmute", command=self._toggle_mute, accelerator="M")
        playback_menu.add_separator()
        playback_menu.add_command(label="Sleep Timer...", command=self._show_sleep_timer)
        
        # Queue menu
        queue_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Queue", menu=queue_menu)
        queue_menu.add_command(label="Shuffle Remaining", command=self._shuffle_remaining)
        queue_menu.add_command(label="Clear Upcoming", command=self._clear_upcoming)
        queue_menu.add_command(label="Clear All", command=self._clear_queue)
        queue_menu.add_separator()
        queue_menu.add_command(label="Save as Playlist...", command=self._save_queue_as_playlist)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        self.theme_var = tk.StringVar(value=self.current_theme)
        
        # Add all themes from registry
        for theme_id, theme_info in THEMES.items():
            view_menu.add_radiobutton(label=theme_info["name"], variable=self.theme_var, 
                                      value=theme_id, command=self._apply_theme)
        
        view_menu.add_separator()
        view_menu.add_command(label="Show Duplicates...", command=self._show_duplicates)
        view_menu.add_command(label="Check Missing Files...", command=self._show_missing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences...", command=self._show_settings)
        settings_menu.add_command(label="Password...", command=self._open_password_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_keyboard_shortcuts, accelerator="F1")
        help_menu.add_separator()
        help_menu.add_command(label="About KVGroove", command=self._show_about)
    
    def _open_password_settings(self):
        """Open password settings dialog"""
        PasswordSettingsDialog(self.root)
    
    def _rescan_library(self):
        """Rescan the music library"""
        self.library.scan()
        self.library_view.refresh()
        messagebox.showinfo("Library Scan", "Library scan complete!")
    
    def _import_playlist(self):
        """Import a playlist from M3U/PLS file"""
        filetypes = [("M3U Playlist", "*.m3u"), ("PLS Playlist", "*.pls"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(title="Import Playlist", filetypes=filetypes)
        if filepath:
            try:
                if filepath.lower().endswith('.m3u'):
                    name, paths = self.playlist_manager.import_playlist_m3u(filepath)
                else:
                    name, paths = self.playlist_manager.import_playlist_pls(filepath)
                messagebox.showinfo("Import", f"Imported playlist '{name}' with {len(paths)} tracks")
                self.playlist_view.refresh()
            except Exception as e:
                messagebox.showerror("Import Error", str(e))
    
    def _export_playlist(self):
        """Export a playlist to M3U/PLS file"""
        playlists = self.playlist_manager.list_playlists()
        if not playlists:
            messagebox.showinfo("Export", "No playlists to export")
            return
        
        # Simple dialog to select playlist
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Playlist")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select playlist:").pack(pady=10)
        playlist_var = tk.StringVar(value=playlists[0])
        combo = ttk.Combobox(dialog, textvariable=playlist_var, values=playlists, state='readonly')
        combo.pack(pady=5)
        
        format_var = tk.StringVar(value="m3u")
        ttk.Radiobutton(dialog, text="M3U", variable=format_var, value="m3u").pack()
        ttk.Radiobutton(dialog, text="PLS", variable=format_var, value="pls").pack()
        
        def do_export():
            name = playlist_var.get()
            fmt = format_var.get()
            filetypes = [("M3U Playlist", "*.m3u")] if fmt == "m3u" else [("PLS Playlist", "*.pls")]
            filepath = filedialog.asksaveasfilename(title="Save Playlist", 
                                                     defaultextension=f".{fmt}",
                                                     filetypes=filetypes)
            if filepath:
                tracks = self.playlist_manager.get_playlist_tracks(name)
                if fmt == "m3u":
                    self.playlist_manager.export_playlist_m3u(name, tracks, filepath)
                else:
                    self.playlist_manager.export_playlist_pls(name, tracks, filepath)
                messagebox.showinfo("Export", f"Playlist exported to {filepath}")
            dialog.destroy()
        
        tk.Button(dialog, text="Export", command=do_export, font=('Segoe UI', 10)).pack(pady=10)
    
    def _show_backup_restore(self):
        """Show backup/restore dialog"""
        BackupRestoreDialog(self.root, self.settings_manager)
    
    def _toggle_mute(self):
        """Toggle mute state"""
        if self.is_muted:
            self.player.set_volume(self.pre_mute_volume / 100)
            self.volume_var.set(self.pre_mute_volume)
            self.is_muted = False
        else:
            self.pre_mute_volume = self.volume_var.get()
            self.player.set_volume(0)
            self.volume_var.set(0)
            self.is_muted = True
    
    def _show_sleep_timer(self):
        """Show sleep timer dialog"""
        SleepTimerDialog(self.root, self.player)
    
    def _shuffle_remaining(self):
        """Shuffle remaining tracks in queue"""
        self.queue.shuffle_remaining()
        self.queue_view.refresh()
    
    def _clear_upcoming(self):
        """Clear upcoming tracks in queue"""
        self.queue.clear_upcoming()
        self.queue_view.refresh()
    
    def _clear_queue(self):
        """Clear entire queue"""
        self.queue.clear()
        self.queue_view.refresh()
    
    def _save_queue_as_playlist(self):
        """Save current queue as a playlist"""
        if len(self.queue) == 0:
            messagebox.showinfo("Save Queue", "Queue is empty")
            return
        
        name = simpledialog.askstring("Save Queue", "Enter playlist name:")
        if name:
            queue_tracks = self.queue.to_list()
            self.playlist_manager.create_playlist(name, queue_tracks)
            self.playlist_view.refresh()
            messagebox.showinfo("Saved", f"Queue saved as playlist '{name}'")
    
    def _apply_theme(self):
        """Apply the selected theme"""
        theme = self.theme_var.get()
        self.current_theme = theme
        self.settings_manager.set("theme", theme)
        
        style = ttk.Style()
        apply_theme(theme, style, self.root)
    
    def _show_duplicates(self):
        """Show duplicate tracks in library"""
        self.library_view._show_duplicates()
        self.notebook.select(0)  # Switch to library tab
    
    def _show_missing(self):
        """Show missing files in library"""
        self.library_view._show_missing()
        self.notebook.select(0)  # Switch to library tab
    
    def _show_settings(self):
        """Show settings dialog"""
        def on_theme_change(theme):
            self.theme_var.set(theme)
            self._apply_theme()
        SettingsDialog(self.root, self.settings_manager, on_theme_change=on_theme_change)
    
    def _show_keyboard_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        KeyboardShortcutsDialog(self.root)
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About KVGroove", 
                           "KVGroove Music Player\n\n"
                           "A simple yet powerful music player\n"
                           "for Windows.\n\n"
                           "© 2025 KVGroove")
    
    def _create_control_bar(self, parent):
        """Create the playback control bar"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Left: Now playing info
        now_playing_frame = ttk.Frame(control_frame)
        now_playing_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.title_var = tk.StringVar(value="No track playing")
        self.artist_var = tk.StringVar(value="")
        
        title_label = ttk.Label(now_playing_frame, textvariable=self.title_var,
                                font=('Segoe UI', 11, 'bold'))
        title_label.pack(anchor=tk.W)
        
        artist_label = ttk.Label(now_playing_frame, textvariable=self.artist_var,
                                 font=('Segoe UI', 9))
        artist_label.pack(anchor=tk.W)
        
        # Center: Playback controls
        controls_center = ttk.Frame(control_frame)
        controls_center.pack(side=tk.LEFT, expand=True)
        
        # Control buttons
        btn_frame = ttk.Frame(controls_center)
        btn_frame.pack()
        
        # Shuffle button
        self.shuffle_var = tk.BooleanVar(value=self.queue.is_shuffle())
        self.shuffle_btn = ttk.Checkbutton(btn_frame, text="🔀", 
                                           variable=self.shuffle_var,
                                           command=self._toggle_shuffle,
                                           style='Toolbutton')
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)
        
        # Previous button
        prev_btn = ttk.Button(btn_frame, text="⏮", width=4,
                              command=self._previous_track, 
                              style='Control.TButton')
        prev_btn.pack(side=tk.LEFT, padx=2)
        
        # Play/Pause button
        self.play_btn_text = tk.StringVar(value="▶")
        play_btn = ttk.Button(btn_frame, textvariable=self.play_btn_text, 
                              width=4, command=self._toggle_play,
                              style='Control.TButton')
        play_btn.pack(side=tk.LEFT, padx=2)
        
        # Stop button
        stop_btn = ttk.Button(btn_frame, text="⏹", width=4,
                              command=self._stop, style='Control.TButton')
        stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Next button
        next_btn = ttk.Button(btn_frame, text="⏭", width=4,
                              command=self._next_track, 
                              style='Control.TButton')
        next_btn.pack(side=tk.LEFT, padx=2)
        
        # Repeat button
        self.repeat_var = tk.StringVar(value=self._get_repeat_symbol())
        repeat_btn = ttk.Button(btn_frame, textvariable=self.repeat_var,
                                width=4, command=self._toggle_repeat)
        repeat_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        progress_frame = ttk.Frame(controls_center)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.position_var = tk.StringVar(value="0:00")
        position_label = ttk.Label(progress_frame, textvariable=self.position_var,
                                   width=6)
        position_label.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_scale = ttk.Scale(progress_frame, from_=0, to=100,
                                        orient=tk.HORIZONTAL,
                                        variable=self.progress_var,
                                        command=self._on_seek)
        self.progress_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.duration_var = tk.StringVar(value="0:00")
        duration_label = ttk.Label(progress_frame, textvariable=self.duration_var,
                                   width=6)
        duration_label.pack(side=tk.LEFT)
        
        # Right: Volume control
        volume_frame = ttk.Frame(control_frame)
        volume_frame.pack(side=tk.RIGHT)
        
        ttk.Label(volume_frame, text="🔊").pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=self.player.get_volume() * 100)
        volume_scale = ttk.Scale(volume_frame, from_=0, to=100,
                                 orient=tk.HORIZONTAL, length=100,
                                 variable=self.volume_var,
                                 command=self._on_volume_change)
        volume_scale.pack(side=tk.LEFT, padx=5)
    
    def _create_content_area(self, parent):
        """Create the main content area with tabs"""
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Library tab
        self.library_view = LibraryView(
            self.notebook,
            self.library,
            on_track_double_click=self._play_track,
            on_add_to_queue=self._add_to_queue,
            on_add_to_playlist=self._add_to_playlist,
            get_playlists=lambda: self.playlist_view.get_playlist_names(),
            settings=self.settings_manager
        )
        self.notebook.add(self.library_view, text="  Library  ")
        
        # Playlists tab
        self.playlist_view = PlaylistView(
            self.notebook,
            self.playlist_manager,
            self.library,
            on_track_double_click=self._play_track,
            on_play_playlist=self._play_playlist
        )
        self.notebook.add(self.playlist_view, text="  Playlists  ")
        
        # Queue tab
        self.queue_view = QueueView(
            self.notebook,
            self.queue,
            self.library,
            on_track_double_click=self._play_queue_index
        )
        self.notebook.add(self.queue_view, text="  Queue  ")
    
    def _setup_bindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<space>', lambda e: self._toggle_play())
        self.root.bind('<Left>', lambda e: self._seek_relative(-5))
        self.root.bind('<Right>', lambda e: self._seek_relative(5))
        self.root.bind('<Control-Left>', lambda e: self._previous_track())
        self.root.bind('<Control-Right>', lambda e: self._next_track())
        self.root.bind('<Control-Up>', lambda e: self._change_volume(5))
        self.root.bind('<Control-Down>', lambda e: self._change_volume(-5))
        self.root.bind('<m>', lambda e: self._toggle_mute())
        self.root.bind('<M>', lambda e: self._toggle_mute())
        self.root.bind('<F1>', lambda e: self._show_keyboard_shortcuts())
        self.root.bind('<Control-q>', lambda e: self._clear_queue())
        self.root.bind('<Control-Q>', lambda e: self._clear_queue())
        self.root.bind('<Control-Shift-s>', lambda e: self._shuffle_remaining())
        self.root.bind('<Control-Shift-S>', lambda e: self._shuffle_remaining())
        self.root.bind('<Control-comma>', lambda e: self._show_settings())
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds as mm:ss"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def _get_repeat_symbol(self) -> str:
        """Get symbol for current repeat mode"""
        mode = self.queue.get_repeat()
        if mode == 'one':
            return "🔂"
        elif mode == 'all':
            return "🔁"
        return "↩"
    
    def _play_track(self, track: Track):
        """Play a specific track"""
        # Add to queue and play
        self.queue.add(track.path)
        self.queue.play_index(len(self.queue) - 1)
        self._load_and_play_current()
    
    def _add_to_queue(self, track: Track):
        """Add track to queue"""
        self.queue.add(track.path)
        self.queue_view.refresh()
    
    def _add_to_playlist(self, track: Track, playlist_name: str):
        """Add track to a playlist"""
        self.playlist_view.add_track_to_playlist(track, playlist_name)
    
    def _play_playlist(self, track_paths: list):
        """Play all tracks in a playlist"""
        self.queue.clear()
        self.queue.add_multiple(track_paths)
        self.queue.play_index(0)
        self._load_and_play_current()
    
    def _play_queue_index(self, index: int):
        """Play track at specific queue index"""
        self.queue.play_index(index)
        self._load_and_play_current()
    
    def _load_and_play_current(self):
        """Load and play the current track in queue"""
        track_path = self.queue.get_current()
        if not track_path:
            return
        
        self.current_track = self.library.get_track_by_path(track_path)
        
        if self.player.load(track_path):
            self.player.play()
            self.play_btn_text.set("⏸")
            
            # Add to recently played
            self.settings_manager.add_to_recently_played(track_path)
            
            # Update display
            if self.current_track:
                self.title_var.set(self.current_track.title)
                self.artist_var.set(self.current_track.artist)
                self.duration_var.set(self._format_time(self.current_track.duration))
            else:
                filename = track_path.split('\\')[-1].split('/')[-1]
                self.title_var.set(filename)
                self.artist_var.set("")
                self.duration_var.set(self._format_time(self.player.get_duration()))
            
            self.queue_view.refresh()
            self.queue_view.set_now_playing(self.current_track)
    
    def _toggle_play(self):
        """Toggle play/pause"""
        if self.player.is_playing:
            self.player.pause()
            self.play_btn_text.set("▶")
        elif self.player.is_paused:
            self.player.play()
            self.play_btn_text.set("⏸")
        elif self.queue.get_current():
            self._load_and_play_current()
    
    def _stop(self):
        """Stop playback"""
        self.player.stop()
        self.play_btn_text.set("▶")
        self.progress_var.set(0)
        self.position_var.set("0:00")
    
    def _previous_track(self):
        """Go to previous track"""
        # If more than 3 seconds in, restart current track
        if self.player.get_position() > 3:
            self.player.seek(0)
            return
        
        if self.queue.get_previous():
            self._load_and_play_current()
    
    def _next_track(self):
        """Go to next track"""
        if self.queue.get_next():
            self._load_and_play_current()
        else:
            self._stop()
    
    def _on_track_end(self):
        """Called when current track ends"""
        self.root.after(0, self._next_track)
    
    def _toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.queue.set_shuffle(self.shuffle_var.get())
        self.queue_view.refresh()
    
    def _toggle_repeat(self):
        """Cycle through repeat modes"""
        current = self.queue.get_repeat()
        if current == 'none':
            self.queue.set_repeat('all')
        elif current == 'all':
            self.queue.set_repeat('one')
        else:
            self.queue.set_repeat('none')
        
        self.repeat_var.set(self._get_repeat_symbol())
    
    def _on_seek(self, value):
        """Handle seek bar change"""
        if self.player.current_file:
            duration = self.player.get_duration()
            if duration > 0:
                position = (float(value) / 100) * duration
                self.player.seek(position)
    
    def _seek_relative(self, seconds: int):
        """Seek relative to current position"""
        if self.player.current_file:
            new_pos = max(0, self.player.get_position() + seconds)
            duration = self.player.get_duration()
            if duration > 0:
                self.progress_var.set((new_pos / duration) * 100)
                self.player.seek(new_pos)
    
    def _on_volume_change(self, value):
        """Handle volume change"""
        self.player.set_volume(float(value) / 100)
    
    def _change_volume(self, delta: int):
        """Change volume by delta percent"""
        new_vol = max(0, min(100, self.volume_var.get() + delta))
        self.volume_var.set(new_vol)
        self.player.set_volume(new_vol / 100)
    
    def _update_position(self):
        """Update position display periodically"""
        if self.player.is_playing:
            position = self.player.get_position()
            duration = self.player.get_duration()
            
            self.position_var.set(self._format_time(position))
            
            if duration > 0:
                progress = (position / duration) * 100
                self.progress_var.set(progress)
        
        # Schedule next update
        self.root.after(100, self._update_position)
    
    def _on_close(self):
        """Handle window close"""
        self._save_settings()
        self.player.cleanup()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
