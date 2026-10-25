"""
AI Engine and session management for Lil-Agents Windows.
Supports:
1. Claude Code CLI (claude)
2. Google Gemini API (gemini-2.0-flash / gemini-1.5-flash)
3. Ollama (local models: llama3.2, qwen2.5, mistral, etc.)
4. OpenAI-compatible API
5. Local Windows Shell / PowerShell terminal execution
"""

import os
import sys
import json
import subprocess
import threading
from typing import Optional, Callable, Dict, Any, List
import requests
from PyQt6.QtCore import QObject, pyqtSignal

class AgentWorker(QObject):
    chunk_received = pyqtSignal(str)
    thought_updated = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, provider: str, prompt: str, history: List[Dict[str, str]], config: Dict[str, Any]):
        super().__init__()
        self.provider = provider
        self.prompt = prompt
        self.history = history
        self.config = config
        self.is_cancelled = False

    def run(self):
        try:
            self.thought_updated.emit("Thinking...")
            if self.provider == "claude":
                self._run_claude()
            elif self.provider == "gemini":
                self._run_gemini()
            elif self.provider == "ollama":
                self._run_ollama()
            elif self.provider == "openai":
                self._run_openai()
            elif self.provider == "powershell":
                self._run_powershell()
            else:
                self._run_gemini()
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()

    def _run_claude(self):
        """Runs Claude Code CLI if installed on Windows."""
        binary = self.config.get("claude_path", "claude")
        try:
            cmd = [binary, "-p", self.prompt]
            self.thought_updated.emit("Claude running...")
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                bufsize=1
            )
            for line in proc.stdout:
                if self.is_cancelled:
                    proc.kill()
                    break
                self.chunk_received.emit(line)
            proc.wait()
            if proc.returncode != 0:
                err = proc.stderr.read()
                if err:
                    self.chunk_received.emit(f"\n[Claude Notice]: {err}")
        except FileNotFoundError:
            self.error_occurred.emit(
                "Claude CLI not found. Install it with 'npm install -g @anthropic-ai/claude-code' "
                "or switch provider to Gemini / Ollama."
            )

    def _run_gemini(self):
        """Streams response from Google Gemini API."""
        api_key = self.config.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            self.chunk_received.emit(
                "🔑 Gemini API key not set.\n\n"
                "Please set GEMINI_API_KEY in environment variables or enter it in Settings, "
                "or switch to local Ollama / PowerShell."
            )
            return

        model = self.config.get("gemini_model", "gemini-2.0-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={api_key}"

        contents = []
        for msg in self.history[-6:]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["text"]}]})
        contents.append({"role": "user", "parts": [{"text": self.prompt}]})

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": "You are a tiny, helpful desktop companion AI named Bruce/Jazz. Keep answers concise, clear, and formatted neatly."}]
            }
        }

        self.thought_updated.emit(f"Gemini ({model})...")
        response = requests.post(url, json=payload, stream=True, timeout=30)
        if response.status_code != 200:
            self.error_occurred.emit(f"Gemini API Error {response.status_code}: {response.text}")
            return

        for line in response.iter_lines(decode_unicode=True):
            if self.is_cancelled:
                break
            if line and line.startswith("data: "):
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        for part in parts:
                            text = part.get("text", "")
                            if text:
                                self.chunk_received.emit(text)
                except Exception:
                    pass

    def _run_ollama(self):
        """Streams response from local Ollama server on Ryzen 7 7735HS."""
        host = self.config.get("ollama_host", "http://localhost:11434")
        model = self.config.get("ollama_model", "llama3.2")

        url = f"{host}/api/chat"
        messages = []
        for msg in self.history[-6:]:
            messages.append({"role": msg["role"], "content": msg["text"]})
        messages.append({"role": "user", "content": self.prompt})

        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        self.thought_updated.emit(f"Ollama ({model})...")
        try:
            response = requests.post(url, json=payload, stream=True, timeout=10)
            if response.status_code != 200:
                self.error_occurred.emit(
                    f"Ollama Error ({response.status_code}). Ensure Ollama is running (`ollama serve`)."
                )
                return

            for line in response.iter_lines(decode_unicode=True):
                if self.is_cancelled:
                    break
                if line:
                    try:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            self.chunk_received.emit(content)
                        if data.get("done", False):
                            break
                    except Exception:
                        pass
        except requests.exceptions.ConnectionError:
            self.error_occurred.emit(
                f"Cannot connect to Ollama at {host}.\n"
                "To use local AI models on your Windows laptop:\n"
                "1. Download Ollama from https://ollama.ai\n"
                "2. Run `ollama run llama3.2` or `ollama run qwen2.5:3b` in Command Prompt."
            )

    def _run_openai(self):
        """OpenAI-compatible chat completion."""
        api_key = self.config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
        base_url = self.config.get("openai_base_url", "https://api.openai.com/v1")
        model = self.config.get("openai_model", "gpt-4o-mini")

        if not api_key and "api.openai.com" in base_url:
            self.chunk_received.emit("🔑 OPENAI_API_KEY is not set.")
            return

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        messages = [{"role": m["role"], "content": m["text"]} for m in self.history[-6:]]
        messages.append({"role": "user", "content": self.prompt})

        payload = {"model": model, "messages": messages, "stream": True}
        self.thought_updated.emit(f"{model}...")

        response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, stream=True)
        for line in response.iter_lines(decode_unicode=True):
            if self.is_cancelled:
                break
            if line and line.startswith("data: "):
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data["choices"][0]["delta"].get("content", "")
                    if delta:
                        self.chunk_received.emit(delta)
                except Exception:
                    pass

    def _run_powershell(self):
        """Runs Windows PowerShell or CMD commands directly and streams output."""
        self.thought_updated.emit("Executing command...")
        try:
            cmd = ["powershell", "-NoProfile", "-Command", self.prompt]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                bufsize=1
            )
            for line in proc.stdout:
                if self.is_cancelled:
                    proc.kill()
                    break
                self.chunk_received.emit(line)
            proc.wait()
            err = proc.stderr.read()
            if err:
                self.chunk_received.emit(f"\n[STDERR]:\n{err}")
        except Exception as e:
            self.error_occurred.emit(f"Execution failed: {e}")
