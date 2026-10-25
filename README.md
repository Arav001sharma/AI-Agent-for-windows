# Lil-Agents for Windows 🤖🐾

A complete Windows port of [ryanstephen/lil-agents](https://github.com/ryanstephen/lil-agents).

Tiny, animated AI companions (**Bruce and Jazz**) that walk and live right on top of your **Windows 11 Taskbar**, featuring an interactive popover AI terminal, floating thought bubbles, audio feedback, and multiple visual themes!

---

## 📁 Clean Project Structure

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
├── dist/
│   └── lil-agents-windows.zip  # Pre-packaged zip archive
│
└── original_macos_source/      # Original Swift/Xcode macOS repo for reference
    ├── LilAgents/              # Original Swift source files & assets
    ├── Tests/                  # Original unit tests
    ├── lil-agents.xcodeproj/   # Xcode project configuration
    └── CLAUDE.md               # Original project notes
```

---

## 🚀 Quick Start on Windows

### 1. Prerequisites
- **Windows 10 / Windows 11** (64-bit)
- **Python 3.10+** (download from [python.org](https://www.python.org/downloads/) — make sure to check **"Add python.exe to PATH"** during install).

### 2. Install Dependencies
Double-click `install.bat` or run:
```cmd
pip install -r requirements.txt
```

### 3. Launch the Application
Double-click `run.bat` or run:
```cmd
python main.py
```

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
