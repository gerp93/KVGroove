"""
KVGroove Themes
Wrapper around tkthemes library for the music player.

This module provides a thin compatibility layer around the standalone
tkthemes library (https://github.com/gerp93/KVG_Themes).
"""

# Re-export everything from tkthemes for backward compatibility
from tkthemes import (
    apply_theme,
    get_theme_list,
    get_theme,
    get_all_themes,
    theme_exists,
    register_theme,
    register_custom_theme,
    unregister_theme,
)
from typing import Dict


# Backward compatibility: create THEMES dict from tkthemes registry
def _build_themes_dict() -> Dict[str, Dict[str, str]]:
    """Build THEMES dict from tkthemes for backward compatibility."""
    themes = {}
    for theme_id, name in get_theme_list():
        theme_info = get_theme(theme_id)
        if theme_info:
            themes[theme_id] = {
                "name": theme_info.get("name", name),
                "icon": theme_info.get("icon", "")
            }
    return themes


THEMES = _build_themes_dict()
