import tkinter as tk
from ui.dialogs import SettingsDialog
from core.settings import SettingsManager
from ui.themes import get_theme_list


def test_settings_dialog_builds_theme_radios(tk_root, tmp_path):
    settings_file = tmp_path / 'settings_dialog.json'
    sm = SettingsManager(str(settings_file))
    dlg = SettingsDialog(parent=tk_root, settings=sm)

    # Count radiobuttons inside the dialog's widgets related to theme
    # Heuristic: find widgets with variable name 'theme_var' is on the dialog
    theme_var = dlg.theme_var
    # Gather all radiobuttons in dialog (ttk.Radiobutton) and count those
    # whose 'value' corresponds to a theme id.
    from tkinter import ttk
    radios = []
    def walk(w):
        for c in w.winfo_children():
            radios.append(c) if isinstance(c, ttk.Radiobutton) else None
            walk(c)
    walk(dlg.dialog)

    theme_ids = {tid for tid, _ in get_theme_list()}
    matched = []
    for r in radios:
        try:
            val = r.cget('value')
        except Exception:
            val = None
        if val in theme_ids:
            matched.append(r)

    # Number of radios should match number of themes in registry
    expected = len(theme_ids)
    assert len(matched) == expected

    # Cleanup
    dlg.dialog.destroy()
