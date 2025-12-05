# Standalone Themes Module - Extraction Plan

## Overview
This document outlines the plan to extract the current `ui/themes.py` module from KVGroove into a standalone, reusable Python package that can be used in any tkinter application.

**Planned Package Name:** `tkthemes` (or `ttk-themes`)
**Target Repository:** `github.com/kgerp/tkthemes` (or similar)

---

## Current State

The themes module currently lives in `KVGroove/ui/themes.py` and contains:
- 9 pre-built themes: Light, Dark, Neon, Retrowave, Hacker, Lava, Electric Lime, Bubblegum, Commander Keen
- Core functions: `apply_theme()`, `get_theme_list()`, individual `_apply_*_theme()` functions
- A `THEMES` registry dictionary with theme metadata

**Current Usage in KVGroove:**
```python
from ui.themes import apply_theme, get_theme_list, THEMES

style = ttk.Style()
apply_theme("neon", style, root)
```

---

## Extraction Goals

1. **Zero Dependencies** - Themes should work on any system with Python 3.7+ and tkinter
2. **Plug & Play** - Drop into any tkinter app with minimal setup
3. **Extensible** - Users can add custom themes via a simple API
4. **Well-Documented** - Clear examples, API docs, and theme development guide
5. **Published** - Available via PyPI for easy installation (`pip install tkthemes`)

---

## Phase 1: Refactoring for Reusability (Current KVGroove)

### Tasks
- [ ] Move `ui/themes.py` → Keep current location but prepare for extraction
- [ ] Remove any KVGroove-specific dependencies or imports
- [ ] Add comprehensive docstrings and type hints
- [ ] Create a `themes/` subpackage structure:
  ```
  ui/themes/
  ├── __init__.py           # Exports: apply_theme, get_theme_list, THEMES, register_theme
  ├── core.py              # Core theme engine
  ├── registry.py          # THEMES dictionary and registration logic
  └── builtins/            # Built-in themes
      ├── light.py
      ├── dark.py
      ├── neon.py
      ├── retrowave.py
      ├── hacker.py
      ├── lava.py
      ├── electric_lime.py
      ├── bubblegum.py
      └── commander_keen.py
  ```

### Expected Changes
- Split monolithic `themes.py` into modular files
- Add `register_theme()` function for custom themes
- Create theme base class or protocol for consistency
- Add validation and error handling

---

## Phase 2: Create Standalone Package

### Directory Structure
```
tkthemes/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── setup.py / pyproject.toml
├── requirements.txt        # (likely empty or minimal)
├── CONTRIBUTING.md
├── tests/
│   ├── test_core.py
│   ├── test_themes.py
│   └── test_registry.py
├── examples/
│   ├── basic_example.py
│   ├── custom_theme_example.py
│   └── demo_app.py          # Full demo with all themes
├── docs/
│   ├── api.md
│   ├── theme_development.md
│   ├── installation.md
│   └── examples.md
└── tkthemes/
    ├── __init__.py          # Package exports
    ├── core.py              # Theme engine
    ├── registry.py          # Theme registry
    ├── utils.py             # Helper functions
    └── themes/
        ├── __init__.py
        ├── light.py
        ├── dark.py
        ├── neon.py
        ├── retrowave.py
        ├── hacker.py
        ├── lava.py
        ├── electric_lime.py
        ├── bubblegum.py
        └── commander_keen.py
```

---

## Phase 3: API Design

### Core Public API

```python
from tkthemes import apply_theme, get_theme_list, register_custom_theme, AVAILABLE_THEMES

# Apply a built-in theme
style = ttk.Style()
apply_theme("neon", style, root_window)

# List available themes
themes = get_theme_list()  # Returns: ["light", "dark", "neon", ...]

# Register a custom theme
def my_theme_config(style, root):
    style.configure('TButton', background='#ff00ff', foreground='white')
    root.configure(bg='#1a1a1a')

register_custom_theme("my_theme", {
    "name": "My Custom Theme",
    "description": "A cool custom theme",
    "apply_fn": my_theme_config
})

# Check available themes
AVAILABLE_THEMES  # Dict of all themes (built-in + custom)
```

### Advanced Features (Phase 2+)

- Theme validation and linting
- Theme export/import (JSON format)
- Dark mode detection (system-level)
- Per-widget theme overrides
- Theme preview utility

---

## Phase 4: Documentation

### Files to Create

1. **README.md** - Features, quick start, screenshots
2. **docs/installation.md** - Installation methods
3. **docs/api.md** - Complete API reference
4. **docs/theme_development.md** - How to create custom themes
5. **docs/examples.md** - Various usage examples
6. **CONTRIBUTING.md** - How to contribute themes

### Example Section
```python
# Quick start example
import tkinter as tk
from tkinter import ttk
from tkthemes import apply_theme

root = tk.Tk()
root.title("Themed App")

style = ttk.Style()
apply_theme("neon", style, root)

ttk.Label(root, text="Hello, themed world!").pack(padx=20, pady=10)
ttk.Button(root, text="Click me").pack()

root.mainloop()
```

---

## Phase 5: Testing & Quality Assurance

### Test Coverage
- [ ] Test each theme applies without errors
- [ ] Test custom theme registration
- [ ] Test on Windows, macOS, Linux
- [ ] Test with different Python versions (3.7, 3.8, 3.9, 3.10, 3.11+)
- [ ] Test with different tkinter versions

### CI/CD Setup
- GitHub Actions workflow for testing
- Automated PyPI publishing on releases
- Code coverage reporting

---

## Phase 6: PyPI Publishing

### Preparation
- [ ] Choose final package name (e.g., `tkthemes`)
- [ ] Finalize version numbering (start at 0.1.0 or 1.0.0)
- [ ] Create PyPI account / set up publishing
- [ ] Add LICENSE file (MIT recommended)

### Publishing Checklist
- [ ] Create `setup.py` or `pyproject.toml`
- [ ] Tag release in git (`v1.0.0`)
- [ ] Build distribution (`python -m build`)
- [ ] Upload to PyPI (`python -m twine upload dist/*`)
- [ ] Verify installation works: `pip install tkthemes`

---

## Integration Path (After Extraction)

### KVGroove will do:
```python
# Instead of local import:
# from ui.themes import apply_theme, THEMES

# Use PyPI package:
from tkthemes import apply_theme, THEMES
```

### Benefits
- KVGroove gets cleaner (removes theme code)
- Themes are reusable in other projects
- Community can contribute new themes
- Easier maintenance and versioning

---

## Timeline Estimate

- **Phase 1 (Refactoring):** 1-2 hours
- **Phase 2 (Package Setup):** 1-2 hours
- **Phase 3 (API Design):** 2-3 hours
- **Phase 4 (Documentation):** 3-4 hours
- **Phase 5 (Testing):** 2-3 hours
- **Phase 6 (PyPI Publishing):** 1 hour

**Total Estimate:** 10-15 hours of focused work

---

## Future Enhancement Ideas

- [ ] Theme editor GUI tool
- [ ] Theme marketplace/sharing community
- [ ] Color scheme generator
- [ ] Accessibility-focused themes
- [ ] Animation/transition support
- [ ] Per-OS platform-native theme options
- [ ] Integration with color palette libraries (e.g., `colorsys`)

---

## Notes

- Current themes are highly opinionated (neon, bubblegum, etc.) — good for showcase, might want "standard" enterprise themes too
- Consider backward compatibility in version 1.0
- Community contributions could expand theme collection significantly
- Consider licensing third-party theme inspirations properly (e.g., Commander Keen theme)

---

## Links & Resources

- [tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [GitHub Actions for CI/CD](https://github.com/features/actions)
- [Semantic Versioning](https://semver.org/)

---

## Contact & Questions

When ready to start extraction, ensure:
1. All current KVGroove features still work after refactoring
2. No external dependencies are introduced
3. API is backward compatible with current KVGroove usage
