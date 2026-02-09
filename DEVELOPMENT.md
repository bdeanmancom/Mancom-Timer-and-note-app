# Development Guide

## Project Architecture

The Mancom Timer & Notes App is built with a clean, modular architecture:

### Main Components

```
main.py
├── TimerManager (QObject)
│   └── Manages individual task timers with PyQt5 signals
├── TaskData
│   └── Data model for tasks
├── DataStore
│   └── File persistence layer (JSON)
└── TimerApp (QMainWindow)
    └── Main GUI and application logic
```

### Code Organization

- **TimerManager**: Handles all timer logic, one timer per task
- **TaskData**: Simple data class holding task information
- **DataStore**: JSON serializer/deserializer for tasks
- **TimerApp**: Main window, UI setup, and event handling

## Adding Features

### 1. Add Task Properties

To add new properties to tasks:

```python
# In TaskData class
def __init__(self, task_id, name, created_at=None):
    self.id = task_id
    self.name = name
    self.created_at = created_at or datetime.now().isoformat()
    self.notes = ""
    self.elapsed_seconds = 0
    self.priority = "normal"  # NEW FIELD
    self.category = "work"     # NEW FIELD
```

Update `to_dict()` and `from_dict()` methods to include new fields.

### 2. Add UI Elements

To add new UI elements:

```python
# In setup_ui() method
category_label = QLabel("Category:")
self.category_combo = QComboBox()
self.category_combo.addItems(["Work", "Personal", "Meeting"])
self.category_combo.currentTextChanged.connect(self.on_category_changed)
right_panel.addWidget(category_label)
right_panel.addWidget(self.category_combo)
```

### 3. Add New Features

Example: Task Statistics

```python
class TaskStats:
    """Calculate statistics for tasks"""
    
    @staticmethod
    def total_time(tasks):
        """Calculate total time across all tasks"""
        return sum(task.elapsed_seconds for task in tasks)
    
    @staticmethod
    def average_time(tasks):
        """Calculate average task duration"""
        if not tasks:
            return 0
        return TaskStats.total_time(tasks) / len(tasks)
```

### 4. Custom Styling

Modify the `setup_ui()` method's stylesheet section:

```python
self.setStyleSheet("""
    QMainWindow {
        background-color: #f5f5f5;
    }
    /* Add more custom styles here */
""")
```

## Extending with Signals

The app uses PyQt5 signals for event handling:

```python
# Define a new signal in TimerManager
task_completed = pyqtSignal(str)  # task_id

# Emit the signal
self.task_completed.emit(task_id)

# Connect in TimerApp
self.timer_manager.task_completed.connect(self.on_task_completed)
```

## Testing

To test the application:

```bash
# Run with debug output
python main.py

# Test with sample data
# Edit create a test file to populate initial data
```

## Building for Distribution

### Create Windows Executable

```bash
# Install build dependencies
pip install pyinstaller

# Build standalone.exe
python build.py

# Find in dist/MancomTimer.exe
```

### Create Installer

For a more professional distribution:

```bash
pip install pyinstaller inno-setup
# Configure installer in build script
```

## Performance Optimization

For apps with many tasks (100+):

1. **Use database instead of JSON**
   ```python
   # Replace DataStore with SQLite
   import sqlite3
   ```

2. **Lazy load task data**
   ```python
   # Load task details on-demand
   ```

3. **Optimize timer updates**
   ```python
   # Use event batching instead of per-second updates
   ```

## Future Enhancement Ideas

- [ ] Task categories and filtering
- [ ] Task search functionality
- [ ] Export reports (PDF, CSV)
- [ ] Task analytics dashboard
- [ ] Recurring tasks
- [ ] Task reminders
- [ ] Pomodoro timer mode
- [ ] Task priority levels
- [ ] Archive completed tasks
- [ ] Cloud sync (Dropbox, Google Drive)
- [ ] Dark mode theme
- [ ] Keyboard shortcuts customization
- [ ] Task templates
- [ ] Integration with calendar apps
- [ ] Time tracking reports

## Debugging

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug("Timer started for task: %s", task_id)
```

## Code Style

Follow PEP 8 guidelines:

```bash
# Check code style
pip install flake8
flake8 main.py

# Auto-format code
pip install black
black main.py
```

## Contributing

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make changes and test
3. Commit with clear messages: `git commit -m "Add feature description"`
4. Push and create pull request

---

Happy coding! 🚀
