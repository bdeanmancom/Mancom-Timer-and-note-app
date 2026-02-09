"""
Build script to create standalone Windows executable
Run: python build.py
"""

import subprocess
import sys
import os

def build_executable():
    """Build standalone Windows executable"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("Building executable...")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "MancomTimer",
        "--icon=icon.ico",  # Optional: add icon if available
        "--add-data", ".",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build successful!")
        print("Executable location: dist/MancomTimer.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
