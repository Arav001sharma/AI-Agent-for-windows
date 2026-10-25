"""
Themes module for Lil-Agents Windows.
Directly ports the 4 themes from lil-agents:
- Peach (Playful pastel pink/peach)
- Midnight (Teenage Engineering dark slate / bright orange)
- Cloud (Wii minimalist clean daylight)
- Moss (iPod / retro olive sage)
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class Theme:
    name: str
    popover_bg: str
    popover_border: str
    border_width: int
    corner_radius: int
    titlebar_bg: str
    title_text: str
    title_font: str
    separator: str
    text_primary: str
    text_dim: str
    accent: str
    error_color: str
    success_color: str
    input_bg: str
    input_radius: int
    bubble_bg: str
    bubble_border: str
    bubble_text: str
    bubble_complete_border: str
    bubble_complete_text: str

THEMES: Dict[str, Theme] = {
    "Peach": Theme(
        name="Peach",
        popover_bg="rgba(255, 248, 235, 0.97)",
        popover_border="rgba(242, 140, 166, 0.85)",
        border_width=2,
        corner_radius=20,
        titlebar_bg="rgba(250, 237, 224, 1.0)",
        title_text="#d95973",
        title_font="'Segoe UI', 'SF Pro Display', sans-serif",
        separator="rgba(242, 140, 166, 0.25)",
        text_primary="#332e38",
        text_dim="#807885",
        accent="#d95973",
        error_color="#e64d33",
        success_color="#4db880",
        input_bg="#fffbf5",
        input_radius=12,
        bubble_bg="rgba(255, 242, 230, 0.95)",
        bubble_border="rgba(242, 140, 166, 0.6)",
        bubble_text="#8c8085",
        bubble_complete_border="rgba(77, 191, 128, 0.7)",
        bubble_complete_text="#339966",
    ),
    "Midnight": Theme(
        name="Midnight",
        popover_bg="rgba(18, 18, 18, 0.96)",
        popover_border="rgba(255, 102, 0, 0.75)",
        border_width=2,
        corner_radius=12,
        titlebar_bg="rgba(26, 26, 26, 1.0)",
        title_text="#ff6600",
        title_font="'Consolas', 'Cascadia Code', 'SF Mono', monospace",
        separator="rgba(255, 102, 0, 0.3)",
        text_primary="#f5f5f5",
        text_dim="#999999",
        accent="#ff6600",
        error_color="#ff4d33",
        success_color="#66a666",
        input_bg="#1f1f1f",
        input_radius=6,
        bubble_bg="rgba(26, 26, 26, 0.92)",
        bubble_border="rgba(255, 102, 0, 0.6)",
        bubble_text="#b3b3b3",
        bubble_complete_border="rgba(77, 204, 77, 0.7)",
        bubble_complete_text="#4dcc4d",
    ),
    "Cloud": Theme(
        name="Cloud",
        popover_bg="rgba(240, 242, 245, 0.98)",
        popover_border="rgba(199, 204, 214, 0.8)",
        border_width=1,
        corner_radius=16,
        titlebar_bg="rgba(224, 230, 237, 1.0)",
        title_text="#4d4d59",
        title_font="'Segoe UI', sans-serif",
        separator="rgba(204, 209, 217, 0.5)",
        text_primary="#262633",
        text_dim="#80808c",
        accent="#0078d4",
        error_color="#d93326",
        success_color="#33a64d",
        input_bg="#ffffff",
        input_radius=8,
        bubble_bg="rgba(240, 242, 247, 0.95)",
        bubble_border="rgba(0, 120, 212, 0.4)",
        bubble_text="#737885",
        bubble_complete_border="rgba(51, 179, 77, 0.6)",
        bubble_complete_text="#268c33",
    ),
    "Moss": Theme(
        name="Moss",
        popover_bg="rgba(209, 214, 199, 0.98)",
        popover_border="rgba(140, 148, 128, 0.8)",
        border_width=2,
        corner_radius=10,
        titlebar_bg="rgba(184, 191, 173, 1.0)",
        title_text="#262b1f",
        title_font="'Courier New', 'Consolas', monospace",
        separator="rgba(140, 148, 128, 0.5)",
        text_primary="#1a1f14",
        text_dim="#59614d",
        accent="#333826",
        error_color="#99261a",
        success_color="#266626",
        input_bg="#e0e6d6",
        input_radius=4,
        bubble_bg="rgba(209, 214, 199, 0.95)",
        bubble_border="rgba(140, 148, 128, 0.7)",
        bubble_text="#666b61",
        bubble_complete_border="rgba(51, 128, 51, 0.7)",
        bubble_complete_text="#266626",
    ),
}

def get_theme(name: str = "Peach") -> Theme:
    return THEMES.get(name, THEMES["Peach"])
