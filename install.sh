#!/bin/bash
# Installation script for Mancom Timer & Notes App

echo ""
echo "========================================"
echo "Mancom Timer and Notes App - Installation"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    echo ""
    echo "macOS: brew install python3"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python found"
python3 --version
echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo ""
echo "Installing PyQt5..."
python3 -m pip install PyQt5==5.15.9
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install PyQt5"
    echo "Please check your internet connection and try again."
    echo ""
    exit 1
fi

echo "[OK] PyQt5 installed successfully"

echo ""
echo "Installing additional dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
