# KVGroove

A simple Windows desktop music player built with Python.

## Features

- **Music Library** - Browse and search your music collection
- **Playlists** - Create, edit, and manage playlists
- **Play Queue** - Queue up tracks to play next
- **Playback Controls** - Play, pause, stop, next, previous, seek
- **Shuffle & Repeat** - Shuffle mode and repeat (none/one/all)
- **Volume Control** - Adjustable volume with keyboard shortcuts

## Supported Formats

- MP3
- FLAC
- WAV
- OGG
- M4A
- WMA

## Installation

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python kvgroove.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Space` | Play/Pause |
| `←` / `→` | Seek backward/forward 5 seconds |
| `Ctrl+←` / `Ctrl+→` | Previous/Next track |
| `Ctrl+↑` / `Ctrl+↓` | Volume up/down |

## Getting Started

1. Launch KVGroove
2. Click **"+ Add Folder"** in the Library tab to add your music folders
3. Double-click any track to play it
4. Right-click tracks to add them to queue or playlists

## Project Structure

```
KVGroove/
├── kvgroove.py          # Main entry point
├── ui/                  # UI components
│   ├── main_window.py   # Main window layout
│   ├── library_view.py  # Library browser
│   ├── playlist_view.py # Playlist manager
│   └── queue_view.py    # Queue panel
├── core/                # Core functionality
│   ├── player.py        # Audio playback engine
│   ├── library.py       # Library management
│   ├── playlist.py      # Playlist management
│   └── queue.py         # Queue management
├── data/                # User data (auto-created)
│   ├── library.json     # Library index
│   ├── playlists.json   # Saved playlists
│   └── settings.json    # App settings
└── requirements.txt     # Python dependencies
```

## License

MIT License
