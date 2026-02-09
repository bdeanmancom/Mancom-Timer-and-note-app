"""\nBuild script to create standalone Windows executable\nRun: python build.py\n\nThis bundles:
- main.py (app logic)
- icon.ico (window icon)
- logo.png/jpg or mancom.gif (branding logo)
- All dependencies
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def build_executable():
    """Build standalone Windows executable"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller and build dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])
    
    print("Cleaning previous build artifacts...")
    
    # Remove old build artifacts to avoid permission errors
    for path in ['dist', 'build', 'MancomTimer.spec']:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                print(f"  Removed: {path}")
            except Exception as e:
                print(f"  Warning: Could not remove {path}: {e}")
    
    print("Building executable...")
    
    # Find logo file
    logo_file = None
    for ext in ['mancominc.png', 'logo.png', 'logo.jpg', 'logo.jpeg', 'mancom.png', 'mancom.jpg', 'mancom.gif']:
        if Path(ext).exists():
            logo_file = ext
            break
    
    # Build command with data files
    # Use python -m PyInstaller for better cross-platform reliability
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "MancomTimer",
    ]
    
    # Add icon if available
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon=icon.ico"])
    else:
        cmd.append("--icon=NONE")
    
    # Add logo file if available
    if logo_file:
        cmd.extend(["--add-data", f"{logo_file}:."])
    
    # Add config file
    cmd.extend(["--add-data", "config.py:."])
    
    cmd.append("main.py")
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build successful!")
        print("Executable location: dist/MancomTimer.exe")
        if logo_file:
            print(f"✓ Logo included: {logo_file}")
        print("\nNote: The exe includes your logo and will display it on launch.")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
