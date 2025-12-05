"""
KVGroove Themes
Theme definitions for the music player
"""

from tkinter import ttk
from typing import Dict, Any, List, Tuple

# Theme registry with display names and icons
THEMES: Dict[str, Dict[str, str]] = {
    "light": {"name": "Light Theme", "icon": ""},
    "dark": {"name": "Dark Theme", "icon": ""},
    "neon": {"name": "🌈 NEON Theme", "icon": "🌈"},
    "retrowave": {"name": "🌅 Retrowave", "icon": "🌅"},
    "hacker": {"name": "💻 Hacker", "icon": "💻"},
    "lava": {"name": "🌋 LAVA", "icon": "🌋"},
    "electric_lime": {"name": "⚡ Electric Lime", "icon": "⚡"},
    "bubblegum": {"name": "🍬 Bubblegum", "icon": "🍬"},
    "commander_keen": {"name": "🚀 Commander Keen", "icon": "🚀"},
}


def get_theme_list() -> List[Tuple[str, str]]:
    """Get list of (theme_id, display_name) tuples"""
    return [(tid, info["name"]) for tid, info in THEMES.items()]


def apply_theme(theme: str, style: ttk.Style, root) -> str:
    """
    Apply the specified theme to the application.
    Returns the background color for the root window.
    """
    
    if theme == "dark":
        return _apply_dark_theme(style, root)
    elif theme == "neon":
        return _apply_neon_theme(style, root)
    elif theme == "retrowave":
        return _apply_retrowave_theme(style, root)
    elif theme == "hacker":
        return _apply_hacker_theme(style, root)
    elif theme == "lava":
        return _apply_lava_theme(style, root)
    elif theme == "electric_lime":
        return _apply_electric_lime_theme(style, root)
    elif theme == "bubblegum":
        return _apply_bubblegum_theme(style, root)
    elif theme == "commander_keen":
        return _apply_commander_keen_theme(style, root)
    else:
        return _apply_light_theme(style, root)


def _apply_light_theme(style: ttk.Style, root) -> str:
    """Light theme - default clean look"""
    bg_color = "#f5f5f5"
    fg_color = "#000000"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=fg_color)
    style.configure('TButton', background='#e0e0e0', foreground=fg_color)
    style.map('TButton',
             background=[('active', '#d0d0d0'), ('pressed', '#c0c0c0')],
             foreground=[('active', fg_color)])
    style.configure('TMenubutton', background='#e0e0e0', foreground=fg_color)
    style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
    style.configure('TRadiobutton', background=bg_color, foreground=fg_color)
    style.configure('TEntry', fieldbackground='white', foreground=fg_color)
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background='#e0e0e0', foreground=fg_color)
    style.configure('Treeview', background='white', foreground=fg_color,
                  fieldbackground='white')
    style.map('Treeview', background=[('selected', '#0078d4')])
    style.configure('Treeview.Heading', background='#e0e0e0', foreground=fg_color)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_dark_theme(style: ttk.Style, root) -> str:
    """Dark theme - easy on the eyes"""
    bg_color = "#2b2b2b"
    fg_color = "#ffffff"
    btn_bg = "#505050"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=fg_color)
    style.configure('TButton', background=btn_bg, foreground=fg_color)
    style.map('TButton', 
             background=[('active', '#606060'), ('pressed', '#707070')],
             foreground=[('active', fg_color)])
    style.configure('TMenubutton', background=btn_bg, foreground=fg_color)
    style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
    style.configure('TRadiobutton', background=bg_color, foreground=fg_color)
    style.configure('TEntry', fieldbackground='#404040', foreground=fg_color)
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background='#404040', foreground=fg_color)
    style.map('TNotebook.Tab', background=[('selected', '#505050')])
    style.configure('Treeview', background='#353535', foreground=fg_color, 
                  fieldbackground='#353535')
    style.map('Treeview', background=[('selected', '#505050')])
    style.configure('Treeview.Heading', background='#404040', foreground=fg_color)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_neon_theme(style: ttk.Style, root) -> str:
    """NEON theme - visually wild but readable"""
    bg_color = "#0a0a0a"
    
    neon_pink = "#ff00ff"
    neon_cyan = "#00ffff"
    neon_green = "#39ff14"
    neon_yellow = "#ffff00"
    neon_orange = "#ff6600"
    hot_pink = "#ff1493"
    electric_blue = "#7df9ff"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=neon_cyan,
                  font=('Consolas', 10, 'bold'))
    style.configure('Header.TLabel', background=bg_color, foreground=neon_pink,
                  font=('Consolas', 12, 'bold'))
    
    style.configure('TButton', background='#330033', foreground=neon_green,
                  font=('Consolas', 9, 'bold'))
    style.map('TButton', 
             background=[('active', '#660066'), ('pressed', '#990099')],
             foreground=[('active', neon_yellow)])
    
    style.configure('Control.TButton', background='#003333', foreground=neon_cyan,
                  font=('Consolas', 14, 'bold'), padding=10)
    style.map('Control.TButton',
             background=[('active', '#006666'), ('pressed', '#009999')],
             foreground=[('active', neon_yellow)])
    
    style.configure('TMenubutton', background='#330033', foreground=neon_pink)
    style.configure('TCheckbutton', background=bg_color, foreground=neon_orange)
    style.configure('TRadiobutton', background=bg_color, foreground=hot_pink)
    style.configure('TEntry', fieldbackground='#1a1a2e', foreground=neon_green,
                  insertcolor=neon_green)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background='#1a0033', foreground=neon_pink,
                  font=('Consolas', 10, 'bold'), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', '#330066')],
             foreground=[('selected', neon_cyan)])
    
    style.configure('Treeview', background='#0d0d1a', foreground=electric_blue,
                  fieldbackground='#0d0d1a', font=('Consolas', 9),
                  rowheight=25)
    style.map('Treeview', 
             background=[('selected', '#660066')],
             foreground=[('selected', neon_yellow)])
    style.configure('Treeview.Heading', background='#1a0033', foreground=neon_pink,
                  font=('Consolas', 10, 'bold'))
    
    style.configure('TScale', background=bg_color, troughcolor='#330033')
    style.configure('TScrollbar', background='#330033', troughcolor=bg_color,
                  arrowcolor=neon_pink)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_retrowave_theme(style: ttk.Style, root) -> str:
    """RETROWAVE - 80s synthwave sunset vibes"""
    bg_color = "#1a0a2e"
    
    sunset_pink = "#ff6b9d"
    sunset_orange = "#ff9a56"
    sunset_yellow = "#ffd93d"
    synth_purple = "#c77dff"
    hot_magenta = "#e040fb"
    chrome = "#e0e0e0"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=sunset_pink,
                  font=('Arial Black', 10))
    style.configure('Header.TLabel', background=bg_color, foreground=sunset_orange,
                  font=('Arial Black', 12))
    
    style.configure('TButton', background='#2d1b4e', foreground=sunset_yellow,
                  font=('Arial', 9, 'bold'))
    style.map('TButton', 
             background=[('active', '#4a2c7a'), ('pressed', '#6b3fa0')],
             foreground=[('active', chrome)])
    
    style.configure('Control.TButton', background='#3d1f5c', foreground=sunset_orange,
                  font=('Arial Black', 14), padding=10)
    style.map('Control.TButton',
             background=[('active', '#5c2d8a'), ('pressed', '#7a3db8')],
             foreground=[('active', sunset_yellow)])
    
    style.configure('TMenubutton', background='#2d1b4e', foreground=hot_magenta)
    style.configure('TCheckbutton', background=bg_color, foreground=synth_purple)
    style.configure('TRadiobutton', background=bg_color, foreground=sunset_pink)
    style.configure('TEntry', fieldbackground='#2d1b4e', foreground=chrome,
                  insertcolor=sunset_pink)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background='#3d1f5c', foreground=sunset_pink,
                  font=('Arial', 10, 'bold'), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', '#5c2d8a')],
             foreground=[('selected', sunset_yellow)])
    
    style.configure('Treeview', background='#1f0f3d', foreground=chrome,
                  fieldbackground='#1f0f3d', font=('Arial', 9),
                  rowheight=25)
    style.map('Treeview', 
             background=[('selected', '#5c2d8a')],
             foreground=[('selected', sunset_yellow)])
    style.configure('Treeview.Heading', background='#3d1f5c', foreground=sunset_orange,
                  font=('Arial Black', 10))
    
    style.configure('TScale', background=bg_color, troughcolor='#3d1f5c')
    style.configure('TScrollbar', background='#3d1f5c', troughcolor=bg_color,
                  arrowcolor=sunset_pink)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_hacker_theme(style: ttk.Style, root) -> str:
    """HACKER - Matrix-style green on black"""
    bg_color = "#0d0d0d"
    
    matrix_green = "#00ff00"
    lime = "#32cd32"
    phosphor = "#00ff41"
    amber = "#ffbf00"
    terminal_green = "#20c20e"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=matrix_green,
                  font=('Courier New', 10, 'bold'))
    style.configure('Header.TLabel', background=bg_color, foreground=phosphor,
                  font=('Courier New', 12, 'bold'))
    
    style.configure('TButton', background='#001a00', foreground=matrix_green,
                  font=('Courier New', 9, 'bold'))
    style.map('TButton', 
             background=[('active', '#003300'), ('pressed', '#004d00')],
             foreground=[('active', amber)])
    
    style.configure('Control.TButton', background='#001a00', foreground=phosphor,
                  font=('Courier New', 14, 'bold'), padding=10)
    style.map('Control.TButton',
             background=[('active', '#003300'), ('pressed', '#004d00')],
             foreground=[('active', amber)])
    
    style.configure('TMenubutton', background='#001a00', foreground=lime)
    style.configure('TCheckbutton', background=bg_color, foreground=terminal_green)
    style.configure('TRadiobutton', background=bg_color, foreground=matrix_green)
    style.configure('TEntry', fieldbackground='#001100', foreground=matrix_green,
                  insertcolor=matrix_green)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background='#001a00', foreground=matrix_green,
                  font=('Courier New', 10, 'bold'), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', '#003300')],
             foreground=[('selected', amber)])
    
    style.configure('Treeview', background='#0a0a0a', foreground=terminal_green,
                  fieldbackground='#0a0a0a', font=('Courier New', 9),
                  rowheight=22)
    style.map('Treeview', 
             background=[('selected', '#003300')],
             foreground=[('selected', amber)])
    style.configure('Treeview.Heading', background='#001a00', foreground=phosphor,
                  font=('Courier New', 10, 'bold'))
    
    style.configure('TScale', background=bg_color, troughcolor='#001a00')
    style.configure('TScrollbar', background='#001a00', troughcolor=bg_color,
                  arrowcolor=matrix_green)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_lava_theme(style: ttk.Style, root) -> str:
    """LAVA - Fiery red hot theme"""
    bg_color = "#cc0000"
    
    molten_orange = "#ff6600"
    fire_yellow = "#ffcc00"
    white_hot = "#ffffff"
    dark_ember = "#330000"
    charcoal = "#1a0000"
    bright_flame = "#ff3300"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=white_hot,
                  font=('Impact', 10))
    style.configure('Header.TLabel', background=bg_color, foreground=fire_yellow,
                  font=('Impact', 12))
    
    style.configure('TButton', background=dark_ember, foreground=fire_yellow,
                  font=('Arial Black', 9))
    style.map('TButton', 
             background=[('active', '#4d0000'), ('pressed', '#660000')],
             foreground=[('active', white_hot)])
    
    style.configure('Control.TButton', background=charcoal, foreground=molten_orange,
                  font=('Impact', 14), padding=10)
    style.map('Control.TButton',
             background=[('active', dark_ember), ('pressed', '#4d0000')],
             foreground=[('active', fire_yellow)])
    
    style.configure('TMenubutton', background=dark_ember, foreground=bright_flame)
    style.configure('TCheckbutton', background=bg_color, foreground=white_hot)
    style.configure('TRadiobutton', background=bg_color, foreground=fire_yellow)
    style.configure('TEntry', fieldbackground=charcoal, foreground=fire_yellow,
                  insertcolor=fire_yellow)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background=dark_ember, foreground=molten_orange,
                  font=('Impact', 10), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', '#660000')],
             foreground=[('selected', fire_yellow)])
    
    style.configure('Treeview', background=charcoal, foreground=fire_yellow,
                  fieldbackground=charcoal, font=('Arial', 9),
                  rowheight=24)
    style.map('Treeview', 
             background=[('selected', '#800000')],
             foreground=[('selected', white_hot)])
    style.configure('Treeview.Heading', background=dark_ember, foreground=molten_orange,
                  font=('Impact', 10))
    
    style.configure('TScale', background=bg_color, troughcolor=dark_ember)
    style.configure('TScrollbar', background=dark_ember, troughcolor=bg_color,
                  arrowcolor=fire_yellow)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_electric_lime_theme(style: ttk.Style, root) -> str:
    """ELECTRIC LIME - Blindingly bright green-yellow"""
    bg_color = "#ccff00"
    
    hot_black = "#0a0a0a"
    deep_purple = "#4a0080"
    electric_blue = "#0066ff"
    magenta_pop = "#ff00aa"
    dark_lime = "#88aa00"
    ultra_violet = "#7700ff"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=hot_black,
                  font=('Trebuchet MS', 10, 'bold'))
    style.configure('Header.TLabel', background=bg_color, foreground=deep_purple,
                  font=('Trebuchet MS', 12, 'bold'))
    
    style.configure('TButton', background=deep_purple, foreground=bg_color,
                  font=('Trebuchet MS', 9, 'bold'))
    style.map('TButton', 
             background=[('active', ultra_violet), ('pressed', '#5c00a3')],
             foreground=[('active', '#ffffff')])
    
    style.configure('Control.TButton', background=electric_blue, foreground='#ffffff',
                  font=('Trebuchet MS', 14, 'bold'), padding=10)
    style.map('Control.TButton',
             background=[('active', '#0080ff'), ('pressed', '#0099ff')],
             foreground=[('active', bg_color)])
    
    style.configure('TMenubutton', background=deep_purple, foreground=bg_color)
    style.configure('TCheckbutton', background=bg_color, foreground=magenta_pop)
    style.configure('TRadiobutton', background=bg_color, foreground=deep_purple)
    style.configure('TEntry', fieldbackground='#ffffff', foreground=hot_black,
                  insertcolor=deep_purple)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background=dark_lime, foreground=hot_black,
                  font=('Trebuchet MS', 10, 'bold'), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', deep_purple)],
             foreground=[('selected', '#ffffff')])
    
    style.configure('Treeview', background='#eeffaa', foreground=hot_black,
                  fieldbackground='#eeffaa', font=('Trebuchet MS', 9),
                  rowheight=24)
    style.map('Treeview', 
             background=[('selected', deep_purple)],
             foreground=[('selected', '#ffffff')])
    style.configure('Treeview.Heading', background=dark_lime, foreground=hot_black,
                  font=('Trebuchet MS', 10, 'bold'))
    
    style.configure('TScale', background=bg_color, troughcolor=dark_lime)
    style.configure('TScrollbar', background=dark_lime, troughcolor=bg_color,
                  arrowcolor=hot_black)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_bubblegum_theme(style: ttk.Style, root) -> str:
    """BUBBLEGUM - Hot pink explosion"""
    bg_color = "#ff69b4"
    
    white = "#ffffff"
    deep_magenta = "#cc0066"
    baby_blue = "#87ceeb"
    candy_purple = "#9932cc"
    sunshine = "#ffff00"
    cotton_candy = "#ffb6c1"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=white,
                  font=('Comic Sans MS', 10, 'bold'))
    style.configure('Header.TLabel', background=bg_color, foreground=sunshine,
                  font=('Comic Sans MS', 12, 'bold'))
    
    style.configure('TButton', background=candy_purple, foreground=white,
                  font=('Comic Sans MS', 9, 'bold'))
    style.map('TButton', 
             background=[('active', '#aa28aa'), ('pressed', '#bb33bb')],
             foreground=[('active', sunshine)])
    
    style.configure('Control.TButton', background=baby_blue, foreground=deep_magenta,
                  font=('Comic Sans MS', 14, 'bold'), padding=10)
    style.map('Control.TButton',
             background=[('active', '#a0d8ef'), ('pressed', '#b8e2f2')],
             foreground=[('active', candy_purple)])
    
    style.configure('TMenubutton', background=candy_purple, foreground=white)
    style.configure('TCheckbutton', background=bg_color, foreground=white)
    style.configure('TRadiobutton', background=bg_color, foreground=sunshine)
    style.configure('TEntry', fieldbackground=cotton_candy, foreground=deep_magenta,
                  insertcolor=deep_magenta)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background=deep_magenta, foreground=white,
                  font=('Comic Sans MS', 10, 'bold'), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', candy_purple)],
             foreground=[('selected', sunshine)])
    
    style.configure('Treeview', background=cotton_candy, foreground=deep_magenta,
                  fieldbackground=cotton_candy, font=('Comic Sans MS', 9),
                  rowheight=24)
    style.map('Treeview', 
             background=[('selected', candy_purple)],
             foreground=[('selected', white)])
    style.configure('Treeview.Heading', background=deep_magenta, foreground=white,
                  font=('Comic Sans MS', 10, 'bold'))
    
    style.configure('TScale', background=bg_color, troughcolor=deep_magenta)
    style.configure('TScrollbar', background=deep_magenta, troughcolor=bg_color,
                  arrowcolor=white)
    
    root.configure(bg=bg_color)
    return bg_color


def _apply_commander_keen_theme(style: ttk.Style, root) -> str:
    """COMMANDER KEEN - Classic DOS EGA/VGA palette!"""
    bg_color = "#0000aa"
    
    ega_black = "#000000"
    ega_magenta = "#aa00aa"
    ega_dark_gray = "#555555"
    ega_bright_blue = "#5555ff"
    ega_bright_green = "#55ff55"
    ega_bright_cyan = "#55ffff"
    ega_yellow = "#ffff55"
    ega_white = "#ffffff"
    ega_brown = "#aa5500"
    ega_cyan = "#00aaaa"
    
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=ega_yellow,
                  font=('Fixedsys', 10, 'bold'))
    style.configure('Header.TLabel', background=bg_color, foreground=ega_bright_green,
                  font=('Fixedsys', 12, 'bold'))
    
    style.configure('TButton', background=ega_bright_blue, foreground=ega_yellow,
                  font=('Fixedsys', 9, 'bold'))
    style.map('TButton', 
             background=[('active', ega_bright_cyan), ('pressed', ega_cyan)],
             foreground=[('active', ega_black)])
    
    style.configure('Control.TButton', background=ega_bright_green, foreground=ega_black,
                  font=('Fixedsys', 14, 'bold'), padding=10)
    style.map('Control.TButton',
             background=[('active', ega_yellow), ('pressed', ega_brown)],
             foreground=[('active', ega_black)])
    
    style.configure('TMenubutton', background=ega_bright_blue, foreground=ega_yellow)
    style.configure('TCheckbutton', background=bg_color, foreground=ega_bright_cyan)
    style.configure('TRadiobutton', background=bg_color, foreground=ega_bright_green)
    style.configure('TEntry', fieldbackground=ega_black, foreground=ega_bright_green,
                  insertcolor=ega_bright_green)
    
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab', background=ega_dark_gray, foreground=ega_yellow,
                  font=('Fixedsys', 10, 'bold'), padding=[15, 5])
    style.map('TNotebook.Tab', 
             background=[('selected', ega_bright_blue)],
             foreground=[('selected', ega_white)])
    
    style.configure('Treeview', background=ega_black, foreground=ega_bright_cyan,
                  fieldbackground=ega_black, font=('Fixedsys', 9),
                  rowheight=22)
    style.map('Treeview', 
             background=[('selected', ega_bright_blue)],
             foreground=[('selected', ega_yellow)])
    style.configure('Treeview.Heading', background=ega_magenta, foreground=ega_yellow,
                  font=('Fixedsys', 10, 'bold'))
    
    style.configure('TScale', background=bg_color, troughcolor=ega_dark_gray)
    style.configure('TScrollbar', background=ega_dark_gray, troughcolor=ega_black,
                  arrowcolor=ega_bright_green)
    
    root.configure(bg=bg_color)
    return bg_color
