"""Built-in Conte configuration presets."""

DEFAULT_CONFIG = {
    "ui": {
        "font_family": "Inter, Segoe UI, Arial",
        "font_size_pt": 11,
        "width_px": 460,
        "height_px": 320,
        "opacity": 0.92,
        "always_on_top": True,
        "borderless": True,
    },
    "rules": [
        {
            "name": "VS Code – General",
            "match": {"exe": ["Code.exe", "code.exe"], "title_regex": ".*"},
            "content_html": """
                <h2>VS Code – Essentials</h2>
                <ul>
                  <li><b>Cmd/Ctrl + P</b>: Quick Open</li>
                  <li><b>Cmd/Ctrl + Shift + P</b>: Command Palette</li>
                  <li><b>Alt + Click</b>: Multiple cursors</li>
                  <li><b>Cmd/Ctrl + D</b>: Add next match</li>
                  <li><b>Cmd/Ctrl + /</b>: Toggle line comment</li>
                  <li><b>Shift + Alt + ↑/↓</b>: Copy line up/down</li>
                  <li><b>Cmd/Ctrl + B</b>: Toggle sidebar</li>
                </ul>
                <p>More:</p>
                <a
                    href=
                    "https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf">
                    Official cheat sheet
                    </a>
                </p>
            """,
        },
        {
            "name": "VS Code – Extensions view",
            "match": {"exe": ["Code.exe", "code.exe"], "title_regex": ".*Extensions.*"},
            "content_html": """
                <h2>VS Code – Extensions</h2>
                <ul>
                  <li>Search: <b>Cmd/Ctrl + Shift + X</b>, then type extension name</li>
                  <li>Enable/Disable: Use gear icon next to extension</li>
                  <li>Quick Manage: <b>Cmd/Ctrl + ,</b> to open Settings</li>
                </ul>
                <p>Tip: Use <b>Profiles</b> to isolate extension sets (gear → Profiles).</p>
            """,
        },
        {
            "name": "Chrome/Edge – Tabs & Nav",
            "match": {"exe": ["chrome.exe", "msedge.exe"], "title_regex": ".*"},
            "content_html": """
                <h2>Browser – Tabs & Navigation</h2>
                <ul>
                  <li><b>Ctrl + L</b>: Focus address bar</li>
                  <li><b>Ctrl + T</b> / <b>Ctrl + W</b>: New/Close tab</li>
                  <li><b>Ctrl + Shift + T</b>: Reopen closed tab</li>
                  <li><b>Ctrl + Tab</b> / <b>Ctrl + Shift + Tab</b>: Next/Prev tab</li>
                  <li><b>Alt + Left/Right</b>: Back/Forward</li>
                  <li><b>Ctrl + Shift + B</b>: Toggle bookmarks bar</li>
                </ul>
                <p>DevTools: <b>F12</b> or <b>Ctrl + Shift + I</b></p>
            """,
        },
        {
            "name": "Windows Explorer – Files",
            "match": {"exe": ["explorer.exe"], "title_regex": ".*"},
            "content_html": """
                <h2>Explorer – Handy Shortcuts</h2>
                <ul>
                  <li><b>Alt + ↑</b>: Up one folder</li>
                  <li><b>Ctrl + L</b>: Focus path</li>
                  <li><b>Ctrl + N</b>: New window</li>
                  <li><b>Ctrl + Shift + N</b>: New folder</li>
                  <li><b>Alt + Enter</b>: Properties</li>
                </ul>
            """,
        },
        {
            "name": "Terminal (cmd/PowerShell/WT)",
            "match": {
                "exe": ["cmd.exe", "powershell.exe", "pwsh.exe", "WindowsTerminal.exe"],
                "title_regex": ".*",
            },
            "content_html": """
                <h2>Terminal – Basics</h2>
                <ul>
                  <li><b>Ctrl + C</b>: Cancel task</li>
                  <li><b>Ctrl + L</b> or <b>cls</b>: Clear</li>
                  <li><b>Up/Down</b>: History</li>
                  <li><b>Ctrl + Shift + C/V</b>: Copy/Paste (WT)</li>
                </ul>
                <p>PowerShell tips: <code>gci</code> (ls), <code>ii .</code> (open explorer), <code>code .</code> (open VS Code)</p>
            """,
        },
    ],
    "fallback_html": """
        <h2>Conte</h2>
        <p>No rule matched the active app. Edit your rules in <code>~/.conte/config.json</code>.</p>
        <p>Create entries with <b>match.exe</b> (list of process names) and optional <b>match.title_regex</b> and set <b>content_html</b>.</p>
    """,
}
