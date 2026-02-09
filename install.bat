@echo off
REM Installation script for Mancom Timer & Notes App on Windows

echo Installing Mancom Timer and Notes App...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Install required packages
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python main.py
echo.
pause
