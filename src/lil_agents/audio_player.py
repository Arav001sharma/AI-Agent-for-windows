"""
Audio player for Lil-Agents Windows.
Plays completion pings (ping-aa through ping-hh) with robust fallbacks for Windows.
"""

import os
import random
import sys
import threading
from pathlib import Path

class SoundManager:
    def __init__(self, sounds_dir: str = None):
        self.sounds_dir = None
        if sounds_dir and Path(sounds_dir).exists():
            self.sounds_dir = Path(sounds_dir)
        else:
            base_dir = Path(__file__).resolve().parent
            candidates = [
                base_dir / "assets" / "sounds",
                base_dir.parent / "assets" / "sounds",
                base_dir.parent.parent / "assets" / "sounds",
            ]
            for c in candidates:
                if c.exists():
                    self.sounds_dir = c
                    break

        self.sound_files = []
        if self.sounds_dir and self.sounds_dir.exists():
            self.sound_files = list(self.sounds_dir.glob("*.mp3")) + list(self.sounds_dir.glob("*.wav"))

    def play_ping(self):
        """Plays a random completion ping asynchronously."""
        if not self.sound_files:
            return

        sound_path = random.choice(self.sound_files)
        threading.Thread(target=self._play_file, args=(str(sound_path),), daemon=True).start()

    def _play_file(self, file_path: str):
        try:
            if sys.platform == "win32":
                import ctypes
                alias = f"ping_{random.randint(100, 999)}"
                mci = ctypes.windll.winmm.mciSendStringW
                mci(f'open "{file_path}" type mpegvideo alias {alias}', None, 0, 0)
                mci(f'play {alias} wait', None, 0, 0)
                mci(f'close {alias}', None, 0, 0)
                return
        except Exception:
            pass

        try:
            if sys.platform == "darwin":
                import subprocess
                subprocess.run(["afplay", file_path], check=False)
        except Exception:
            pass
