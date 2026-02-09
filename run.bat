@echo off
REM Mancom Timer & Notes App Launcher

echo Launching Mancom Timer ^& Notes App...
python main.py

if errorlevel 1 (
    echo.
    echo Error: Could not start the application.
    echo Please make sure Python is installed and dependencies are installed.
    echo Run: install.bat
    pause
)
