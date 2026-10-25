"""
Lil-Agents Windows Package
Tiny AI companions that walk on your Windows Taskbar.
"""

from .themes import get_theme, Theme, THEMES
from .audio_player import SoundManager
from .ai_engine import AgentWorker
from .companion import CompanionWidget, ThoughtBubble
from .terminal import PopoverTerminal

__all__ = [
    "get_theme",
    "Theme",
    "THEMES",
    "SoundManager",
    "AgentWorker",
    "CompanionWidget",
    "ThoughtBubble",
    "PopoverTerminal",
]
