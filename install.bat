@echo off
title Install Lil-Agents Dependencies
cd /d "%~dp0"

echo ========================================================
echo Installing Lil-Agents Dependencies for Windows...
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================================
echo Installation Complete! Double-click run.bat to start.
echo ========================================================
pause
