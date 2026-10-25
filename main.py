"""
Main Entry Point for Lil-Agents Windows.
Tiny AI companions (Bruce & Jazz) that walk and live on your Windows Taskbar.
"""

import sys
import os
from pathlib import Path

# Add project root and src directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

try:
    from lil_agents.companion import CompanionWidget
    from lil_agents.terminal import PopoverTerminal
    from lil_agents.audio_player import SoundManager
except ImportError:
    try:
        from src.lil_agents.companion import CompanionWidget
        from src.lil_agents.terminal import PopoverTerminal
        from src.lil_agents.audio_player import SoundManager
    except ImportError:
        from companion import CompanionWidget
        from terminal import PopoverTerminal
        from audio_player import SoundManager

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Lil-Agents Windows")
    app.setQuitOnLastWindowClosed(False)

    sound_mgr = SoundManager()

    companion = CompanionWidget(character_name="bruce", theme_name="Peach", provider="gemini")
    terminal = PopoverTerminal(sound_mgr, character_name="bruce", theme_name="Peach", provider="gemini")
    terminal.companion = companion

    def toggle_terminal():
        if terminal.isVisible():
            terminal.hide()
        else:
            terminal.anchor_above(companion.geometry())
            terminal.show()
            terminal.activateWindow()
            terminal.input_field.setFocus()

    companion.open_terminal_requested.connect(toggle_terminal)

    def on_theme_change(theme_name):
        terminal.apply_theme(theme_name)

    companion.theme_changed.connect(on_theme_change)

    def on_provider_change(provider):
        terminal.set_provider(provider)

    companion.provider_changed.connect(on_provider_change)

    # System Tray
    tray_icon = QSystemTrayIcon(app)
    tray_candidates = [
        PROJECT_ROOT / "assets" / "characters" / "bruce" / "frame_000.png",
        PROJECT_ROOT / "assets" / "menuicon.png"
    ]
    for icon_path in tray_candidates:
        if icon_path.exists():
            tray_icon.setIcon(QIcon(str(icon_path)))
            break

    tray_icon.setToolTip("Lil-Agents Windows")

    tray_menu = QMenu()
    toggle_term_action = tray_menu.addAction("Open Terminal")
    toggle_term_action.triggered.connect(toggle_terminal)

    snap_action = tray_menu.addAction("Snap Character to Taskbar")
    snap_action.triggered.connect(companion.snap_to_taskbar)

    tray_menu.addSeparator()
    quit_action = tray_menu.addAction("Quit Lil-Agents")
    quit_action.triggered.connect(app.quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(lambda reason: toggle_terminal() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)
    tray_icon.show()

    companion.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
