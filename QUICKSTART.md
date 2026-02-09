# Quick Start Guide - Windows Users

## Installation (5 minutes)

### Option 1: Easy Installation (Recommended)

1. **Download the repository**
   - Visit https://github.com/bdeanmancom/Mancom-Timer-and-note-app
   - Click "Code" > "Download ZIP"
   - Extract the ZIP file

2. **Install Dependencies**
   - Double-click `install.bat`
   - Wait for the installation to complete
   - A command window will appear and show "Installation complete!"

3. **Run the Application**
   - Double-click `run.bat` to start the app
   - The Mancom Timer window will open

### Option 2: Build Standalone Executable

If you want a single `.exe` file that doesn't need Python:

1. Complete steps 1-2 from Option 1

2. **Build the Executable**
   - Open Command Prompt in the application folder
   - Run: `python build.py`
   - Wait for the build to complete

3. **Find Your Executable**
   - Look in the `dist/` folder
   - You'll see `MancomTimer.exe`
   - This file can be run on any Windows machine!

## Using the Application

### Starting a Task
1. Type the task name (e.g., "Client Meeting", "Code Review")
2. Click "Add" or press Enter
3. Click on the task in the list
4. Click "Start" to begin the timer

### Switching Tasks
- Just click on another task and hit "Start"
- The previous task's timer automatically pauses
- Return to the previous task and click "Start" to resume

### Taking Notes
- While a task is selected, type in the Notes section
- Your notes are automatically saved with each task

### Minimizing to Tray
- Click the minimize button
- The app minimizes to your system tray
- Double-click the tray icon to restore
- Right-click the tray icon for more options

### Tracking Time
- Each task shows its total elapsed time in brackets `[HH:MM:SS]`
- The main timer displays the selected task's total time
- All times are saved automatically

## Where's My Data?

Your task data is saved in `tasks_data.json` in the same folder as the application:
- **Backup**: Copy this file to save your work
- **Share**: Send this file to another computer to transfer all tasks and notes
- **Delete**: Delete this file to start fresh (but your tasks will be lost!)

## Troubleshooting

**Problem: "Python not found"**
- Install Python from https://www.python.org/
- Check "Add Python to PATH" during installation
- Restart your computer

**Problem: "ModuleNotFoundError: No module named 'PyQt5'"**
- Run `install.bat` again
- Or manually run: `pip install PyQt5`

**Problem: Tasks not saving**
- Make sure you have write permissions in the application folder
- Try moving the folder to a different location (e.g., Desktop or Documents)

**Problem: Timer not starting**
- Click "Start" button (it should turn orange/red when pressed)
- Check that your selected task is highlighted

## Tips & Tricks

✅ **Name tasks clearly**: Use descriptive names like "Fix Bug #123" instead of "Work"

✅ **Use notes consistently**: Add details about what you did during each session

✅ **Regular backups**: Copy `tasks_data.json` to your cloud storage or external drive

✅ **Keyboard shortcut**: Press Enter while typing a task name to quickly add it

✅ **Multi-tasking tracking**: Keep multiple tasks running on different parts of your work

## Need Help?

- Check the full README.md for detailed documentation
- Visit: https://github.com/bdeanmancom/Mancom-Timer-and-note-app/issues
- Review the FAQ section in README.md

---

**Mancom, Inc - Professional Time Tracking**
