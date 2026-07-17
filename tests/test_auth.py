from core.auth import Auth


def test_auth_set_verify_remove(tmp_path):
    path = tmp_path / 'auth.json'
    a = Auth(str(path))
    assert not a.is_password_set()

    a.set_password('secret')
    assert a.is_password_set()
    assert a.verify_password('secret')
    assert not a.verify_password('wrong')

    assert a.change_password('secret', 'new') is True
    assert a.verify_password('new')

    a.remove_password()
    assert a.is_password_set() is False
