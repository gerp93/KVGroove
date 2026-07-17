import time
import types
import pytest

from core import player as player_module


class FakeMusic:
    def __init__(self):
        self._busy = False
        self._pos = 0
        self._volume = 0.5
        self._loaded = None

    def load(self, path):
        self._loaded = path

    def play(self, start=0):
        self._busy = True
        self._pos = int(start * 1000)

    def pause(self):
        self._busy = False

    def unpause(self):
        self._busy = True

    def stop(self):
        self._busy = False

    def get_busy(self):
        return self._busy

    def get_pos(self):
        return self._pos

    def set_volume(self, v):
        self._volume = v


class FakeMixer:
    def __init__(self):
        self.music = FakeMusic()

    def init(self, *args, **kwargs):
        return None

    def quit(self):
        return None


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    fake = FakeMixer()
    monkeypatch.setattr(player_module, 'pygame', types.SimpleNamespace(mixer=fake))
    yield


def test_load_play_pause_stop(monkeypatch, tmp_path):
    # Create fake audio file
    file = tmp_path / 'track.mp3'
    file.write_text('x')

    # Mock mutagen File to return object with info.length
    class FakeInfo:
        length = 2.5

    def fake_File(path):
        class A: pass
        a = A()
        a.info = FakeInfo()
        return a

    # Patch mutagen.File so player._get_duration picks up our fake
    monkeypatch.setattr('mutagen.File', fake_File, raising=False)

    ap = player_module.AudioPlayer()
    assert ap.load(str(file)) is True
    assert ap.get_duration() == 2.5

    assert ap.play() is True
    assert ap.is_playing is True

    ap.pause()
    assert ap.is_paused is True

    ap.play()
    assert ap.is_paused is False

    ap.seek(1.0)
    # seek should set position offset; get_position may return 0 due to fake
    ap.stop()
    assert ap.is_playing is False


def test_sleep_timer(monkeypatch):
    ap = player_module.AudioPlayer()
    called = {'f': False}

    def on_sleep():
        called['f'] = True

    ap.set_sleep_timer(0.001, callback=on_sleep)  # ~0.06s
    time.sleep(0.1)
    assert called['f'] is True
    assert not ap.is_sleep_timer_active()
