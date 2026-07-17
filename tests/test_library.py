import json
import os
from pathlib import Path

import pytest

from core.library import Library, Track


def make_track_from_path(p: Path) -> Track:
    return Track(path=str(p), title=p.stem, artist='Artist', album='Album', duration=10.0)


def test_add_folder_scans_and_saves(tmp_path, monkeypatch):
    # Create fake folder with some audio files
    folder = tmp_path / 'music'
    folder.mkdir()
    (folder / 'a.mp3').write_text('fake')
    (folder / 'b.flac').write_text('fake')
    (folder / 'c.txt').write_text('not audio')

    lib_file = tmp_path / 'library.json'

    # Monkeypatch _extract_metadata to avoid real mutagen parsing
    def fake_extract(self, file_path):
        p = Path(file_path)
        if p.suffix.lower() in {'.mp3', '.flac'}:
            return make_track_from_path(p)
        return None

    monkeypatch.setattr(Library, '_extract_metadata', fake_extract)

    lib = Library(str(lib_file))
    added = lib.add_folder(str(folder))
    assert added == 2

    # Ensure tracks saved
    data = json.loads(lib_file.read_text(encoding='utf-8'))
    assert 'folders' in data and len(data['folders']) == 1
    assert 'tracks' in data and len(data['tracks']) == 2

    # get_all_tracks
    all_tracks = lib.get_all_tracks()
    assert len(all_tracks) == 2


def test_search_and_getters(tmp_path, monkeypatch):
    lib_file = tmp_path / 'library2.json'
    lib = Library(str(lib_file))

    t1 = Track(path=str(tmp_path / 'music' / 'song1.mp3'), title='Hello', artist='Alice', album='A', duration=3)
    t2 = Track(path=str(tmp_path / 'music' / 'song2.mp3'), title='World', artist='Bob', album='B', duration=4)
    t3 = Track(path=str(tmp_path / 'music' / 'song3.mp3'), title='Hello', artist='Alice', album='A', duration=5)

    lib.tracks = [t1, t2, t3]

    # search
    res = lib.search('hello')
    assert len(res) == 2

    # get by path
    assert lib.get_track_by_path(t2.path) == t2
    assert lib.get_tracks_by_paths([t1.path, t3.path]) == [t1, t3]

    # folder structure
    structure = lib.get_folder_structure()
    assert any(isinstance(v, list) for v in structure.values())

    # artists/albums
    artists = lib.get_all_artists()
    assert 'Alice' in artists and 'Bob' in artists
    albums = lib.get_all_albums()
    assert 'A' in albums and 'B' in albums

    # get by artist/album
    assert lib.get_tracks_by_artist('alice') == [t1, t3]
    assert lib.get_tracks_by_album('a') == [t1, t3]

    # duplicates
    dupes = lib.find_duplicates()
    assert any(len(group) > 1 for group in dupes)


def test_missing_and_remove(tmp_path):
    lib_file = tmp_path / 'library3.json'
    lib = Library(str(lib_file))

    existing = Track(path=str(tmp_path / 'music' / 'exists.mp3'), title='E', artist='A', album='A', duration=1)
    missing = Track(path=str(tmp_path / 'music' / 'missing.mp3'), title='M', artist='B', album='B', duration=1)
    lib.tracks = [existing, missing]

    # create only existing file
    (Path(existing.path)).parent.mkdir(parents=True, exist_ok=True)
    Path(existing.path).write_text('x')

    found_missing = lib.find_missing_files()
    assert len(found_missing) == 1
    assert found_missing[0].path == missing.path

    removed = lib.remove_missing_files()
    assert removed == 1
    assert all(t.path != missing.path for t in lib.tracks)


def test_delete_track_file_removes_from_source_and_index(tmp_path, monkeypatch):
    lib_file = tmp_path / 'library4.json'
    lib = Library(str(lib_file))

    song = tmp_path / 'music' / 'song.mp3'
    song.parent.mkdir(parents=True, exist_ok=True)
    song.write_text('audio')

    track = Track(path=str(song), title='S', artist='A', album='A', duration=1)
    lib.tracks = [track]

    # Stub send2trash so the test doesn't depend on a real Recycle Bin;
    # emulate its effect by removing the file from the source folder.
    trashed = []

    def fake_trash(p):
        trashed.append(p)
        os.remove(p)

    monkeypatch.setattr('send2trash.send2trash', fake_trash)

    success, error = lib.delete_track_file(str(song))
    assert success is True
    assert error is None
    assert len(trashed) == 1
    assert not song.exists()  # gone from the source folder
    assert lib.get_track_by_path(str(song)) is None
    # Change persisted
    data = json.loads(lib_file.read_text(encoding='utf-8'))
    assert len(data['tracks']) == 0


def test_delete_track_file_when_already_missing(tmp_path):
    lib_file = tmp_path / 'library5.json'
    lib = Library(str(lib_file))

    ghost = str(tmp_path / 'music' / 'ghost.mp3')
    track = Track(path=ghost, title='G', artist='A', album='A', duration=1)
    lib.tracks = [track]

    # File never existed; deletion should still succeed and purge the index entry
    success, error = lib.delete_track_file(ghost)
    assert success is True
    assert error is None
    assert lib.get_track_by_path(ghost) is None
