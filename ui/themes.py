"""
KVGroove Themes
Applies VisualAssault (https://github.com/gerp93/VisualAssault) color themes
to the KVGroove Tkinter/ttk UI.

Exposes the same small API the rest of the app already calls
(apply_theme, get_theme_list, THEMES) so main_window.py/dialogs.py don't
need to change — only the underlying theme source does.
"""
from typing import Any, Dict, List, Tuple

from visual_assault_tkinter import THEMES as _VA_THEMES

# Backward-compatible shape: id -> {"name": ..., "icon": ...}. VisualAssault
# themes carry no icon; kept empty rather than removing the key so any
# caller doing THEMES[id]["icon"] still works.
THEMES: Dict[str, Dict[str, str]] = {
    theme_id: {"name": data["name"], "icon": ""}
    for theme_id, data in _VA_THEMES.items()
}


def get_theme_list() -> List[Tuple[str, str]]:
    """List of (theme_id, display_name) tuples, for menus/dialogs."""
    return [(theme_id, data["name"]) for theme_id, data in THEMES.items()]


def apply_theme(theme_id: str, style: Any, root: Any) -> str:
    """
    Apply a VisualAssault theme by id to the given ttk.Style/root window.

    Returns the background color, matching the old tkthemes apply_theme
    signature/contract that main_window.py relies on.
    """
    theme = _VA_THEMES.get(theme_id) or _VA_THEMES[next(iter(_VA_THEMES))]

    style.theme_use("clam")

    style.configure("TFrame", background=theme["background"])
    style.configure("TLabel", background=theme["background"], foreground=theme["foreground"])
    style.configure(
        "TButton",
        background=theme["buttonBackground"],
        foreground=theme["foreground"],
        bordercolor=theme["border"],
    )
    style.map(
        "TButton",
        background=[("disabled", theme["surface"]), ("active", theme["buttonHover"])],
        foreground=[("disabled", theme["textMuted"])],
    )
    style.configure("TMenubutton", background=theme["buttonBackground"], foreground=theme["foreground"])
    style.configure("TCheckbutton", background=theme["background"], foreground=theme["foreground"])
    style.map("TCheckbutton", background=[("active", theme["backgroundHover"])])
    style.configure("TRadiobutton", background=theme["background"], foreground=theme["foreground"])
    style.map("TRadiobutton", background=[("active", theme["backgroundHover"])])
    style.configure(
        "TEntry",
        fieldbackground=theme["surface"],
        foreground=theme["foreground"],
        bordercolor=theme["border"],
        insertcolor=theme["foreground"],
    )
    style.configure("TNotebook", background=theme["background"], bordercolor=theme["border"])
    style.configure(
        "TNotebook.Tab",
        background=theme["buttonBackground"],
        foreground=theme["foreground"],
        padding=(10, 4),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", theme["topBarBackground"])],
        foreground=[("selected", theme["foreground"])],
    )
    style.configure(
        "Treeview",
        background=theme["surface"],
        foreground=theme["foreground"],
        fieldbackground=theme["surface"],
        bordercolor=theme["border"],
    )
    style.map("Treeview", background=[("selected", theme["buttonHover"])])
    style.configure(
        "Treeview.Heading",
        background=theme["buttonBackground"],
        foreground=theme["foreground"],
    )

    root.configure(background=theme["background"])

    # tk.Menu (the menubar) isn't ttk-styled — restyle it manually, same as
    # KVGrainy's theming.py does for its raw tk widgets.
    menu = root.nametowidget(root["menu"]) if root["menu"] else None
    if menu is not None:
        _restyle_menu(menu, theme)

    return theme["background"]


def _restyle_menu(menu: Any, theme: Dict[str, str]) -> None:
    menu.configure(
        background=theme["surface"],
        foreground=theme["foreground"],
        activebackground=theme["buttonHover"],
        activeforeground=theme["foreground"],
    )
    for i in range(menu.index("end") + 1 if menu.index("end") is not None else 0):
        try:
            submenu_name = menu.entrycget(i, "menu")
        except Exception:
            continue
        if submenu_name:
            _restyle_menu(menu.nametowidget(submenu_name), theme)
