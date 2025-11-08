# Conte

Conte is an always-on-top helper panel that shows the right cheat sheet for the
app you're using. It watches the active window on Windows and swaps to the
matching HTML snippet defined in a simple JSON config.

> Early prototype — expect rough edges. Feedback and contributions are welcome!

## Features
- 🧠 Detects the foreground app (exe + title) and switches contextual content
- 📋 Renders lightweight HTML (links + formatting) inside a PySide6 window
- 📁 Stores user config at `~/.conte/config.json`, generated on first run
- 🧲 Non-blocking, borderless panel that stays behind other windows by default
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
- `ui.always_on_back`: set to `true` (default) to keep Conte behind other apps; toggle
  `ui.always_on_top` if you prefer the classic overlay behavior

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
