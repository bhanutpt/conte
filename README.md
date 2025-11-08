# Conte

Conte is an always-on-top helper panel that shows the right cheat sheet for the
app you're using. It watches the active window on Windows and swaps to the
matching HTML snippet defined in a simple JSON config.

> Early prototype — expect rough edges. Feedback and contributions are welcome!

## Features
- 🧠 Detects the foreground app (exe + title) and switches contextual content
- 📋 Renders lightweight HTML (links + formatting) inside a PySide6 window
- 📁 Stores user config at `~/.conte/config.json`, generated on first run
- 🧲 Full-screen reference board (945 × 532 default) that stays behind other windows
- 🪟 Windows-first implementation with room for future Mac/Linux adapters

## Requirements
- Python 3.11+ (tested on 3.12)
- Windows with [`pywin32`](https://pypi.org/project/pywin32/) support
- Dependencies from `requirements.txt` (PySide6, psutil, pywin32)

## Quick Start
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The first launch creates `~/.conte/config.json` using the built-in defaults
from `context/config/defaults.py`. Edit that file to customize UI preferences or
add new rules.

## Configuration

Each rule in the config looks like:

```json
{
  "name": "VS Code – General",
  "match": {
    "exe": ["Code.exe", "code.exe"],
    "title_regex": ".*"
  },
  "content_html": "<h2>Shortcuts</h2>..."
}
```

- `match.exe`: list of executable names (case-sensitive on Windows)
- `match.title_regex`: optional regex run against the window title
- `content_html`: small HTML fragment rendered in the panel
- `fallback_html`: global HTML used when no rule matches
- `ui.always_on_back`: set to `true` (default) to keep Conte behind other apps.
  Setting `ui.always_on_top` to `true` automatically disables `always_on_back`.
  Older configs are auto-migrated to this behavior so the window never steals focus.
- `ui.start_maximized`: when `true` Conte launches maximized so you can mirror
  large-format reference sheets (VS Code style). Set to `false` to go back to a
  floating compact panel.
- `ui.lock_aspect_ratio`: keeps the panel locked to the configured aspect (default
  16:9 landscape). When enabled the app recomputes height from the chosen width
  (default 945×532) so large reference posters fit without manual tweaking.
- `ui.aspect_ratio`: optional `[width, height]` pair (e.g., `[16, 9]` or `[9, 16]`)
  used when `ui.lock_aspect_ratio` is `true`.
- `ui.base_width_px` / `ui.base_height_px`: logical design size. Combined with
  `ui.panel_scale` you can create larger/smaller layouts without editing every
  rule.
- `ui.panel_scale`: multiplier applied to `base_width_px` (and derived height) to
  scale the whole panel while keeping the aspect ratio intact. Values between
  0.2 and 4.0 are supported; e.g., `panel_scale: 1.25` produces a 1180 px wide sheet.

The built-in presets in `context/config/defaults.py` mimic the two-column layout
from the official VS Code keyboard shortcut posters. Use the provided
`.shortcut-grid` and `.shortcut-table` classes to keep a consistent look across
apps.

The helper `context/config/defaults.py` contains the shipping presets. You can
copy-paste sections from there into your personal config as a starting point.

## Project Structure

```
app.py                   # Main PySide6 application
context/config/          # Built-in configuration helpers & presets
config.json              # Example user config checked into the repo
requirements.txt         # Runtime dependencies
```

## Development Workflow

1. Create & activate a virtual environment.
2. Install dependencies via `pip install -r requirements.txt`.
3. Run lint/format checks (`black` via `pyproject.toml`).
4. Launch `python app.py` and exercise common app contexts (VS Code, browser,
   terminal) to verify rules switch as expected.

After editing `context/config/defaults.py`, delete `~/.conte/config.json` to
regenerate it with the updated schema (or manually merge the changes).

## Roadmap Ideas
- Cross-platform active-window adapters
- In-app config editor with live preview
- Markdown support + component library for richer content
- Packaging via MSIX/winget

---

Have ideas or spot issues? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance.
