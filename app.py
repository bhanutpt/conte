#!/usr/bin/env python3
# Conte – a tiny always‑on‑top helper panel that switches content based on the active app
# OS: Windows-first (uses pywin32), but structured for future macOS/Linux adapters.
#
# Features (MVP):
#  • Always-on-top, borderless, draggable mini window you can park on any monitor
#  • Auto-detects active window (exe + title) and swaps to matching cheat-sheet
#  • User-editable JSON config created on first run (~/.conte/config.json)
#  • Simple HTML rendering (links clickable)
#  • System tray menu: Open config, Reload, Opacity, Quit
#
# Dependencies:
#   pip install PySide6 psutil pywin32
#
# Run:
#   python app.py
#
# Autostart (Windows):
#   Create shortcut of this script in shell:startup (Start → Run → shell:startup) or use Task Scheduler.

import os
import sys
import json

# import time
# import threading
import re
import webbrowser
from dataclasses import dataclass

from context.config import get_default_config

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

# --- Windows active-window inspection ---
ACTIVE_WIN_SUPPORTED = True
try:
    import win32gui
    import win32process
    import psutil
except Exception:
    ACTIVE_WIN_SUPPORTED = False

APP_DIR = os.path.expanduser("~/.conte")
CONFIG_PATH = os.path.join(APP_DIR, "config.json")


@dataclass
class ActiveContext:
    exe: str = ""
    title: str = ""


def ensure_config():
    os.makedirs(APP_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(get_default_config(), f, indent=2)


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # Basic sanity defaults
    cfg.setdefault("ui", {})
    cfg["ui"].setdefault("opacity", 0.92)
    cfg["ui"].setdefault("width_px", 460)
    cfg["ui"].setdefault("height_px", 320)
    cfg["ui"].setdefault("always_on_top", False)
    cfg["ui"].setdefault("always_on_back", True)
    cfg["ui"].setdefault("borderless", True)
    cfg.setdefault("rules", [])
    cfg.setdefault("fallback_html", "<p>Configure me in ~/.conte/config.json</p>")
    return cfg


# --- Active window query (Windows) ---


def get_active_window_info() -> ActiveContext:
    if not ACTIVE_WIN_SUPPORTED:
        return ActiveContext("", "")
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return ActiveContext("", "")
        title = win32gui.GetWindowText(hwnd) or ""
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        exe = ""
        if pid:
            try:
                p = psutil.Process(pid)
                exe = p.name() or ""
            except Exception:
                exe = ""
        return ActiveContext(exe=exe, title=title)
    except Exception:
        return ActiveContext("", "")


# --- UI ---
class Panel(QtWidgets.QMainWindow):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.setWindowTitle("Conte")
        self.setWindowFlag(
            Qt.WindowStaysOnTopHint, self.cfg["ui"].get("always_on_top", False)
        )
        self.setWindowFlag(
            Qt.WindowStaysOnBottomHint, self.cfg["ui"].get("always_on_back", False)
        )
        if self.cfg["ui"].get("borderless", True):
            self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.resize(
            self.cfg["ui"].get("width_px", 460), self.cfg["ui"].get("height_px", 320)
        )
        self.setWindowOpacity(float(self.cfg["ui"].get("opacity", 0.92)))

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Header bar
        header = QtWidgets.QHBoxLayout()
        self.lbl_app = QtWidgets.QLabel("")
        self.lbl_app.setStyleSheet("font-weight:600;")
        header.addWidget(self.lbl_app)
        header.addStretch(1)

        self.btn_open_cfg = QtWidgets.QToolButton()
        self.btn_open_cfg.setText("⚙")
        self.btn_open_cfg.setToolTip("Open config")
        self.btn_open_cfg.clicked.connect(self.open_config)
        header.addWidget(self.btn_open_cfg)

        self.btn_close = QtWidgets.QToolButton()
        self.btn_close.setText("✕")
        self.btn_close.setToolTip("Quit")
        self.btn_close.clicked.connect(QtWidgets.QApplication.instance().quit)
        header.addWidget(self.btn_close)

        layout.addLayout(header)

        # Viewer
        self.view = QtWidgets.QTextBrowser()
        self.view.setOpenExternalLinks(True)
        font = self.view.font()
        try:
            font.setFamilies([self.cfg["ui"].get("font_family", "Segoe UI")])
        except Exception:
            font.setFamily(self.cfg["ui"].get("font_family", "Segoe UI"))
        font.setPointSize(int(self.cfg["ui"].get("font_size_pt", 11)))
        self.view.setFont(font)
        self.view.setStyleSheet(
            "QTextBrowser{background:#111418;color:#e6e6e6;border:1px solid #2a2f35;border-radius:10px;padding:10px;} a{color:#7ab6ff;}"
        )
        layout.addWidget(self.view, 1)

        # Dragging for borderless window
        self._drag_pos = None

        # Tray
        self.tray = QtWidgets.QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        menu = QtWidgets.QMenu()
        act_show = menu.addAction("Show/Hide")
        act_show.triggered.connect(self.toggle_visible)
        act_reload = menu.addAction("Reload config")
        act_reload.triggered.connect(self.reload_config)
        menu.addSeparator()
        op_sub = menu.addMenu("Opacity")
        for pct in [1.0, 0.95, 0.9, 0.85, 0.8]:
            a = op_sub.addAction(f"{int(pct*100)}%")
            a.triggered.connect(lambda _, p=pct: self.setWindowOpacity(p))
        menu.addSeparator()
        act_quit = menu.addAction("Quit")
        act_quit.triggered.connect(QtWidgets.QApplication.instance().quit)
        self.tray.setContextMenu(menu)
        self.tray.show()

        self.last_ctx = ActiveContext("", "")
        self.apply_content(self.cfg.get("fallback_html", ""))

        # Watcher timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(800)
        self.timer.timeout.connect(self.tick)
        self.timer.start()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._drag_pos = (
                e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            e.accept()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if self._drag_pos and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            e.accept()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        self._drag_pos = None

    def toggle_visible(self):
        self.setVisible(not self.isVisible())

    def open_config(self):
        # Open the config file in default editor
        if os.path.exists(CONFIG_PATH):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(CONFIG_PATH))
        else:
            webbrowser.open("https://")

    def reload_config(self):
        try:
            self.cfg = load_config()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self, "Config error", f"Failed to load config:\n{e}"
            )
        # re-apply UI tunables
        self.setWindowOpacity(float(self.cfg["ui"].get("opacity", 0.92)))

    def tick(self):
        ctx = get_active_window_info()
        if ctx.exe != self.last_ctx.exe or ctx.title != self.last_ctx.title:
            self.last_ctx = ctx
            self.update_for_context(ctx)

    def update_for_context(self, ctx: ActiveContext):
        exe = (ctx.exe or "").lower()
        title = ctx.title or ""
        self.lbl_app.setText(f"{exe}  —  {title[:48]}{'…' if len(title) > 48 else ''}")
        html = None
        for rule in self.cfg.get("rules", []):
            exes = [e.lower() for e in rule.get("match", {}).get("exe", [])]
            title_rx = rule.get("match", {}).get("title_regex")
            if exes and exe not in exes:
                continue
            if title_rx:
                try:
                    if not re.match(title_rx, title, flags=re.IGNORECASE):
                        continue
                except re.error:
                    # Bad regex → ignore title constraint
                    pass
            html = rule.get("content_html")
            if html:
                break
        if not html:
            html = self.cfg.get("fallback_html", "<p>No content.</p>")
        self.apply_content(html)

    def apply_content(self, html: str):
        # minimal theming wrapper
        theme = (
            "<style>body{font-family:'%s'; font-size:%dpt; line-height:1.35}"
            "h1,h2{margin:0 0 6px 0} ul{margin-top:6px} code{background:#222;padding:1px 4px;border-radius:5px}"
            "</style>"
            % (
                self.cfg["ui"].get("font_family", "Segoe UI"),
                int(self.cfg["ui"].get("font_size_pt", 11)),
            )
        )
        self.view.setHtml(theme + "<body>" + (html or "") + "</body>")


def main():
    ensure_config()
    cfg = load_config()

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = Panel(cfg)
    # Start near top-right of primary screen
    geo = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    x = geo.right() - cfg["ui"].get("width_px", 460) - 20
    y = geo.top() + 60
    w.move(x, y)
    w.show()

    # If active window detection not available, notify in panel
    if not ACTIVE_WIN_SUPPORTED:
        w.apply_content(
            """
            <h2>Conte</h2>
            <p>Active window detection is unavailable. On Windows, install <code>pywin32</code> and <code>psutil</code>.</p>
            <pre>pip install pywin32 psutil</pre>
            """
        )

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
