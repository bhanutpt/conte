# Contributing to Conte

Thanks for your interest in improving Conte! This is an early-stage project, so
PRs that tighten up UX, add presets, or improve infrastructure are very welcome.

## Getting Started

1. Fork and clone the repo.
2. Create a virtual environment (Python 3.11+).
3. Install dependencies: `pip install -r requirements.txt`.
4. Run `python app.py` once to generate `~/.conte/config.json`.

## Preferred Workflow

1. Create a topic branch off `main`.
2. Make focused commits (Conventional Commit subjects are appreciated).
3. Run formatters/linting (currently `black`).
4. Manually test the panel for the contexts you touched (VS Code, browser, etc.).
5. Open a PR with:
   - Summary of the change.
   - Screenshots or short clips for UI tweaks.
   - Manual test notes (apps tried, results).

## Coding Standards

- Follow the existing style in `app.py` (two-space indents in UI code).
- Keep identifiers in `snake_case`; reserve `CamelCase` for types and uppercase
  for constants/macros.
- Use helper functions/modules for large data blobs (e.g., configs) instead of
  stuffing them into UI classes.
- When editing config defaults, update the docs to reflect new keys.

## Testing Checklist

- Does the window stay draggable/always-on-top after your change?
- Are rule matches switching when you alt-tab between supported apps?
- Is `config.json` regenerated correctly (delete `~/.conte/config.json` to test)?
- Did you try the system tray menu (open config, reload, quit)?

## Documentation

Add or update documentation whenever you:

- Introduce new configuration keys or presets.
- Change the setup process.
- Adjust platform support or dependencies.

See `README.md` for the current structure; feel free to expand it with new
insights.

## Questions?

File an issue or open a draft PR describing what you're planning. Feedback is
fastest when there's code to look at, but rough ideas are welcome too. Happy
hacking!
