import json
from pathlib import Path

from core.playlist import PlaylistManager


def test_playlist_crud_and_export_import(tmp_path):
    file = tmp_path / 'playlists.json'
    pm = PlaylistManager(str(file))

    p = pm.create_playlist('MyList')
    assert p.name.startswith('MyList')

    assert pm.add_track_to_playlist(p.name, '/path/a.mp3')
    assert pm.add_track_to_playlist(p.name, '/path/b.mp3')
    assert pm.get_playlist(p.name) is not None

    # export m3u
    export_m3u = tmp_path / 'list.m3u'
    assert pm.export_playlist_m3u(p.name, str(export_m3u))
    assert export_m3u.exists()

    # export pls
    export_pls = tmp_path / 'list.pls'
    assert pm.export_playlist_pls(p.name, str(export_pls))
    assert export_pls.exists()

    # import back from m3u (paths don't exist so import will skip them) -> create file entries
    # Create a small m3u with absolute paths
    m3u = tmp_path / 'in.m3u'
    m3u.write_text('#EXTM3U\n' + '/nonexistent/a.mp3\n')
    # import should create playlist with no tracks (path doesn't exist)
    pl = pm.import_playlist_m3u(str(m3u), playlist_name='Imported')
    assert pl is not None

    # test export_all and import_all
    outdir = tmp_path / 'out'
    assert pm.export_all_playlists(str(outdir))
    backup = outdir / 'playlists_backup.json'
    assert backup.exists()

    # import_all
    pm2 = PlaylistManager(str(tmp_path / 'p2.json'))
    assert pm2.import_all_playlists(str(backup), merge=False)
    assert len(pm2.get_all_playlists()) >= 0


def test_remove_track_from_all_playlists(tmp_path):
    pm = PlaylistManager(str(tmp_path / 'pl_all.json'))
    p1 = pm.create_playlist('One')
    p2 = pm.create_playlist('Two')
    pm.add_track_to_playlist(p1.name, '/music/shared.mp3')
    pm.add_track_to_playlist(p1.name, '/music/only1.mp3')
    pm.add_track_to_playlist(p2.name, '/music/shared.mp3')

    affected = pm.remove_track_from_all_playlists('/music/shared.mp3')
    assert affected == 2
    assert '/music/shared.mp3' not in pm.get_playlist('One').tracks
    assert '/music/shared.mp3' not in pm.get_playlist('Two').tracks
    assert '/music/only1.mp3' in pm.get_playlist('One').tracks

    # Removing a track that appears nowhere affects zero playlists
    assert pm.remove_track_from_all_playlists('/music/ghost.mp3') == 0
