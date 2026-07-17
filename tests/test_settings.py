import json
from pathlib import Path

import pytest

from core.settings import SettingsManager


def test_settings_defaults_and_save(tmp_path):
    settings_file = tmp_path / "settings.json"
    sm = SettingsManager(str(settings_file))

    # defaults exist
    assert sm.get('volume') == 0.7
    assert sm.get('theme') == 'light'

    # set some values
    sm.set('volume', 0.3)
    sm.set('theme', 'dark')

    # file should exist
    assert settings_file.exists()

    data = json.loads(settings_file.read_text(encoding='utf-8'))
    assert data['volume'] == 0.3
    assert data['theme'] == 'dark'


def test_recently_played_trimming(tmp_path):
    settings_file = tmp_path / "settings2.json"
    sm = SettingsManager(str(settings_file))
    sm.set('recently_played_max', 3)

    sm.add_to_recently_played('a')
    sm.add_to_recently_played('b')
    sm.add_to_recently_played('c')
    sm.add_to_recently_played('d')

    rp = sm.get_recently_played()
    assert rp == ['d', 'c', 'b']

    sm.clear_recently_played()
    assert sm.get_recently_played() == []


def test_favorites_toggle_and_remove(tmp_path):
    settings_file = tmp_path / "settings3.json"
    sm = SettingsManager(str(settings_file))

    assert sm.get_favorites() == []
    assert sm.toggle_favorite('song1') is True
    assert sm.is_favorite('song1')
    assert sm.toggle_favorite('song1') is False
    assert not sm.is_favorite('song1')

    sm.add_favorite('song2')
    assert 'song2' in sm.get_favorites()
    sm.remove_favorite('song2')
    assert 'song2' not in sm.get_favorites()


def test_export_import(tmp_path):
    settings_file = tmp_path / "settings4.json"
    sm = SettingsManager(str(settings_file))
    sm.set('volume', 0.9)
    export_path = tmp_path / 'export.json'
    assert sm.export_settings(str(export_path))

    # create new manager and import
    sm2_file = tmp_path / 'other.json'
    sm2 = SettingsManager(str(sm2_file))
    assert sm2.import_settings(str(export_path))
    assert sm2.get('volume') == 0.9


def test_remove_from_recently_played(tmp_path):
    settings_file = tmp_path / "settings_recent.json"
    sm = SettingsManager(str(settings_file))

    sm.add_to_recently_played('a')
    sm.add_to_recently_played('b')
    assert 'a' in sm.get_recently_played()

    sm.remove_from_recently_played('a')
    assert 'a' not in sm.get_recently_played()
    assert 'b' in sm.get_recently_played()

    # Removing a path not present is a no-op
    sm.remove_from_recently_played('zzz')
    assert 'b' in sm.get_recently_played()
