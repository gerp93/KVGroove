import random
from core.queue import PlayQueue


def test_queue_basic_operations():
    q = PlayQueue()
    q.add('a')
    q.add('b')
    q.add('c')

    assert len(q) == 3
    assert q.get_queue() == ['a', 'b', 'c']

    # play index
    assert q.play_index(1) == 'b'
    assert q.get_current() == 'b'

    # add_next
    q.add_next('x')
    # if current index >=0, inserted after current
    assert 'x' in q.get_queue()

    # remove
    removed = q.remove(0)
    assert removed == 'a'

    # previous/next
    q.play_index(0)
    assert q.get_next() is not None

    # repeat one
    q.set_repeat('one')
    cur = q.get_current()
    assert q.get_next() == cur

    # shuffle
    q = PlayQueue()
    for i in range(10): q.add(str(i))
    q.set_shuffle(True)
    assert q.is_shuffle() is True
    q.set_shuffle(False)
    assert q.is_shuffle() is False


def test_move_and_clear_upcoming():
    q = PlayQueue()
    q.add('a'); q.add('b'); q.add('c'); q.add('d')
    q.play_index(1)
    q.move_track(3,1)
    assert 'd' in q.get_queue()
    q.clear_upcoming()
    assert len(q.get_upcoming()) == 0


def test_remove_by_path_adjusts_current_index():
    q = PlayQueue()
    q.add('a'); q.add('b'); q.add('c'); q.add('d')
    q.play_index(2)  # current is 'c'

    # Remove a track before current -> index shifts down, current stays 'c'
    removed = q.remove_by_path('a')
    assert removed == 1
    assert q.get_queue() == ['b', 'c', 'd']
    assert q.get_current() == 'c'

    # Remove the current track -> index clamps, current becomes next available
    removed = q.remove_by_path('c')
    assert removed == 1
    assert q.get_queue() == ['b', 'd']
    assert q.get_current() in ('b', 'd')

    # Removing a path not present returns 0
    assert q.remove_by_path('zzz') == 0


def test_remove_by_path_removes_all_occurrences():
    q = PlayQueue()
    q.add('a'); q.add('dup'); q.add('b'); q.add('dup')
    removed = q.remove_by_path('dup')
    assert removed == 2
    assert 'dup' not in q.get_queue()
