"""
Configuration and theming for Mancom Timer & Notes App
"""

# Mancom, Inc color scheme
COLORS = {
    'primary': '#2c3e50',      # Dark blue-gray
    'accent': '#27ae60',        # Green (timer running)
    'warning': '#e67e22',       # Orange (paused)
    'danger': '#e74c3c',        # Red (delete)
    'background': '#f5f5f5',    # Light gray
    'surface': '#ffffff',       # White
    'text': '#2c3e50',          # Dark text
    'border': '#bdc3c7',        # Light gray border
    'highlight': '#d5f4e6',     # Light green highlight
}

# Application settings
SETTINGS = {
    'auto_save_interval': 30000,  # milliseconds
    'window_width': 1000,
    'window_height': 600,
    'data_file': 'tasks_data.json',
    'timer_update_interval': 1000,  # milliseconds
}

# Brand information
BRAND = {
    'name': 'Mancom, Inc',
    'app_name': 'Mancom Timer & Notes',
    'version': '1.0.0',
    'company': 'Mancom, Inc',
}

# UI Text
BUTTON_TEXT = {
    'add': 'Add',
    'start': 'Start',
    'stop': 'Stop',
    'delete': 'Delete Selected',
    'show': 'Show',
    'hide': 'Hide',
    'quit': 'Quit',
}

LABELS = {
    'tasks': 'MANCOM, INC - TASK TIMER',
    'task_input': 'Enter task name...',
    'select_task': 'Select a task to view details',
    'elapsed_time': 'Elapsed Time:',
    'notes': 'Notes:',
    'notes_placeholder': 'Add notes here...',
}

def get_stylesheet(mode='system'):
    """Return the application stylesheet for 'light' or 'dark' mode.
    Use 'system' to let the caller choose based on OS/Qt palette."""

    light = {
        **COLORS
    }

    dark = {
        'primary': '#1f2a36',
        'accent': '#2ecc71',
        'warning': '#d35400',
        'danger': '#c0392b',
        'background': '#1e1f23',
        'surface': '#2b2b2f',
        'text': '#ecf0f1',
        'border': '#3a3f44',
        'highlight': '#274b3a',
    }

    if mode == 'dark':
        C = dark
    else:
        C = light

    return f"""
        QMainWindow {{
            background-color: {C['background']};
        }}
        
        QPushButton {{
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: bold;
            border: none;
            color: white;
        }}
        
        QPushButton:hover {{
            opacity: 0.9;
        }}
        
        QPushButton:pressed {{
            opacity: 0.8;
        }}
        
        QPushButton#addBtn {{
            background-color: {C['primary']};
        }}
        
        QPushButton#startBtn {{
            background-color: {C['accent']};
        }}
        
        QPushButton#stopBtn {{
            background-color: {C['warning']};
        }}
        
        QPushButton#deleteBtn {{
            background-color: {C['danger']};
        }}
        
        QLineEdit, QTextEdit {{
            border: 1px solid {C['border']};
            border-radius: 4px;
            padding: 5px;
            background-color: {C['surface']};
            color: {C['text']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {C['primary']};
        }}
        
        QListWidget {{
            border: 1px solid {C['border']};
            border-radius: 4px;
            background-color: {C['surface']};
        }}
        
        QListWidget::item {{
            padding: 5px;
            margin: 2px 0px;
        }}
        
        QListWidget::item:selected {{
            background-color: {C['primary']};
            color: white;
        }}
        
        QLabel {{
            color: {C['text']};
        }}
    """
