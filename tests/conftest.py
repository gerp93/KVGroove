import pytest
import tkinter as tk

@pytest.fixture(scope='session')
def tk_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        root.destroy()
    except Exception:
        pass
