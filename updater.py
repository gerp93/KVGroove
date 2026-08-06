"""Thin app-specific wrapper around kvg_updater (see KVG_Standards).

Supplies KVGroove's repo/app name/version and the zero-arg call shape
main_window.py uses. See kvg_updater's README for the full package.
"""
from pathlib import Path
from typing import Callable, Optional

from kvg_updater import (
    apply_update_and_restart as _apply_update_and_restart,
    check_for_update as _check_for_update,
    download_update as _download_update,
)

GITHUB_REPO = "gerp93/KVGroove"
APP_NAME = "KVGroove"

try:
    from _version import __version__ as CURRENT_VERSION
except ImportError:
    CURRENT_VERSION = "0.0.0-dev"


def check_for_update() -> Optional[dict]:
    return _check_for_update(GITHUB_REPO, APP_NAME, CURRENT_VERSION)


def download_update(download_url: str, progress_callback: Optional[Callable[[float], None]] = None) -> Path:
    return _download_update(download_url, APP_NAME, progress_callback)


def apply_update_and_restart(new_binary_path: Path) -> None:
    _apply_update_and_restart(new_binary_path, APP_NAME)
