# Lil-Agents for Windows 🤖🐾

[![Download](https://img.shields.io/badge/Download-Lil--Agents%20Windows%20(ZIP)-0078D4?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/Arav001sharma/AI-Agent-for-windows/releases/latest/download/lil-agents-windows.zip)
[![Latest Release](https://img.shields.io/github/v/release/Arav001sharma/AI-Agent-for-windows?style=for-the-badge&color=28a745)](https://github.com/Arav001sharma/AI-Agent-for-windows/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A complete Windows port of [ryanstephen/lil-agents](https://github.com/ryanstephen/lil-agents).

Tiny, animated AI companions (**Bruce and Jazz**) that walk and live right on top of your **Windows 11 Taskbar**, featuring an interactive popover AI terminal, floating thought bubbles, audio feedback, and multiple visual themes!

---

## 📥 Direct Download (No Git Required)

You can download the ready-to-run package directly:

👉 [**⬇️ Download Latest Version (lil-agents-windows.zip)**](https://github.com/Arav001sharma/AI-Agent-for-windows/releases/latest/download/lil-agents-windows.zip)

Or visit all releases: [**GitHub Releases**](https://github.com/Arav001sharma/AI-Agent-for-windows/releases)

### Setup in 3 Simple Steps:
1. **Download & Unzip:** Click the download link above and extract `lil-agents-windows.zip`.
2. **Install:** Double-click `install.bat` (installs Python dependencies).
3. **Launch:** Double-click `run.bat` to have Bruce or Jazz appear on your taskbar!

*(Note: Requires Python 3.10+ installed from [python.org](https://www.python.org/downloads/) with "Add to PATH" checked).*

---

## 💻 Clone via Git (Developers)

```cmd
git clone https://github.com/Arav001sharma/AI-Agent-for-windows.git
cd AI-Agent-for-windows
install.bat
run.bat
```

---

## ✨ Features

- **🐾 Taskbar Companion Overlay:**
  - Auto-snaps to the Windows Taskbar (respects taskbar height and screen boundaries).
  - Smooth 12-FPS walking physics with boundary bouncing and character flipping.
  - Interactive: Click to open terminal, drag anywhere to reposition.
- **💬 Themed Popover AI Terminal:**
  - Anchors directly above Bruce or Jazz.
  - Multi-turn conversation history with live streaming responses.
  - Sound effects (chimes) on completion using original audio assets.
- **🎨 4 Curated Themes (from original app):**
  - **Peach** (Playful pastel pink/peach)
  - **Midnight** (Teenage Engineering dark slate / bright orange)
  - **Cloud** (Wii clean minimal daylight)
  - **Moss** (iPod / retro olive sage)
- **🧠 Multi-Provider AI Support:**
  - **Google Gemini** (Gemini 2.0 Flash / 1.5 Flash streaming via REST)
  - **Local Ollama** (Run local models on your CPU/RAM with zero GPU requirements, e.g., `llama3.2`, `qwen2.5:3b`)
  - **Claude Code CLI** (`claude -p`)
  - **OpenAI** (GPT-4o / GPT-4o-mini)
  - **Windows PowerShell / Terminal** (Execute real commands directly from your desktop pet)
- **⚡ Super Lightweight:**
  - Built with Python & PyQt6.
  - Zero heavy Chromium/Electron overhead (~45 MB RAM usage).
  - High DPI scaling supported for Windows 11.

---

## 🎮 How to Control

- **Open Terminal:** Left-click on Bruce or Jazz.
- **Drag & Move:** Click and hold to drag the companion to any spot on your screen.
- **Right-Click Context Menu:**
  - **Companion Character:** Switch between **Bruce** and **Jazz**.
  - **Character Size:** Switch between **Small**, **Medium**, or **Large**.
  - **Visual Theme:** Switch between **Peach**, **Midnight**, **Cloud**, or **Moss**.
  - **AI Assistant:** Switch between **Google Gemini**, **Local Ollama**, **Claude Code CLI**, **OpenAI**, or **PowerShell**.
  - **Walk along Taskbar:** Toggle movement on/off.
  - **Snap to Taskbar:** Re-align immediately to the bottom edge above the taskbar.

---

## 🧠 Setting Up AI Providers

### Option A: Local AI via Ollama (Free & Private on your Ryzen 7 7735HS)
1. Download Ollama for Windows from [ollama.ai](https://ollama.ai).
2. Open Command Prompt and run:
   ```cmd
   ollama run llama3.2
   ```
3. In Lil-Agents, right-click the character -> **AI Assistant** -> **Local Ollama**. Done!

### Option B: Google Gemini API (Cloud)
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. In Command Prompt or System Environment Variables:
   ```cmd
   setx GEMINI_API_KEY "your_api_key_here"
   ```

### Option C: Claude Code CLI
1. Install Claude CLI via Node.js:
   ```cmd
   npm install -g @anthropic-ai/claude-code
   ```
2. Run `claude login`.
3. In Lil-Agents, choose **Claude Code CLI**.

---

## 📁 Repository Structure

```
AI Agent for windows/
├── main.py                     # Application entry point
├── run.bat                     # 1-Click Windows launch script
├── install.bat                 # 1-Click Windows dependency installer
├── requirements.txt            # Minimal Python dependencies (PyQt6, requests)
├── .gitignore                  # Git ignore rules for Python & Windows
├── README.md                   # Setup guide and documentation
│
├── src/                        # Modular Windows source code
│   └── lil_agents/
│       ├── __init__.py         # Package initialization
│       ├── companion.py        # Taskbar walking overlay & physics
│       ├── terminal.py         # Themed popover chat & terminal window
│       ├── ai_engine.py        # Multi-provider AI streaming backend
│       ├── audio_player.py     # Windows notification chimes & audio
│       └── themes.py           # Peach, Midnight, Cloud, Moss palettes
│
├── assets/                     # Extracted transparent media
│   ├── characters/
│   │   ├── bruce/              # 120 frames with alpha transparency
│   │   └── jazz/               # 120 frames with alpha transparency
│   └── sounds/                 # Original completion pings
│
└── original_macos_source/      # Original Swift/Xcode macOS repo for reference
    ├── LilAgents/              # Original Swift source files & assets
    ├── Tests/                  # Original unit tests
    ├── lil-agents.xcodeproj/   # Xcode project configuration
    └── CLAUDE.md               # Original project notes
```
