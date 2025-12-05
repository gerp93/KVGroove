"""
KVGroove Settings Dialog
Preferences and settings UI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional

from core.settings import SettingsManager
from ui.themes import get_theme_list


class SettingsDialog:
    """Settings/Preferences dialog"""
    
    def __init__(self, parent: tk.Tk, settings: SettingsManager,
                 on_theme_change: Optional[Callable[[str], None]] = None):
        self.settings = settings
        self.parent = parent
        self.on_theme_change = on_theme_change
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x450")
        self.dialog.resizable(False, False)
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 450) // 2
        self.dialog.geometry(f"500x450+{x}+{y}")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Playback tab
        self._create_playback_tab(notebook)
        
        # Appearance tab
        self._create_appearance_tab(notebook)
        
        # Library tab
        self._create_library_tab(notebook)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(btn_frame, text="Save", width=12, font=('Segoe UI', 9),
                  command=self._on_save).pack(side=tk.RIGHT, padx=(5, 0), ipady=3)
        tk.Button(btn_frame, text="Cancel", width=12, font=('Segoe UI', 9),
                  command=self.dialog.destroy).pack(side=tk.RIGHT, ipady=3)
    
    def _create_playback_tab(self, notebook):
        """Create playback settings tab"""
        frame = ttk.Frame(notebook, padding=15)
        notebook.add(frame, text="  Playback  ")
        
        # Crossfade
        cf_frame = ttk.LabelFrame(frame, text="Crossfade", padding=10)
        cf_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.crossfade_var = tk.DoubleVar(value=self.settings.get('crossfade_seconds', 0))
        ttk.Label(cf_frame, text="Crossfade duration (seconds):").pack(anchor=tk.W)
        cf_scale = ttk.Scale(cf_frame, from_=0, to=10, variable=self.crossfade_var,
                            orient=tk.HORIZONTAL)
        cf_scale.pack(fill=tk.X, pady=(5, 0))
        self.cf_label = ttk.Label(cf_frame, text=f"{self.crossfade_var.get():.1f}s")
        self.cf_label.pack(anchor=tk.E)
        self.crossfade_var.trace('w', lambda *args: self.cf_label.config(
            text=f"{self.crossfade_var.get():.1f}s"))
        
        # Playback speed
        speed_frame = ttk.LabelFrame(frame, text="Playback Speed", padding=10)
        speed_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.speed_var = tk.DoubleVar(value=self.settings.get('playback_speed', 1.0))
        ttk.Label(speed_frame, text="Speed:").pack(anchor=tk.W)
        
        speed_options = ttk.Frame(speed_frame)
        speed_options.pack(fill=tk.X, pady=(5, 0))
        
        for speed in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            ttk.Radiobutton(speed_options, text=f"{speed}x", value=speed,
                           variable=self.speed_var).pack(side=tk.LEFT, padx=5)
        
        # Sleep timer presets
        sleep_frame = ttk.LabelFrame(frame, text="Sleep Timer Presets", padding=10)
        sleep_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(sleep_frame, text="Quick presets: 15, 30, 45, 60 minutes").pack(anchor=tk.W)
        ttk.Label(sleep_frame, text="(Access from File menu)", 
                 font=('Segoe UI', 8)).pack(anchor=tk.W)
    
    def _create_appearance_tab(self, notebook):
        """Create appearance settings tab"""
        frame = ttk.Frame(notebook, padding=15)
        notebook.add(frame, text="  Appearance  ")
        
        # Theme
        theme_frame = ttk.LabelFrame(frame, text="Theme", padding=10)
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.settings.get('theme', 'light'))
        
        # Dynamically create radio buttons from tkthemes
        for theme_id, theme_name in get_theme_list():
            ttk.Radiobutton(theme_frame, text=theme_name, value=theme_id,
                           variable=self.theme_var).pack(anchor=tk.W)
        
        # Visualizations
        vis_frame = ttk.LabelFrame(frame, text="Visualizations", padding=10)
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.waveform_var = tk.BooleanVar(value=self.settings.get('show_waveform', False))
        ttk.Checkbutton(vis_frame, text="Show waveform display",
                       variable=self.waveform_var).pack(anchor=tk.W)
        
        self.spectrum_var = tk.BooleanVar(value=self.settings.get('show_spectrum', False))
        ttk.Checkbutton(vis_frame, text="Show spectrum analyzer",
                       variable=self.spectrum_var).pack(anchor=tk.W)
        
        ttk.Label(vis_frame, text="Note: Visualizations may affect performance",
                 font=('Segoe UI', 8), foreground='gray').pack(anchor=tk.W, pady=(5, 0))
    
    def _create_library_tab(self, notebook):
        """Create library settings tab"""
        frame = ttk.Frame(notebook, padding=15)
        notebook.add(frame, text="  Library  ")
        
        # Auto-rescan
        scan_frame = ttk.LabelFrame(frame, text="Auto-Rescan", padding=10)
        scan_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.auto_rescan_var = tk.BooleanVar(value=self.settings.get('auto_rescan', False))
        ttk.Checkbutton(scan_frame, text="Automatically rescan library folders",
                       variable=self.auto_rescan_var).pack(anchor=tk.W)
        
        interval_frame = ttk.Frame(scan_frame)
        interval_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(interval_frame, text="Rescan interval (minutes):").pack(side=tk.LEFT)
        self.rescan_interval_var = tk.IntVar(value=self.settings.get('auto_rescan_interval', 60))
        ttk.Spinbox(interval_frame, from_=5, to=360, width=8,
                   textvariable=self.rescan_interval_var).pack(side=tk.LEFT, padx=(5, 0))
        
        # Recently played
        recent_frame = ttk.LabelFrame(frame, text="Recently Played", padding=10)
        recent_frame.pack(fill=tk.X, pady=(0, 10))
        
        max_frame = ttk.Frame(recent_frame)
        max_frame.pack(fill=tk.X)
        ttk.Label(max_frame, text="Maximum tracks to remember:").pack(side=tk.LEFT)
        self.recent_max_var = tk.IntVar(value=self.settings.get('recently_played_max', 50))
        ttk.Spinbox(max_frame, from_=10, to=500, width=8,
                   textvariable=self.recent_max_var).pack(side=tk.LEFT, padx=(5, 0))
    
    def _on_save(self):
        """Save settings"""
        # Playback
        self.settings.set('crossfade_seconds', self.crossfade_var.get())
        self.settings.set('playback_speed', self.speed_var.get())
        
        # Appearance
        old_theme = self.settings.get('theme')
        new_theme = self.theme_var.get()
        self.settings.set('theme', new_theme)
        self.settings.set('show_waveform', self.waveform_var.get())
        self.settings.set('show_spectrum', self.spectrum_var.get())
        
        # Library
        self.settings.set('auto_rescan', self.auto_rescan_var.get())
        self.settings.set('auto_rescan_interval', self.rescan_interval_var.get())
        self.settings.set('recently_played_max', self.recent_max_var.get())
        
        self.settings.save()
        
        # Notify theme change
        if old_theme != new_theme and self.on_theme_change:
            self.on_theme_change(new_theme)
        
        messagebox.showinfo("Settings Saved", "Settings have been saved.",
                           parent=self.dialog)
        self.dialog.destroy()


class SleepTimerDialog:
    """Sleep timer dialog"""
    
    def __init__(self, parent: tk.Tk, on_set: Callable[[float], None],
                 current_remaining: float = 0):
        self.parent = parent
        self.on_set = on_set
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Sleep Timer")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 300) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
        self.dialog.geometry(f"300x200+{x}+{y}")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets(current_remaining)
    
    def _create_widgets(self, current_remaining: float):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Sleep Timer", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))
        
        # Current status
        if current_remaining > 0:
            mins = int(current_remaining // 60)
            secs = int(current_remaining % 60)
            status_text = f"Timer active: {mins}:{secs:02d} remaining"
        else:
            status_text = "No timer set"
        
        ttk.Label(main_frame, text=status_text).pack(pady=(0, 10))
        
        # Quick presets
        preset_frame = ttk.Frame(main_frame)
        preset_frame.pack(pady=(0, 10))
        
        for mins in [15, 30, 45, 60]:
            tk.Button(preset_frame, text=f"{mins} min", width=8,
                     command=lambda m=mins: self._set_timer(m)).pack(side=tk.LEFT, padx=2)
        
        # Custom time
        custom_frame = ttk.Frame(main_frame)
        custom_frame.pack(pady=(10, 0))
        
        ttk.Label(custom_frame, text="Custom (minutes):").pack(side=tk.LEFT)
        self.custom_var = tk.IntVar(value=30)
        ttk.Spinbox(custom_frame, from_=1, to=480, width=6,
                   textvariable=self.custom_var).pack(side=tk.LEFT, padx=5)
        tk.Button(custom_frame, text="Set", width=6,
                 command=lambda: self._set_timer(self.custom_var.get())).pack(side=tk.LEFT)
        
        # Cancel button
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(btn_frame, text="Cancel Timer", width=12,
                 command=lambda: self._set_timer(0)).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Close", width=10,
                 command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def _set_timer(self, minutes: float):
        """Set the timer"""
        self.on_set(minutes)
        self.dialog.destroy()


class KeyboardShortcutsDialog:
    """Dialog showing keyboard shortcuts"""
    
    def __init__(self, parent: tk.Tk):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Keyboard Shortcuts")
        self.dialog.geometry("400x450")
        self.dialog.resizable(False, False)
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 450) // 2
        self.dialog.geometry(f"400x450+{x}+{y}")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Keyboard Shortcuts",
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))
        
        shortcuts = [
            ("Playback", [
                ("Space", "Play / Pause"),
                ("Ctrl+Right", "Next track"),
                ("Ctrl+Left", "Previous track"),
                ("Left / Right", "Seek 5 seconds"),
                ("Ctrl+Up", "Volume up"),
                ("Ctrl+Down", "Volume down"),
                ("M", "Mute / Unmute"),
            ]),
            ("Queue", [
                ("Ctrl+Q", "Clear queue"),
                ("Ctrl+Shift+S", "Shuffle queue"),
            ]),
            ("General", [
                ("Ctrl+F", "Search library"),
                ("Ctrl+N", "New playlist"),
                ("F1", "Show shortcuts"),
                ("Ctrl+,", "Settings"),
            ]),
        ]
        
        for category, items in shortcuts:
            cat_frame = ttk.LabelFrame(main_frame, text=category, padding=10)
            cat_frame.pack(fill=tk.X, pady=(0, 10))
            
            for key, action in items:
                row = ttk.Frame(cat_frame)
                row.pack(fill=tk.X, pady=1)
                ttk.Label(row, text=key, width=15, font=('Consolas', 9)).pack(side=tk.LEFT)
                ttk.Label(row, text=action).pack(side=tk.LEFT)
        
        tk.Button(main_frame, text="Close", width=10,
                 command=self.dialog.destroy).pack(pady=(10, 0))


class BackupRestoreDialog:
    """Backup and restore dialog"""
    
    def __init__(self, parent: tk.Tk, settings: SettingsManager, 
                 playlist_manager, library):
        self.parent = parent
        self.settings = settings
        self.playlist_manager = playlist_manager
        self.library = library
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Backup & Restore")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 300) // 2
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Backup & Restore",
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))
        
        # Backup section
        backup_frame = ttk.LabelFrame(main_frame, text="Backup", padding=10)
        backup_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(backup_frame, 
                 text="Export settings, playlists, and library data").pack(anchor=tk.W)
        
        tk.Button(backup_frame, text="Export Backup...", width=20,
                 command=self._export_backup).pack(pady=(10, 0))
        
        # Restore section
        restore_frame = ttk.LabelFrame(main_frame, text="Restore", padding=10)
        restore_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(restore_frame,
                 text="Import settings and playlists from backup").pack(anchor=tk.W)
        
        tk.Button(restore_frame, text="Import Backup...", width=20,
                 command=self._import_backup).pack(pady=(10, 0))
        
        # Close button
        tk.Button(main_frame, text="Close", width=10,
                 command=self.dialog.destroy).pack(pady=(10, 0))
    
    def _export_backup(self):
        """Export backup"""
        folder = filedialog.askdirectory(title="Select Backup Location",
                                         parent=self.dialog)
        if folder:
            try:
                from pathlib import Path
                import json
                
                backup_dir = Path(folder) / "KVGroove_Backup"
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                # Export settings
                self.settings.export_settings(str(backup_dir / "settings.json"))
                
                # Export playlists
                self.playlist_manager.export_all_playlists(str(backup_dir))
                
                messagebox.showinfo("Backup Complete",
                                   f"Backup saved to:\n{backup_dir}",
                                   parent=self.dialog)
            except Exception as e:
                messagebox.showerror("Backup Failed",
                                    f"Error creating backup:\n{e}",
                                    parent=self.dialog)
    
    def _import_backup(self):
        """Import backup"""
        folder = filedialog.askdirectory(title="Select Backup Folder",
                                         parent=self.dialog)
        if folder:
            try:
                from pathlib import Path
                
                backup_dir = Path(folder)
                
                settings_file = backup_dir / "settings.json"
                if settings_file.exists():
                    self.settings.import_settings(str(settings_file))
                
                playlists_file = backup_dir / "playlists_backup.json"
                if playlists_file.exists():
                    self.playlist_manager.import_all_playlists(str(playlists_file))
                
                messagebox.showinfo("Restore Complete",
                                   "Backup has been restored.\nRestart the app to apply all changes.",
                                   parent=self.dialog)
            except Exception as e:
                messagebox.showerror("Restore Failed",
                                    f"Error restoring backup:\n{e}",
                                    parent=self.dialog)
