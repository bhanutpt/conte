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
import ctypes

# import time
# import threading
import re
import webbrowser
from dataclasses import dataclass

from context.config import get_default_config

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

# --- Windows active-window inspection ---
IS_WINDOWS = os.name == "nt"
try:
    USER32 = ctypes.windll.user32 if IS_WINDOWS else None
except Exception:
    USER32 = None

SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
SWP_NOSENDCHANGING = 0x0400
SWP_SHOWWINDOW = 0x0040
HWND_BOTTOM = 1


ACTIVE_WIN_SUPPORTED = True
try:
    import win32gui
    import win32process
    import win32con
    import psutil
except Exception:
    ACTIVE_WIN_SUPPORTED = False
    win32gui = win32process = win32con = psutil = None

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
    ui = cfg["ui"]
    ui.setdefault("font_family", "Inter, Segoe UI, Arial")
    ui.setdefault("font_size_pt", 12)
    ui.setdefault("opacity", 0.95)
    ui.setdefault("base_width_px", ui.get("width_px", 945))
    ui.setdefault("base_height_px", ui.get("height_px", 532))
    ui.setdefault("width_px", 945)
    ui.setdefault("height_px", 532)
    ui.setdefault("panel_scale", 1.0)
    ui.setdefault("lock_aspect_ratio", True)
    ratio = ui.get("aspect_ratio")
    if (
        not isinstance(ratio, (list, tuple))
        or len(ratio) != 2
        or any(not isinstance(x, (int, float)) or x <= 0 for x in ratio)
    ):
        ratio = [16, 9]
    ratio_w = int(round(float(ratio[0])))
    ratio_h = int(round(float(ratio[1])))
    if ratio_w <= 0 or ratio_h <= 0:
        ratio_w, ratio_h = 16, 9
    ui["aspect_ratio"] = [ratio_w, ratio_h]
    if ui["lock_aspect_ratio"]:
        scale = float(ui.get("panel_scale", 1.0) or 1.0)
        scale = max(0.2, min(scale, 4.0))
        base_width = max(1, int(ui.get("base_width_px", 945)))
        width = int(round(base_width * scale))
        ui["width_px"] = width
        target_height = max(1, int(round(width * ratio_h / ratio_w)))
        ui["height_px"] = target_height
    else:
        ui["width_px"] = max(1, int(ui.get("width_px", 945)))
        ui["height_px"] = max(1, int(ui.get("height_px", 532)))
    ui.setdefault("always_on_top", False)
    had_back_key = "always_on_back" in ui
    ui.setdefault("always_on_back", True)
    if not had_back_key:
        cfg["ui"]["always_on_top"] = False
    cfg["ui"]["always_on_top"] = bool(cfg["ui"].get("always_on_top", False))
    cfg["ui"].setdefault("borderless", True)
    cfg["ui"].setdefault("start_maximized", True)
    if cfg["ui"].get("always_on_back", True):
        cfg["ui"]["always_on_top"] = False
    elif cfg["ui"].get("always_on_top"):
        cfg["ui"]["always_on_back"] = False
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
        self.start_maximized = bool(self.cfg["ui"].get("start_maximized", False))
        self.setWindowTitle("Conte")
        ui_flags = self.windowFlags()
        always_on_top = bool(self.cfg["ui"].get("always_on_top", False))
        always_on_back = (
            bool(self.cfg["ui"].get("always_on_back", False)) and not always_on_top
        )
        if always_on_top:
            ui_flags |= Qt.WindowStaysOnTopHint
            ui_flags &= ~Qt.WindowStaysOnBottomHint
        elif always_on_back:
            ui_flags |= Qt.WindowStaysOnBottomHint
            ui_flags &= ~Qt.WindowStaysOnTopHint
        else:
            ui_flags &= ~Qt.WindowStaysOnTopHint
            ui_flags &= ~Qt.WindowStaysOnBottomHint
        if self.cfg["ui"].get("borderless", True):
            ui_flags |= Qt.FramelessWindowHint
        else:
            ui_flags &= ~Qt.FramelessWindowHint
        self.setWindowFlags(ui_flags)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAttribute(
            Qt.WA_ShowWithoutActivating,
            bool(self.cfg["ui"].get("always_on_back", False)),
        )
        self.setWindowOpacity(float(self.cfg["ui"].get("opacity", 0.95)))

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

        self._backdrop_timer = None
        if self.cfg["ui"].get("always_on_back", False):
            self._backdrop_timer = QtCore.QTimer(self)
            self._backdrop_timer.setInterval(2500)
            self._backdrop_timer.timeout.connect(self.enforce_backdrop)
            self._backdrop_timer.start()
            QtCore.QTimer.singleShot(250, self.enforce_backdrop)

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

    def enforce_backdrop(self):
        """Push the window behind other apps when always_on_back is enabled."""
        if not self.cfg["ui"].get("always_on_back", False):
            return
        hwnd = None
        wid = self.winId()
        try:
            hwnd = int(wid) if wid is not None else None
        except TypeError:
            try:
                hwnd = wid.__int__() if wid is not None else None
            except Exception:
                hwnd = None
        if USER32 and hwnd:
            try:
                USER32.SetWindowPos(
                    hwnd,
                    HWND_BOTTOM,
                    0,
                    0,
                    0,
                    0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_NOSENDCHANGING,
                )
                return
            except Exception:
                pass
        # Fallback when the Windows API is unavailable
        self.lower()

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
            return
        # re-apply UI tunables
        self.setWindowOpacity(float(self.cfg["ui"].get("opacity", 0.95)))
        self.start_maximized = bool(self.cfg["ui"].get("start_maximized", False))
        wants_backdrop = bool(self.cfg["ui"].get("always_on_back", False))
        if wants_backdrop and not self._backdrop_timer:
            self._backdrop_timer = QtCore.QTimer(self)
            self._backdrop_timer.setInterval(2500)
            self._backdrop_timer.timeout.connect(self.enforce_backdrop)
            self._backdrop_timer.start()
        elif not wants_backdrop and self._backdrop_timer:
            self._backdrop_timer.stop()
            self._backdrop_timer = None
        self.enforce_backdrop()

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
        # current: stops on first match
        # new: collect matches and pick the most specific
        candidates = []
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
                    pass
            # compute specificity score: prefer rules with title_regex other than '.*'
            score = 0
            if title_rx and title_rx != ".*":
                score += 10
                score += len(
                    title_rx
                )  # longer regex => more specific (simple heuristic)
            score += 1 if exes else 0
            candidates.append((score, rule))
        if candidates:
            # choose highest score
            candidates.sort(key=lambda x: x[0], reverse=True)
            html = candidates[0][1].get("content_html")
        else:
            html = None
        if not html:
            html = self.cfg.get("fallback_html", "<p>No content.</p>")
        self.apply_content(html)

    def apply_content(self, html: str):
        # minimal theming wrapper
        theme = (
            "<style>"
            "body{font-family:'%s';font-size:%dpt;line-height:1.35;margin:0;padding:18px;"
            "background-color:#0f111a;color:#f4f6ff;}"
            "h1,h2{margin:0 0 6px 0}"
            ".shortcut-grid{display:flex;flex-wrap:wrap;gap:20px;margin-top:12px}"
            ".shortcut-grid.two-col section{flex:1 1 300px}"
            ".shortcut-grid section{flex:1 1 240px;background:rgba(255,255,255,0.04);"
            "border-radius:12px;padding:14px 18px;box-shadow:0 6px 18px rgba(0,0,0,0.35)}"
            ".shortcut-grid h3{margin:0 0 10px 0;font-size:15px;text-transform:uppercase;"
            "letter-spacing:0.05em;color:#7dd3fc}"
            ".shortcut-table{width:100%%;border-collapse:collapse}"
            ".shortcut-table td{padding:4px 0;vertical-align:top}"
            ".shortcut-table td.shortcut{font-weight:600;color:#c4fba4;padding-right:12px;"
            "white-space:nowrap}"
            ".shortcut-note{margin-top:14px;font-size:12px;color:#b6bee3}"
            "a{color:#7dd3fc;text-decoration:none}a:hover{text-decoration:underline}"
            "code{background:#1f2233;padding:2px 5px;border-radius:4px}"
            "</style>"
            % (
                self.cfg["ui"].get("font_family", "Segoe UI"),
                int(self.cfg["ui"].get("font_size_pt", 12)),
            )
        )
        self.view.setHtml(theme + "<body>" + (html or "") + "</body>")


def main():
    ensure_config()
    cfg = load_config()

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = Panel(cfg)
    start_max = bool(cfg["ui"].get("start_maximized", False))
    if start_max:
        w.showMaximized()
        w.enforce_backdrop()
    else:
        width = int(cfg["ui"].get("width_px", 460))
        height = int(cfg["ui"].get("height_px", 320))
        w.resize(width, height)
        geo = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        x = geo.right() - width - 20
        y = geo.top() + 60
        w.move(x, y)
        w.show()
        w.enforce_backdrop()

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
