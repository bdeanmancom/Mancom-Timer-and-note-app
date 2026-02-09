"""
Build script to create standalone Windows executable
Run: python build.py

First install build dependencies:
pip install -r requirements-dev.txt
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
        print("Installing PyInstaller and build dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])
    
    print("Building executable...")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "MancomTimer",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "--icon=NONE",
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
