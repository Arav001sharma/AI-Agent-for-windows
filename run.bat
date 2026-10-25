@echo off
title Lil-Agents for Windows
cd /d "%~dp0"

echo [Lil-Agents] Starting your desktop companion...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add python.exe to PATH" during installation.
    pause
    exit /b 1
)

python main.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [Lil-Agents] It looks like some dependencies might be missing.
    echo Running installer now...
    python -m pip install -r requirements.txt
    echo Relaunching...
    python main.py
)
pause
