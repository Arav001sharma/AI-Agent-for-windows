"""
Themed Popover Terminal Window for Lil-Agents Windows.
Anchors directly above the character with streaming markdown support,
quick provider switching, and theme reactive styling.
"""

from typing import List, Dict, Any, Optional
from PyQt6.QtCore import Qt, QPoint, QRect, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QAction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser,
    QLineEdit, QPushButton, QFrame,
    QApplication, QMenu, QGraphicsDropShadowEffect
)

try:
    from .themes import get_theme, Theme
    from .ai_engine import AgentWorker
    from .audio_player import SoundManager
except ImportError:
    from themes import get_theme, Theme
    from ai_engine import AgentWorker
    from audio_player import SoundManager

class PopoverTerminal(QWidget):
    message_sent = pyqtSignal(str)

    def __init__(self, sound_manager: SoundManager, character_name="bruce", theme_name="Peach", provider="gemini"):
        super().__init__()
        self.sound_manager = sound_manager
        self.character_name = character_name
        self.theme_name = theme_name
        self.theme: Theme = get_theme(theme_name)
        self.provider = provider

        self.history: List[Dict[str, str]] = []
        self.current_worker: Optional[AgentWorker] = None
        self.current_thread: Optional[QThread] = None
        self.config: Dict[str, Any] = {
            "gemini_model": "gemini-2.0-flash",
            "ollama_host": "http://localhost:11434",
            "ollama_model": "llama3.2",
            "openai_model": "gpt-4o-mini",
        }

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(460, 520)

        self._init_ui()
        self.apply_theme()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)

        self.card = QFrame()
        self.card.setObjectName("cardFrame")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 70))
        shadow.setOffset(0, 4)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(16, 12, 16, 14)
        card_layout.setSpacing(10)

        # Header Bar
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusDot")

        self.title_label = QLabel(self._format_title())
        self.title_label.setObjectName("titleLabel")

        header_layout.addWidget(self.status_dot)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        self.model_btn = QPushButton(self._get_provider_badge())
        self.model_btn.setObjectName("modelBtn")
        self.model_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.model_btn.clicked.connect(self._show_provider_menu)
        header_layout.addWidget(self.model_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(self.clear_btn)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.hide)
        header_layout.addWidget(self.close_btn)

        card_layout.addLayout(header_layout)

        self.sep = QFrame()
        self.sep.setFrameShape(QFrame.Shape.HLine)
        self.sep.setFrameShadow(QFrame.Shadow.Plain)
        card_layout.addWidget(self.sep)

        # Chat stream viewer
        self.text_browser = QTextBrowser()
        self.text_browser.setObjectName("textBrowser")
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setPlaceholderText(
            f"✨ Hello! I am {self.character_name.capitalize()}.\n"
            f"Ask me anything, execute commands, or chat with {self.provider.upper()}."
        )
        card_layout.addWidget(self.text_browser, stretch=1)

        # Input Row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("inputField")
        self.input_field.setPlaceholderText("Message your lil-agent...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field, stretch=1)

        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("sendBtn")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        card_layout.addLayout(input_layout)
        main_layout.addWidget(self.card)

    def _format_title(self) -> str:
        return f"{self.character_name} ~ {self.provider}"

    def _get_provider_badge(self) -> str:
        mapping = {
            "gemini": "Gemini 2.0",
            "ollama": "Ollama Local",
            "claude": "Claude CLI",
            "openai": "GPT-4o",
            "powershell": "PowerShell"
        }
        return mapping.get(self.provider, self.provider.title())

    def apply_theme(self, theme_name: Optional[str] = None):
        if theme_name:
            self.theme_name = theme_name
        self.theme = get_theme(self.theme_name)

        self.card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {self.theme.popover_bg};
                border: {self.theme.border_width}px solid {self.theme.popover_border};
                border-radius: {self.theme.corner_radius}px;
            }}
            QLabel#titleLabel {{
                color: {self.theme.title_text};
                font-family: {self.theme.title_font};
                font-size: 13px;
                font-weight: bold;
            }}
            QLabel#statusDot {{
                color: {self.theme.success_color};
                font-size: 10px;
            }}
            QFrame {{
                border: none;
                background-color: {self.theme.separator};
                max-height: 1px;
            }}
            QTextBrowser#textBrowser {{
                background-color: transparent;
                color: {self.theme.text_primary};
                font-family: 'Consolas', 'Segoe UI', monospace;
                font-size: 12px;
                border: none;
                selection-background-color: {self.theme.accent};
            }}
            QLineEdit#inputField {{
                background-color: {self.theme.input_bg};
                color: {self.theme.text_primary};
                border: 1px solid {self.theme.separator};
                border-radius: {self.theme.input_radius}px;
                padding: 8px 12px;
                font-size: 12px;
            }}
            QLineEdit#inputField:focus {{
                border: 1.5px solid {self.theme.accent};
            }}
            QPushButton#sendBtn {{
                background-color: {self.theme.accent};
                color: white;
                border: none;
                border-radius: {self.theme.input_radius}px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton#sendBtn:hover {{
                opacity: 0.9;
            }}
            QPushButton#modelBtn, QPushButton#clearBtn {{
                background-color: {self.theme.input_bg};
                color: {self.theme.text_dim};
                border: 1px solid {self.theme.separator};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 10px;
            }}
            QPushButton#closeBtn {{
                background: transparent;
                color: {self.theme.text_dim};
                border: none;
                font-size: 14px;
                font-weight: bold;
                padding: 2px 6px;
            }}
            QPushButton#closeBtn:hover {{
                color: {self.theme.error_color};
            }}
        """)

        self.title_label.setText(self._format_title())
        self.model_btn.setText(self._get_provider_badge())

    def _show_provider_menu(self):
        menu = QMenu(self)
        providers = [
            ("gemini", "Google Gemini (Cloud)"),
            ("ollama", "Local Ollama (Ryzen 7 7735HS)"),
            ("claude", "Claude Code CLI"),
            ("openai", "OpenAI (GPT-4o)"),
            ("powershell", "Windows PowerShell"),
        ]
        for p_id, p_label in providers:
            action = menu.addAction(p_label)
            action.setCheckable(True)
            action.setChecked(self.provider == p_id)
            action.triggered.connect(lambda checked, pid=p_id: self.set_provider(pid))
        menu.exec(self.model_btn.mapToGlobal(QPoint(0, self.model_btn.height())))

    def set_provider(self, provider: str):
        self.provider = provider
        self.title_label.setText(self._format_title())
        self.model_btn.setText(self._get_provider_badge())

    def set_character(self, character_name: str):
        self.character_name = character_name
        self.title_label.setText(self._format_title())

    def clear_chat(self):
        self.history.clear()
        self.text_browser.clear()

    def anchor_above(self, target_rect: QRect):
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry() if screen else QRect(0, 0, 1920, 1080)

        x = target_rect.center().x() - self.width() // 2
        x = max(avail.left() + 15, min(x, avail.right() - self.width() - 15))

        y = target_rect.top() - self.height() - 10
        if y < avail.top() + 15:
            y = max(avail.top() + 15, avail.bottom() - self.height() - 60)

        self.move(x, y)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.input_field.clear()
        self._append_message("user", text)
        self.history.append({"role": "user", "text": text})

        self.set_busy(True)
        self.status_dot.setText("⏳")

        self.current_thread = QThread()
        self.current_worker = AgentWorker(self.provider, text, self.history, self.config)
        self.current_worker.moveToThread(self.current_thread)

        self.current_thread.started.connect(self.current_worker.run)
        self.current_worker.chunk_received.connect(self._on_chunk)
        self.current_worker.error_occurred.connect(self._on_error)
        self.current_worker.finished.connect(self._on_finished)
        self.current_worker.finished.connect(self.current_thread.quit)
        self.current_worker.finished.connect(self.current_worker.deleteLater)
        self.current_thread.finished.connect(self.current_thread.deleteLater)

        self.response_text = ""
        self._start_assistant_message()
        self.current_thread.start()

    def set_busy(self, busy: bool):
        self.send_btn.setEnabled(not busy)
        self.input_field.setEnabled(not busy)
        if hasattr(self, 'companion') and self.companion:
            self.companion.set_agent_busy(busy)

    def _append_message(self, role: str, text: str):
        color = self.theme.accent if role == "user" else self.theme.text_primary
        prefix = "<b>You:</b>" if role == "user" else f"<b>{self.character_name.capitalize()}:</b>"
        html = f"""
        <div style="margin: 6px 0;">
            <span style="color: {color};">{prefix}</span>
            <div style="margin-left: 8px; color: {self.theme.text_primary};">{text}</div>
        </div>
        """
        self.text_browser.append(html)

    def _start_assistant_message(self):
        prefix = f"<b style='color: {self.theme.title_text};'>{self.character_name.capitalize()}:</b> "
        self.text_browser.append(prefix)

    def _on_chunk(self, chunk: str):
        self.response_text += chunk
        cursor = self.text_browser.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(chunk)
        self.text_browser.setTextCursor(cursor)
        self.text_browser.ensureCursorVisible()

    def _on_error(self, err_msg: str):
        self._append_message("system", f"<span style='color: {self.theme.error_color};'>⚠ {err_msg}</span>")

    def _on_finished(self):
        self.set_busy(False)
        self.status_dot.setText("●")
        if self.response_text:
            self.history.append({"role": "assistant", "text": self.response_text})
        self.sound_manager.play_ping()
        self.input_field.setFocus()
