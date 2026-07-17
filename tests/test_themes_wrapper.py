import pytest

import ui.themes as themes


def test_themes_dict_has_entries():
    # THEMES should be built from the tkthemes package
    assert isinstance(themes.THEMES, dict)
    assert len(themes.THEMES) > 0
    # common theme ids should be present
    assert 'light' in themes.THEMES or 'dark' in themes.THEMES


def test_get_theme_list_matches_THEMES():
    listed = dict(themes.get_theme_list())
    # Every theme returned by get_theme_list should appear in THEMES
    for tid, name in listed.items():
        assert tid in themes.THEMES
        assert 'name' in themes.THEMES[tid]
