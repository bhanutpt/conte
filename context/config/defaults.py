"""Built-in Conte configuration presets."""

DEFAULT_CONFIG = {
    "ui": {
        "base_width_px": 945,
        "base_height_px": 532,
        "font_family": "Inter, Segoe UI, Arial",
        "font_size_pt": 12,
        "width_px": 945,
        "height_px": 532,
        "panel_scale": 1.0,
        "opacity": 0.95,
        "always_on_top": False,
        "always_on_back": True,
        "borderless": True,
        "start_maximized": True,
        "lock_aspect_ratio": True,
        "aspect_ratio": [16, 9],
    },
    "rules": [
        {
            "name": "VS Code – General",
            "match": {"exe": ["Code.exe", "code.exe"], "title_regex": ".*"},
            "content_html": """
                <div class="shortcut-grid two-col">
                  <section>
                    <h3>General</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;P</td><td>Command Palette</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;P</td><td>Quick Open</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;N</td><td>New window</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;W</td><td>Close window</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;,</td><td>User Settings</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;S</td><td>Keyboard Shortcuts</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;0</td><td>Fold all</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;J</td><td>Unfold all</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Basic Editing</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;X</td><td>Cut line (no selection)</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;C</td><td>Copy line (no selection)</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;↑ / ↓</td><td>Move line up/down</td></tr>
                      <tr><td class="shortcut">Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;↑ / ↓</td><td>Copy line up/down</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;K</td><td>Delete line</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Enter</td><td>Insert line below</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;Enter</td><td>Insert line above</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;\\</td><td>Jump to bracket</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;]</td><td>Indent line</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;[</td><td>Outdent line</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;/</td><td>Toggle line comment</td></tr>
                      <tr><td class="shortcut">Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;A</td><td>Toggle block comment</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;↓</td><td>Copy selection below</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Z / Ctrl&nbsp;+&nbsp;Y</td><td>Undo / Redo</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Multi-cursor &amp; Selection</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;Click</td><td>Insert cursor</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Alt&nbsp;+&nbsp;↑ / ↓</td><td>Insert cursor above/below</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;L</td><td>Select all occurrences</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;F2</td><td>Select all occurrences of word</td></tr>
                      <tr><td class="shortcut">Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;→ / ←</td><td>Expand / shrink selection</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;Arrow</td><td>Column selection</td></tr>
                      <tr><td class="shortcut">Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;I</td><td>Insert cursor at line ends</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;D</td><td>Add selection to next find match</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;U</td><td>Soft undo cursor state</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Search &amp; Replace</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;F</td><td>Find</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;H</td><td>Replace</td></tr>
                      <tr><td class="shortcut">F3 / Shift&nbsp;+&nbsp;F3</td><td>Find next / previous</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;Enter</td><td>Select all matches</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;F3</td><td>Find selection</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;F</td><td>Find in files</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;H</td><td>Replace in files</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Navigation</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;T</td><td>Go to symbol</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;G</td><td>Go to line</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;O</td><td>Go to symbol in file</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;M</td><td>Toggle Problems</td></tr>
                      <tr><td class="shortcut">F8 / Shift&nbsp;+&nbsp;F8</td><td>Next / previous problem</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;← / →</td><td>Back / Forward</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Tab</td><td>Navigate history</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;PageDown / PageUp</td><td>Next / previous editor</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;\\</td><td>Navigate matching bracket</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Editor Management</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;N</td><td>New file</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;W</td><td>Close editor</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;W</td><td>Close all editors</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;\\</td><td>Split editor</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;1 / 2 / 3</td><td>Focus editor group</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;← / →</td><td>Focus previous / next group</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Shift&nbsp;+&nbsp;Ctrl&nbsp;+&nbsp;← / →</td><td>Move editor group</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;Alt&nbsp;+&nbsp;← / →</td><td>Move editor between groups</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>File Management</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;O</td><td>Open file</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;S</td><td>Save</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;S</td><td>Save As</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;S</td><td>Save all</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;F4</td><td>Close file</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;T</td><td>Reopen closed editor</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Enter</td><td>Keep preview editor</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Display</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;B</td><td>Toggle activity bar / side bar</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;E</td><td>Explorer focus</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;F</td><td>Search view</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;G</td><td>Source Control</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;D</td><td>Run &amp; Debug</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;X</td><td>Extensions</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;+ / −</td><td>Zoom in / out</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Z</td><td>Zen mode</td></tr>
                      <tr><td class="shortcut">F11 / Shift&nbsp;+&nbsp;F11</td><td>Fullscreen / leave fullscreen</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Debug</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">F5</td><td>Start / Continue</td></tr>
                      <tr><td class="shortcut">Shift&nbsp;+&nbsp;F5</td><td>Stop</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;F5</td><td>Run without debugging</td></tr>
                      <tr><td class="shortcut">F9</td><td>Toggle breakpoint</td></tr>
                      <tr><td class="shortcut">F10</td><td>Step over</td></tr>
                      <tr><td class="shortcut">F11 / Shift&nbsp;+&nbsp;F11</td><td>Step into / out</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K Ctrl&nbsp;+&nbsp;I</td><td>Show hover</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;F9</td><td>Remove breakpoints</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Integrated Terminal</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;`</td><td>Toggle terminal</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;`</td><td>New terminal</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;C</td><td>Copy selection</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;V</td><td>Paste into terminal</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;↑ / ↓</td><td>Scroll up / down</td></tr>
                      <tr><td class="shortcut">Shift&nbsp;+&nbsp;PageUp / PageDown</td><td>Scroll page</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K</td><td>Clear terminal</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;← / →</td><td>Move between terminals</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;5</td><td>Split terminal</td></tr>
                    </table>
                  </section>
                </div>
                <p class="shortcut-note">
                    Full reference: <a href="https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf">VS Code keyboard shortcuts (Windows)</a>
                </p>
            """,
        },
        {
            "name": "VS Code – Extensions view",
            "match": {"exe": ["Code.exe", "code.exe"], "title_regex": ".*Extensions.*"},
            "content_html": """
                <div class="shortcut-grid">
                  <section>
                    <h3>Extensions</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;X</td><td>Open Extensions view</td></tr>
                      <tr><td class="shortcut">Enter</td><td>Install/enable selected</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;F</td><td>Search marketplace</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Profiles & Settings</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;,</td><td>Open Settings</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;K, Ctrl&nbsp;+&nbsp;S</td><td>Keyboard Shortcuts editor</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;P &rarr; “Profiles”</td><td>Switch profile</td></tr>
                    </table>
                  </section>
                </div>
                <p class="shortcut-note">Use Profiles to isolate language/tooling-specific extension sets.</p>
            """,
        },
        {
            "name": "Chrome/Edge – Tabs & Nav",
            "match": {"exe": ["chrome.exe", "msedge.exe"], "title_regex": ".*"},
            "content_html": """
                <div class="shortcut-grid">
                  <section>
                    <h3>Tabs</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;T</td><td>New tab</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;W</td><td>Close tab</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;T</td><td>Reopen closed tab</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Tab</td><td>Next tab</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Navigation</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;L</td><td>Focus address bar</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;← / →</td><td>Back / forward</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;B</td><td>Toggle bookmarks bar</td></tr>
                      <tr><td class="shortcut">F12 / Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;I</td><td>Developer Tools</td></tr>
                    </table>
                  </section>
                </div>
            """,
        },
        {
            "name": "Windows Explorer – Files",
            "match": {"exe": ["explorer.exe"], "title_regex": ".*"},
            "content_html": """
                <div class="shortcut-grid">
                  <section>
                    <h3>Navigation</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;↑</td><td>Up one folder</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;← / →</td><td>Back / forward</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;L</td><td>Focus path bar</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Files & Windows</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;N</td><td>New window</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;N</td><td>New folder</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;Enter</td><td>Properties</td></tr>
                    </table>
                  </section>
                </div>
            """,
        },
        {
            "name": "Terminal (cmd/PowerShell/WT)",
            "match": {
                "exe": ["cmd.exe", "powershell.exe", "pwsh.exe", "WindowsTerminal.exe"],
                "title_regex": ".*",
            },
            "content_html": """
                <div class="shortcut-grid">
                  <section>
                    <h3>Core</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;C</td><td>Cancel task</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;L / cls</td><td>Clear screen</td></tr>
                      <tr><td class="shortcut">↑ / ↓</td><td>Command history</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>Windows Terminal</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;C / V</td><td>Copy / paste</td></tr>
                      <tr><td class="shortcut">Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;T</td><td>New tab</td></tr>
                      <tr><td class="shortcut">Alt&nbsp;+&nbsp;Shift&nbsp;+&nbsp;D</td><td>Split pane</td></tr>
                    </table>
                  </section>
                  <section>
                    <h3>PowerShell Aliases</h3>
                    <table class="shortcut-table">
                      <tr><td class="shortcut">gci</td><td>List items (ls)</td></tr>
                      <tr><td class="shortcut">ii&nbsp;.</td><td>Open Explorer</td></tr>
                      <tr><td class="shortcut">code&nbsp;.</td><td>Open folder in VS Code</td></tr>
                    </table>
                  </section>
                </div>
            """,
        },
    ],
    "fallback_html": """
        <h2>Conte</h2>
        <p>No rule matched the active app. Edit your rules in <code>~/.conte/config.json</code>.</p>
        <p>Create entries with <b>match.exe</b> (list of process names) and optional <b>match.title_regex</b>, then provide a <b>content_html</b> snippet.</p>
    """,
}
