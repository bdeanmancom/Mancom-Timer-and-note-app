@echo off
REM Installation script for Mancom Timer & Notes App on Windows

echo.
echo ========================================
echo Mancom Timer and Notes App - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Upgrade pip first
echo Installing pip upgrade...
python -m pip install --upgrade pip

echo.
echo Installing PyQt5...
pip install PyQt5==5.15.9
if errorlevel 1 (
    echo [ERROR] Failed to install PyQt5
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo [OK] PyQt5 installed successfully

echo.
echo Installing additional dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To run the application:
echo   python main.py
echo.
echo Or double-click: run.bat
echo.
pause
