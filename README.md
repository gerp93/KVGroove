# KVGroove

A feature-rich Windows desktop music player built with Python and tkinter. Organize your music with playlists, queue up tracks, and enjoy playback with powerful controls and beautiful themes.

## Features

- **Music Library** - Browse and search your music collection with metadata support
- **Playlists** - Create, edit, and manage playlists (save/load from JSON)
- **Play Queue** - Queue up tracks, shuffle remaining, clear upcoming, save queue as playlist
- **Playback Controls** - Play, pause, stop, next, previous, seek, volume control
- **Shuffle & Repeat** - Shuffle mode and repeat (none/one/all)
- **Themes** - 9 beautiful themes: Light, Dark, Neon, Retrowave, Hacker, Lava, Electric Lime, Bubblegum, Commander Keen
- **Track Editing** - Edit metadata (title, artist, album) and save to file
- **Sleep Timer** - Auto-stop playback after a set duration
- **Favorites & Recently Played** - Mark favorite tracks and track your listening history
- **Password Protection** - Optional password lock for library access
- **Duplicate & Missing Detection** - Find duplicate tracks and detect missing files
- **Backup & Restore** - Backup and restore your library and playlists

## Supported Formats

- MP3
- FLAC
- WAV
- OGG
- M4A
- WMA

## Installation

### Option 1: Download and Run (Recommended for Users)

**Latest Release:**
- Download the latest `.exe` or `.zip` from [GitHub Releases](https://github.com/gerp93/KVGroove/releases)
- Extract the `.zip` file (if downloaded as archive)
- Run `KVGroove.exe` (no installation required)

**System Requirements:**
- Windows 7 or later
- ~50 MB disk space for the executable

### Option 2: Clone and Run (For Developers)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gerp93/KVGroove.git
   cd KVGroove
   ```

2. **Create a Python virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python kvgroove.py
   ```

### Option 3: Install from Source (Advanced)

1. Clone the repo and install dependencies (see Option 2 steps 1-3)
2. Build a standalone executable using PyInstaller:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --icon=icon.ico kvgroove.py
   ```
3. The executable will be in the `dist/` folder

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Space` | Play/Pause |
| `←` / `→` | Seek backward/forward 5 seconds |
| `Ctrl+←` / `Ctrl+→` | Previous/Next track |
| `Ctrl+↑` / `Ctrl+↓` | Volume up/down |
| `Ctrl+M` | Toggle Mute |
| `Ctrl+H` | Show keyboard shortcuts help |

**View all shortcuts in-app:** File → Help → Keyboard Shortcuts

## Getting Started

1. **Launch KVGroove**
   - If running from executable: Double-click `KVGroove.exe`
   - If running from source: `python kvgroove.py`

2. **Add Music to Your Library**
   - Click **"+ Add Folder"** in the Library tab
   - Select a folder containing music files
   - KVGroove will scan and index all supported audio files

3. **Play Music**
   - Double-click any track in the library to start playback
   - Use the playback controls (play, pause, next, previous)
   - Adjust volume with the volume slider or `Ctrl+↑`/`Ctrl+↓`

4. **Queue & Playlists**
   - Right-click tracks to add them to the queue
   - Create playlists in the Playlist tab
   - Save the current queue as a new playlist

5. **Customize Your Experience**
   - **Change Theme:** View menu → Select a theme
   - **Set Sleep Timer:** Playback menu → Sleep Timer
   - **Edit Track Info:** Right-click a track → Edit Metadata
   - **Adjust Settings:** File → Settings

## Project Structure

```
KVGroove/
├── kvgroove.py              # Main entry point
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── THEMES_MODULE_PLAN.md    # Plan for standalone themes module
├── .github/
│   └── copilot-instructions.md  # AI assistant context
├── ui/                      # UI components
│   ├── __init__.py
│   ├── main_window.py       # Main window and menu bar
│   ├── library_view.py      # Library browser panel
│   ├── playlist_view.py     # Playlist manager panel
│   ├── queue_view.py        # Queue panel
│   ├── themes.py            # Theme definitions (9 themes)
│   ├── dialogs.py           # Settings, sleep timer, shortcuts dialogs
│   ├── login_dialog.py      # Password protection dialog
│   └── track_editor.py      # Track metadata editor
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── player.py            # Audio playback engine (pygame)
│   ├── library.py           # Library management & metadata (mutagen)
│   ├── playlist.py          # Playlist management
│   ├── queue.py             # Play queue management
│   ├── settings.py          # Settings persistence
│   └── auth.py              # Password authentication
└── data/                    # User data (auto-created)
    ├── library.json         # Scanned music library index
    ├── playlists.json       # Saved playlists
    └── settings.json        # App preferences & theme
```

## Technology Stack

- **Language:** Python 3.8+
- **UI Framework:** tkinter (bundled with Python)
- **Audio Playback:** pygame 2.6.1
- **Audio Metadata:** mutagen 1.47.0
- **Data Storage:** JSON files (no database required)

## Troubleshooting

### No sound when playing music
- Make sure your audio drivers are installed and working
- Try adjusting the volume in KVGroove or your system mixer
- Check that the audio device is not muted

### Library not scanning files
- Ensure you have read permissions on the music folder
- Supported formats: MP3, FLAC, WAV, OGG, M4A, WMA
- Large folders may take a few moments to scan; check the status bar

### Password forgotten
- Delete `data/settings.json` to reset all settings (including password)
- Note: This will also reset your library and playlists

## Future Roadmap

- Cross-platform support (macOS, Linux)
- Standalone `tkthemes` module for other tkinter apps
- Apple Music integration
- Visualization/equalizer
- Theme customization UI

See [THEMES_MODULE_PLAN.md](THEMES_MODULE_PLAN.md) for upcoming theme module extraction.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request


## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the [LICENSE](LICENSE) file for details.

## Support

- **Issues:** Report bugs or request features on [GitHub Issues](https://github.com/gerp93/KVGroove/issues)
- **Discussions:** Join the conversation on [GitHub Discussions](https://github.com/gerp93/KVGroove/discussions)

## Acknowledgments

- Built with Python, tkinter, pygame, and mutagen
- Inspired by classic music players and modern UI design
- Special themes: Neon, Retrowave, Hacker, Lava, Electric Lime, Bubblegum, Commander Keen
