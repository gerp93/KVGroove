# KVGroove - Music Player

## Project Overview
KVGroove is a Windows desktop music player built with Python, featuring:
- Music library browser
- Playlist management
- Play queue system
- Audio playback controls

## Tech Stack
- **Language**: Python 3.x
- **UI**: tkinter
- **Audio**: pygame
- **Metadata**: mutagen
- **Storage**: JSON files

## Project Structure
```
KVGroove/
├── kvgroove.py          # Main application entry point
├── ui/                  # UI components
│   ├── __init__.py
│   ├── main_window.py   # Main window layout
│   ├── library_view.py  # Library browser panel
│   ├── playlist_view.py # Playlist panel
│   └── queue_view.py    # Queue panel
├── core/                # Core functionality
│   ├── __init__.py
│   ├── player.py        # Audio playback engine
│   ├── library.py       # Library management
│   ├── playlist.py      # Playlist management
│   └── queue.py         # Queue management
├── data/                # User data storage
│   ├── library.json     # Library index
│   ├── playlists.json   # Saved playlists
│   └── settings.json    # App settings
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## Running the App
```bash
pip install -r requirements.txt
python kvgroove.py
```
