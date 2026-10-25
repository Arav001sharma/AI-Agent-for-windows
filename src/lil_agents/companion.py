"""
Companion Widget for Lil-Agents Windows.
Displays animated character (Bruce or Jazz) that walks along the Windows Taskbar,
with floating thought bubble and drag/click interactions.
"""

import os
from pathlib import Path
from typing import List, Optional
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QPixmap, QTransform, QColor, QFont, QPen,
    QBrush, QCursor, QFontMetrics
)
from PyQt6.QtWidgets import QWidget, QMenu, QApplication

try:
    from .themes import get_theme, Theme
except ImportError:
    from themes import get_theme, Theme

class ThoughtBubble(QWidget):
    """Floating thought pill that appears above the companion while processing."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.text = "Thinking..."
        self.is_completed = False
        self.theme: Theme = get_theme("Peach")
        self.resize(160, 36)

    def set_status(self, text: str, is_completed: bool = False, theme: Theme = None):
        self.text = text
        self.is_completed = is_completed
        if theme:
            self.theme = theme
        self.adjust_size()
        self.update()

    def adjust_size(self):
        font = QFont("Segoe UI", 9, QFont.Weight.Bold if self.is_completed else QFont.Weight.Medium)
        fm = QFontMetrics(font)
        text_w = fm.horizontalAdvance(self.text)
        w = max(90, text_w + 30)
        h = 32
        self.resize(w, h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(2, 2, -2, -2)
        radius = 14

        if self.is_completed:
            bg_color = QColor(self.theme.bubble_bg)
            border_color = QColor(self.theme.bubble_complete_border)
            text_color = QColor(self.theme.bubble_complete_text)
        else:
            bg_color = QColor(self.theme.bubble_bg)
            border_color = QColor(self.theme.bubble_border)
            text_color = QColor(self.theme.bubble_text)

        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(border_color, 1.5))
        painter.drawRoundedRect(rect, radius, radius)

        font = QFont("Segoe UI", 9, QFont.Weight.Bold if self.is_completed else QFont.Weight.Medium)
        painter.setFont(font)
        painter.setPen(QPen(text_color))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)


class CompanionWidget(QWidget):
    open_terminal_requested = pyqtSignal()
    theme_changed = pyqtSignal(str)
    provider_changed = pyqtSignal(str)

    SIZES = {
        "Small": {"height": 130, "width": 73},
        "Medium": {"height": 175, "width": 98},
        "Large": {"height": 220, "width": 124},
    }

    def __init__(self, character_name: str = "bruce", theme_name: str = "Peach", provider: str = "gemini"):
        super().__init__()
        self.character_name = character_name
        self.current_theme_name = theme_name
        self.theme: Theme = get_theme(theme_name)
        self.provider = provider
        self.size_mode = "Medium"

        self.frames: List[QPixmap] = []
        self.current_frame_idx = 0
        self.facing_right = True
        self.is_walking_enabled = True
        self.is_busy = False

        # Dragging state
        self.drag_position = QPoint()
        self.is_dragging = False
        self.press_pos = QPoint()

        # Window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Thought bubble
        self.bubble = ThoughtBubble()

        # Load frames
        self.load_character_frames(self.character_name)

        # Snapping to Taskbar
        self.apply_size()
        self.snap_to_taskbar()

        # Animation timer (12 FPS = ~83 ms)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._on_animation_tick)
        self.anim_timer.start(83)

        # Bubble dismiss timer
        self.bubble_timer = QTimer(self)
        self.bubble_timer.setSingleShot(True)
        self.bubble_timer.timeout.connect(self.bubble.hide)

    def load_character_frames(self, character_name: str):
        self.character_name = character_name
        base_dir = Path(__file__).resolve().parent
        candidates = [
            base_dir / "assets" / "characters" / character_name,
            base_dir.parent / "assets" / "characters" / character_name,
            base_dir.parent.parent / "assets" / "characters" / character_name,
        ]
        frames_dir = candidates[0]
        for c in candidates:
            if c.exists():
                frames_dir = c
                break

        self.frames = []
        if frames_dir.exists():
            files = sorted(frames_dir.glob("frame_*.png"))
            for f in files:
                pix = QPixmap(str(f))
                if not pix.isNull():
                    self.frames.append(pix)

        self.current_frame_idx = 0
        self.update()

    def set_theme(self, theme_name: str):
        self.current_theme_name = theme_name
        self.theme = get_theme(theme_name)
        self.theme_changed.emit(theme_name)
        if self.bubble.isVisible():
            self.bubble.theme = self.theme
            self.bubble.update()

    def set_provider(self, provider: str):
        self.provider = provider
        self.provider_changed.emit(provider)

    def set_size_mode(self, mode: str):
        if mode in self.SIZES:
            self.size_mode = mode
            self.apply_size()
            self.snap_to_taskbar()

    def apply_size(self):
        dim = self.SIZES[self.size_mode]
        self.resize(dim["width"], dim["height"])

    def snap_to_taskbar(self):
        screen = QApplication.primaryScreen()
        if not screen:
            return
        avail = screen.availableGeometry()
        char_h = self.height()
        y = avail.bottom() - char_h + 8
        x = min(self.x(), avail.right() - self.width() - 20)
        x = max(avail.left() + 20, x)
        self.move(x, y)
        self._update_bubble_position()

    def set_agent_busy(self, busy: bool, message: str = "Thinking..."):
        self.is_busy = busy
        if busy:
            self.bubble_timer.stop()
            self.bubble.set_status(message, is_completed=False, theme=self.theme)
            self._update_bubble_position()
            self.bubble.show()
        else:
            self.bubble.set_status("Done ✓", is_completed=True, theme=self.theme)
            self._update_bubble_position()
            self.bubble_timer.start(2500)

    def _update_bubble_position(self):
        if self.bubble:
            bx = self.x() + (self.width() - self.bubble.width()) // 2
            by = self.y() - self.bubble.height() - 6
            self.bubble.move(bx, by)

    def _on_animation_tick(self):
        if not self.frames:
            return

        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)

        if self.is_walking_enabled and not self.is_dragging:
            if 36 <= self.current_frame_idx <= 99:
                screen = QApplication.primaryScreen()
                avail = screen.availableGeometry() if screen else QRect(0, 0, 1920, 1080)

                step = 2.2
                dx = step if self.facing_right else -step
                new_x = self.x() + int(dx)

                if new_x + self.width() >= avail.right() - 10:
                    self.facing_right = False
                    new_x = avail.right() - self.width() - 10
                elif new_x <= avail.left() + 10:
                    self.facing_right = True
                    new_x = avail.left() + 10

                self.move(new_x, self.y())
                self._update_bubble_position()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if not self.frames:
            painter.setBrush(QBrush(QColor(self.theme.accent)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(10, 10, self.width() - 20, self.height() - 20)
            return

        current_pixmap = self.frames[self.current_frame_idx]
        scaled = current_pixmap.scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        if not self.facing_right:
            transform = QTransform().scale(-1, 1)
            scaled = scaled.transformed(transform)

        draw_x = (self.width() - scaled.width()) // 2
        draw_y = self.height() - scaled.height()
        painter.drawPixmap(draw_x, draw_y, scaled)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.press_pos = event.globalPosition().toPoint()
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            self._update_bubble_position()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            dist = (event.globalPosition().toPoint() - self.press_pos).manhattanLength()
            if dist < 6:
                self.open_terminal_requested.emit()
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.open_terminal_requested.emit()

    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {self.theme.popover_bg};
                color: {self.theme.text_primary};
                border: 1px solid {self.theme.popover_border};
                border-radius: 8px;
                padding: 6px;
                font-family: 'Segoe UI', sans-serif;
            }}
            QMenu::item {{
                padding: 6px 20px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {self.theme.accent};
                color: white;
            }}
            QMenu::separator {{
                height: 1px;
                background: {self.theme.separator};
                margin: 4px 8px;
            }}
        """)

        char_menu = menu.addMenu("Companion Character")
        for char in ["bruce", "jazz"]:
            action = char_menu.addAction(char.capitalize())
            action.setCheckable(True)
            action.setChecked(self.character_name == char)
            action.triggered.connect(lambda checked, c=char: self.load_character_frames(c))

        size_menu = menu.addMenu("Character Size")
        for s in ["Small", "Medium", "Large"]:
            action = size_menu.addAction(s)
            action.setCheckable(True)
            action.setChecked(self.size_mode == s)
            action.triggered.connect(lambda checked, sm=s: self.set_size_mode(sm))

        theme_menu = menu.addMenu("Visual Theme")
        for t in ["Peach", "Midnight", "Cloud", "Moss"]:
            action = theme_menu.addAction(t)
            action.setCheckable(True)
            action.setChecked(self.current_theme_name == t)
            action.triggered.connect(lambda checked, tm=t: self.set_theme(tm))

        prov_menu = menu.addMenu("AI Assistant")
        providers = [
            ("gemini", "Google Gemini (Flash)"),
            ("ollama", "Local Ollama (Ryzen 7 7735HS)"),
            ("claude", "Claude Code CLI"),
            ("openai", "OpenAI (GPT-4o)"),
            ("powershell", "Windows PowerShell"),
        ]
        for p_id, p_label in providers:
            action = prov_menu.addAction(p_label)
            action.setCheckable(True)
            action.setChecked(self.provider == p_id)
            action.triggered.connect(lambda checked, pid=p_id: self.set_provider(pid))

        menu.addSeparator()

        walk_action = menu.addAction("Walk along Taskbar")
        walk_action.setCheckable(True)
        walk_action.setChecked(self.is_walking_enabled)
        walk_action.triggered.connect(lambda checked: setattr(self, 'is_walking_enabled', checked))

        snap_action = menu.addAction("Snap to Taskbar")
        snap_action.triggered.connect(self.snap_to_taskbar)

        term_action = menu.addAction("Open Terminal Popover")
        term_action.triggered.connect(self.open_terminal_requested.emit)

        menu.addSeparator()
        quit_action = menu.addAction("Exit Lil-Agents")
        quit_action.triggered.connect(QApplication.instance().quit)

        menu.exec(pos)
