import sys
import json
import os
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QListWidget, 
                             QListWidgetItem, QLineEdit, QTextEdit, QSplitter,
                             QMessageBox, QSystemTrayIcon, QMenu)
from PyQt5.QtCore import QTimer, Qt, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap
import config

class TimerManager(QObject):
    """Manages timers for individual tasks"""
    time_updated = pyqtSignal(str, int)  # task_id, elapsed_seconds
    
    def __init__(self):
        super().__init__()
        self.timers = {}
        self.current_task_id = None
        
    def start_task(self, task_id):
        """Start or resume a task timer"""
        if self.current_task_id and self.current_task_id != task_id:
            self.pause_task(self.current_task_id)
        
        self.current_task_id = task_id
        
        if task_id not in self.timers:
            self.timers[task_id] = {'elapsed': 0, 'running': False, 'qt_timer': QTimer()}
            self.timers[task_id]['qt_timer'].timeout.connect(
                lambda: self._tick_task(task_id)
            )
        
        self.timers[task_id]['running'] = True
        self.timers[task_id]['qt_timer'].start(1000)  # Update every second
        
    def pause_task(self, task_id):
        """Pause a task timer"""
        if task_id in self.timers:
            self.timers[task_id]['running'] = False
            self.timers[task_id]['qt_timer'].stop()
    
    def _tick_task(self, task_id):
        """Internal tick for a task"""
        if task_id in self.timers:
            self.timers[task_id]['elapsed'] += 1
            self.time_updated.emit(task_id, self.timers[task_id]['elapsed'])
    
    def get_elapsed_time(self, task_id):
        """Get elapsed time in seconds"""
        if task_id in self.timers:
            return self.timers[task_id]['elapsed']
        return 0
    
    def set_elapsed_time(self, task_id, seconds):
        """Set elapsed time for a task"""
        if task_id not in self.timers:
            self.timers[task_id] = {'elapsed': seconds, 'running': False, 'qt_timer': QTimer()}
            self.timers[task_id]['qt_timer'].timeout.connect(
                lambda: self._tick_task(task_id)
            )
        else:
            self.timers[task_id]['elapsed'] = seconds

class TaskData:
    """Data model for a task"""
    def __init__(self, task_id, name, created_at=None):
        self.id = task_id
        self.name = name
        self.created_at = created_at or datetime.now().isoformat()
        self.notes = ""
        self.elapsed_seconds = 0
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'notes': self.notes,
            'elapsed_seconds': self.elapsed_seconds
        }
    
    @staticmethod
    def from_dict(data):
        task = TaskData(data['id'], data['name'], data['created_at'])
        task.notes = data.get('notes', '')
        task.elapsed_seconds = data.get('elapsed_seconds', 0)
        return task

class DataStore:
    """Handles data persistence"""
    def __init__(self, filename='tasks_data.json'):
        self.filepath = Path(filename)
        
    def save(self, tasks):
        """Save tasks to file"""
        data = [task.to_dict() for task in tasks]
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load tasks from file"""
        if not self.filepath.exists():
            return []
        
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        
        return [TaskData.from_dict(item) for item in data]

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mancom Timer & Notes")
        self.setGeometry(100, 100, 1000, 600)
        
        # Set window icon if available (try multiple paths)
        icon_path = None
        for attempt in [Path("icon.ico"), Path(os.getcwd()) / "icon.ico", Path(__file__).parent / "icon.ico"]:
            if attempt.exists():
                icon_path = attempt
                break
        
        if icon_path:
            try:
                self.setWindowIcon(QIcon(str(icon_path)))
                print(f"✓ Window icon loaded from: {icon_path}")
            except Exception as e:
                print(f"Warning: Could not set window icon: {e}")
        
        # Initialize managers
        self.timer_manager = TimerManager()
        self.data_store = DataStore()
        self.tasks = []
        self.current_task = None
        self.task_counter = 0
        
        # Dirty flag tracks whether there are unsaved changes
        self.dirty = False

        # Setup UI first (before loading tasks)
        self.setup_ui()

        # Apply initial theme (system)
        self.current_theme = 'system'
        self.apply_theme('system')

        # Load saved tasks
        self.load_tasks()
        
        # Connect signals
        self.timer_manager.time_updated.connect(self.update_timer_display)
        
        # Setup system tray
        self.setup_tray()
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_tasks)
        self.auto_save_timer.start(30000)  # Save every 30 seconds
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create menu bar for theme switching
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")
        
        theme_light = view_menu.addAction("Light Theme")
        theme_dark = view_menu.addAction("Dark Theme")
        theme_system = view_menu.addAction("System Theme")
        
        theme_light.triggered.connect(lambda: self.apply_theme('light'))
        theme_dark.triggered.connect(lambda: self.apply_theme('dark'))
        theme_system.triggered.connect(lambda: self.apply_theme('system'))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Tasks list
        left_panel = QVBoxLayout()
        
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        
        tasks_label = QLabel("MANCOM, INC - TASK TIMER")
        tasks_label.setFont(title_font)
        tasks_label.setStyleSheet("color: #2c3e50; padding: 5px;")
        tasks_label.setWordWrap(True)
        left_panel.addWidget(tasks_label)
        
        # Task input
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task name...")
        self.task_input.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_task)
        add_btn.setMaximumWidth(70)
        input_layout.addWidget(add_btn)
        left_panel.addLayout(input_layout)
        
        # Tasks list
        self.tasks_list = QListWidget()
        self.tasks_list.itemClicked.connect(self.on_task_selected)
        left_panel.addWidget(self.tasks_list)
        
        # Delete button
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_task)
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        left_panel.addWidget(delete_btn)
        
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setMaximumWidth(300)
        
        # Right panel - Task details
        right_panel = QVBoxLayout()
        
        # Add Mancom logo if image exists
        logo_layout = QHBoxLayout()
        # Try multiple image formats: PNG, JPG, then GIF
        logo_path = None
        for ext in ['logo.png', 'logo.jpg', 'logo.jpeg', 'mancom.png', 'mancom.jpg', 'mancom.gif']:
            for attempt in [Path(ext), Path(os.getcwd()) / ext, Path(__file__).parent / ext]:
                if attempt.exists():
                    logo_path = attempt
                    break
            if logo_path:
                break
        
        if logo_path:
            try:
                logo_label = QLabel()
                pixmap = QPixmap(str(logo_path))
                if not pixmap.isNull():
                    # Scale to 64px height maintaining aspect ratio
                    pixmap = pixmap.scaledToHeight(64, Qt.SmoothTransformation)
                    logo_label.setPixmap(pixmap)
                    logo_label.setMaximumHeight(80)
                    logo_label.setAlignment(Qt.AlignCenter)
                    logo_layout.addStretch()
                    logo_layout.addWidget(logo_label)
                    logo_layout.addStretch()
                    right_panel.addLayout(logo_layout)
                    print(f"✓ Logo loaded: {logo_path.name}")
                else:
                    print(f"Warning: Could not load image from {logo_path}")
            except Exception as e:
                print(f"Warning: Error loading logo: {e}")
        
        # Task details label
        self.task_details_label = QLabel("Select a task to view details")
        self.task_details_label.setFont(title_font)
        self.task_details_label.setStyleSheet("color: #2c3e50; padding: 5px;")
        right_panel.addWidget(self.task_details_label)
        
        # Timer display
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(QLabel("Elapsed Time:"))
        self.timer_display = QLabel("00:00:00")
        self.timer_display.setFont(QFont("Courier", 16, QFont.Bold))
        self.timer_display.setStyleSheet("color: #27ae60; background-color: #ecf0f1; padding: 10px; border-radius: 5px;")
        timer_layout.addWidget(self.timer_display)
        timer_layout.addStretch()
        right_panel.addLayout(timer_layout)
        
        # Notes section
        notes_label = QLabel("Notes:")
        right_panel.addWidget(notes_label)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Add notes here...")
        self.notes_edit.textChanged.connect(self.on_notes_changed)
        right_panel.addWidget(self.notes_edit)
        
        # Start/Stop buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_task)
        self.start_btn.setStyleSheet("background-color: #27ae60; color: white;")
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_task)
        self.stop_btn.setStyleSheet("background-color: #e67e22; color: white;")
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        # Save button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save_clicked)
        self.save_btn.setStyleSheet("background-color: #2980b9; color: white;")
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        right_panel.addLayout(button_layout)
        
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        
        # Add to main layout
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget, 1)
        
        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def setup_tray(self):
        """Setup system tray icon and menu"""
        # Use a bundled icon if available, otherwise default
        icon_path = Path("icon.ico")
        if icon_path.exists():
            tray_icon = QIcon(str(icon_path))
            self.tray_icon = QSystemTrayIcon(tray_icon, self)
        else:
            self.tray_icon = QSystemTrayIcon(self)
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show_window)
        
        hide_action = tray_menu.addAction("Hide")
        hide_action.triggered.connect(self.hide_window)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        # Theme submenu
        theme_menu = tray_menu.addMenu("Theme")
        light_action = theme_menu.addAction("Light")
        dark_action = theme_menu.addAction("Dark")
        system_action = theme_menu.addAction("System")
        light_action.triggered.connect(lambda: self.apply_theme('light'))
        dark_action.triggered.connect(lambda: self.apply_theme('dark'))
        system_action.triggered.connect(lambda: self.apply_theme('system'))
        
        self.tray_icon.setContextMenu(tray_menu)
        # Show the tray icon; some environments may not support system tray
        try:
            self.tray_icon.show()
            print("✓ System tray icon displayed")
        except Exception as e:
            print(f"Warning: system tray unavailable: {e}")
        
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def on_tray_activated(self, reason):
        """Handle tray icon click"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide_window()
            else:
                self.show_window()

    def detect_system_theme(self):
        """Return 'dark' or 'light' based on the system palette."""
        try:
            palette = QApplication.palette()
            color = palette.color(QPalette.Window)
            # lightness ranges 0..255; lower -> darker
            return 'dark' if color.lightness() < 128 else 'light'
        except Exception:
            return 'light'

    def apply_theme(self, mode):
        """Apply the selected theme to the application."""
        if mode == 'system':
            chosen = self.detect_system_theme()
        else:
            chosen = mode

        stylesheet = config.get_stylesheet(chosen)
        # Apply to main window and ensure it cascades to all children
        self.setStyleSheet(stylesheet)
        # Force update of all widgets
        QApplication.instance().setStyle(QApplication.instance().style())
        self.current_theme = mode
    
    def show_window(self):
        """Show the application window"""
        self.showNormal()
        self.raise_()
        self.activateWindow()
    
    def hide_window(self):
        """Hide to system tray"""
        self.hide()
    
    def quit_app(self):
        """Quit the application"""
        self.save_tasks()
        QApplication.quit()
    
    def add_task(self):
        """Add a new task"""
        task_name = self.task_input.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Error", "Please enter a task name")
            return
        
        self.task_counter += 1
        task = TaskData(str(self.task_counter), task_name)
        self.tasks.append(task)
        self.task_input.clear()
        
        self.refresh_task_list()
        self.set_dirty(True)
    
    def delete_task(self):
        """Delete the selected task"""
        if not self.current_task:
            return
        
        reply = QMessageBox.question(self, "Confirm", 
                                     f"Delete task '{self.current_task.name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.tasks.remove(self.current_task)
            self.timer_manager.pause_task(self.current_task.id)
            self.current_task = None
            self.refresh_task_list()
            self.clear_task_details()
            self.set_dirty(True)
    
    def on_task_selected(self, item):
        """Handle task selection"""
        task_index = self.tasks_list.row(item)
        self.current_task = self.tasks[task_index]
        self.display_task_details()
    
    def display_task_details(self):
        """Display the selected task's details"""
        if not self.current_task:
            self.clear_task_details()
            return
        
        self.task_details_label.setText(
            f"Task: {self.current_task.name} | Created: {self.current_task.created_at[:10]}"
        )
        self.notes_edit.blockSignals(True)
        self.notes_edit.setPlainText(self.current_task.notes)
        self.notes_edit.blockSignals(False)
        self.update_timer_display(self.current_task.id, self.current_task.elapsed_seconds)
        
        # Enable start button
        if self.timer_manager.current_task_id != self.current_task.id:
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
        else:
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
    
    def clear_task_details(self):
        """Clear task details display"""
        self.task_details_label.setText("Select a task to view details")
        self.notes_edit.clear()
        self.timer_display.setText("00:00:00")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
    
    def start_task(self):
        """Start the selected task's timer"""
        if not self.current_task:
            return
        
        self.timer_manager.start_task(self.current_task.id)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.refresh_task_list()
        self.set_dirty(True)
    
    def stop_task(self):
        """Stop the selected task's timer"""
        if not self.current_task:
            return
        
        self.timer_manager.pause_task(self.current_task.id)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.refresh_task_list()
        self.set_dirty(True)
    
    def on_notes_changed(self):
        """Handle notes text changes"""
        if self.current_task:
            self.current_task.notes = self.notes_edit.toPlainText()
            self.set_dirty(True)
    
    def update_timer_display(self, task_id, elapsed_seconds):
        """Update the timer display showing total time (stored + running)"""
        # Don't overwrite stored elapsed here; save_tasks() handles that
        # Calculate total: stored + currently running
        if self.current_task and task_id == self.current_task.id:
            total_elapsed = self.current_task.elapsed_seconds + elapsed_seconds
            hours = total_elapsed // 3600
            minutes = (total_elapsed % 3600) // 60
            seconds = total_elapsed % 60
            self.timer_display.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        self.refresh_task_list()
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        self.tasks_list.clear()
        
        for task in self.tasks:
            elapsed = self.timer_manager.get_elapsed_time(task.id)
            total_seconds = task.elapsed_seconds + elapsed
            
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            is_running = (self.timer_manager.current_task_id == task.id and 
                         task.id in self.timer_manager.timers and 
                         self.timer_manager.timers[task.id]['running'])
            
            status = "▶ " if is_running else "⏸ "
            list_item_text = f"{status}{task.name} [{time_str}]"
            
            item = QListWidgetItem(list_item_text)
            if is_running:
                item.setBackground(QColor("#d5f4e6"))
            self.tasks_list.addItem(item)
    
    def save_tasks(self):
        """Save tasks to file"""
        # Update elapsed time in tasks from running timers
        # Accumulate running time into stored time WITHOUT resetting counter
        for task in self.tasks:
            if task.id in self.timer_manager.timers:
                running = self.timer_manager.timers[task.id]['elapsed']
                if running > 0:
                    task.elapsed_seconds += running
                    # Move running back to base, but keep it accumulating properly
                    # by storing the old base and resetting to 0 for next interval
                    self.timer_manager.timers[task.id]['elapsed'] = 0
        
        self.data_store.save(self.tasks)
        self.set_dirty(False)
    
    def on_save_clicked(self):
        """Handler for Save button"""
        self.save_tasks()

    def set_dirty(self, value: bool = True):
        """Set dirty flag and update Save button state"""
        self.dirty = bool(value)
        try:
            self.save_btn.setEnabled(self.dirty)
        except Exception:
            pass

    def load_tasks(self):
        """Load tasks from file"""
        self.tasks = self.data_store.load()
        
        # Set counter to max task id
        if self.tasks:
            max_id = max(int(task.id) for task in self.tasks)
            self.task_counter = max_id
        
        # Initialize timer manager with loaded times
        for task in self.tasks:
            self.timer_manager.set_elapsed_time(task.id, task.elapsed_seconds)
        
        self.refresh_task_list()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # If there are unsaved changes, prompt the user
        if getattr(self, 'dirty', False):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Save before closing?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            ret = msg.exec_()
            if ret == QMessageBox.Cancel:
                event.ignore()
                return
            if ret == QMessageBox.Save:
                self.save_tasks()
        # Hide to tray instead of quitting the app
        self.hide()
        event.ignore()

def main():
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
