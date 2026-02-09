#!/bin/bash
# Installation script for Mancom Timer & Notes App

echo "Installing Mancom Timer & Notes App..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation complete!"
echo ""
echo "To run the application:"
echo "  python main.py"
