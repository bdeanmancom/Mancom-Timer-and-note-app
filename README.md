# Mancom Timer & Notes App

A professional task timer application for Windows with built-in note-taking capabilities. Perfect for tracking work sessions and managing your time efficiently.

## Features

✨ **Core Features:**
- **Task Management**: Create and organize multiple tasks
- **Running Timer**: Individual timers for each task with automatic start/stop
- **Task Switching**: Pause one timer and start another with a single click
- **Notes**: Add detailed notes to each task
- **Time Tracking**: Displays total time spent on each task
- **Data Persistence**: Automatically saves your tasks and progress

🎨 **User Interface:**
- Clean, modern, professional design
- Minimizable to system tray
- Easy to move and resize
- Real-time timer updates
- One-click task management
- Mancom, Inc branding

## Installation

### Prerequisites
- Windows 7 or later (also works on macOS and Linux)
- Python 3.8 or higher

### Quick Start (Windows)

1. **Clone or download this repository**

2. **Run the installer:**
   ```bash
   install.bat
   ```

3. **Start the application:**
   ```bash
   python main.py
   ```

### Alternative: Manual Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

1. **Add a Task:**
   - Enter a task name in the text field at the top
   - Click "Add" or press Enter
   - The new task appears in the task list

2. **Start Timer:**
   - Click on a task to select it
   - Click the "Start" button
   - The timer begins counting elapsed time
   - The task is highlighted in green

3. **Switch Tasks:**
   - Click on another task
   - Click "Start" to begin the new task
   - The previous task's timer automatically pauses
   - Your elapsed time is preserved

4. **Add Notes:**
   - While a task is selected, type notes in the "Notes" section
   - Notes are automatically saved
   - Each task maintains its own notes

5. **Stop Task:**
   - Click the "Stop" button to pause the current timer
   - The timer can be restarted later and will continue from where it paused

6. **Delete Task:**
   - Select a task
   - Click "Delete Selected"
   - Confirm the deletion

7. **Minimize/Restore:**
   - Click the minimize button to collapse to system tray
   - Double-click the tray icon to restore
   - Right-click the tray icon for menu options

## Building a Standalone Executable

To create a standalone `.exe` file that doesn't require Python installed:

```bash
# Install PyInstaller (if not already installed)
pip install pyinstaller

# Run the build script
python build.py
```

The executable will be created in the `dist/` folder as `MancomTimer.exe`.

### Distributing the Application

After building:
1. The standalone `MancomTimer.exe` can be run on any Windows machine
2. No Python installation required
3. Data is stored in `tasks_data.json` in the same directory

## Data Storage

Tasks and notes are automatically saved to `tasks_data.json` in the application directory. This file is:
- Auto-saved every 30 seconds during use
- Saved when the application closes
- Loaded automatically on startup

### Backing Up Your Data

Simply copy `tasks_data.json` to a safe location to back up all your tasks and time tracking data.

## File Structure

```
Mancom-Timer-and-note-app/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── build.py               # Script to build Windows executable
├── install.bat            # Windows installation script
├── install.sh             # Linux/macOS installation script
├── tasks_data.json        # Auto-generated task data file
└── README.md              # This file
```

## Keyboard Shortcuts

- `Enter` in task input field: Add new task
- `Ctrl+Q`: Quit application (when focused)

## Troubleshooting

### "Python not found" error
- Install Python 3.8+ from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "No module named PyQt5" error
- Run: `pip install PyQt5`

### Tasks not saving
- Check that the application has write permissions in its directory
- Ensure disk space is available

### Timer not advancing
- Make sure the "Start" button is clicked (status should show ▶)
- Check system clock is running correctly

## Development

### Project Structure
- **main.py**: Contains all application logic including:
  - `TimerApp`: Main GUI window
  - `TimerManager`: Timer state management
  - `TaskData`: Task data model
  - `DataStore`: File persistence

### Adding Features

To extend the application, you can modify `main.py`:
- Add new signals in `TimerManager` for events
- Extend `TaskData` with additional fields
- Modify `setup_ui()` to add new UI elements
- Extend `DataStore` for different persistence methods

## License

This project is part of the Mancom, Inc suite.

## Support

For issues or feature requests, please visit the project repository:
https://github.com/bdeanmancom/Mancom-Timer-and-note-app

---

**Built with ❤️ for Mancom, Inc**