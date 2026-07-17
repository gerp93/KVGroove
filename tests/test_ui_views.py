import tkinter as tk
from core.library import Library, Track
from core.playlist import PlaylistManager
from core.queue import PlayQueue
from ui.library_view import LibraryView
from ui.playlist_view import PlaylistView
from ui.queue_view import QueueView


def make_track(path, title='T'):
    return Track(path=path, title=title, artist='A', album='AL', duration=12)


def test_library_view_refresh_and_search(tk_root, tmp_path):
    lib_file = tmp_path / 'lib.json'
    lib = Library(str(lib_file))
    t1 = make_track(str(tmp_path / 'a.mp3'), 'Hello')
    t2 = make_track(str(tmp_path / 'b.mp3'), 'World')
    lib.tracks = [t1, t2]

    settings = type('S', (), {
        'is_favorite': lambda self, p: False,
        'get_favorites': lambda self: [],
        'get_recently_played': lambda self: []
    })()

    lv = LibraryView(tk_root, lib, lambda t: None, lambda t: None, lambda t,n: None, lambda: [], settings)
    lv._on_search()
    assert 'tracks' in lv.status_var.get() or '0' in lv.status_var.get()
    lv._sort_by('title')


def test_playlist_view_basic_ops(tk_root, tmp_path):
    pm_file = tmp_path / 'pl.json'
    pm = PlaylistManager(str(pm_file))
    lib = Library(str(tmp_path / 'lib2.json'))
    t = make_track(str(tmp_path / 'song.mp3'), 'S')
    lib.tracks = [t]

    pv = PlaylistView(tk_root, pm, lib, lambda tr: None, lambda lst: None)
    pl = pm.create_playlist('P')
    pm.add_track_to_playlist(pl.name, t.path)
    pv._refresh_playlist_list()
    pv._on_playlist_select()


def test_queue_view_refresh_and_now_playing(tk_root, tmp_path):
    lib = Library(str(tmp_path / 'lib3.json'))
    t = make_track(str(tmp_path / 's.mp3'), 'Song')
    lib.tracks = [t]
    q = PlayQueue()
    q.add(t.path)
    q.play_index(0)

    qv = QueueView(tk_root, q, lib, lambda idx: None)
    qv.refresh()
    assert 'tracks' in qv.status_var.get() or '0' in qv.status_var.get()
    qv.set_now_playing(t)
    assert 'Song' in qv.now_playing_var.get()
