# 🎯 Application Flow & Architecture

## User Workflow

```
START
  │
  ├─→ Install Application
  │   ├─ Double-click install.bat (Windows)
  │   ├─ OR bash install.sh (Linux/macOS)
  │   └─ Dependencies installed automatically
  │
  ├─→ Launch Application  
  │   ├─ Double-click run.bat (Windows)
  │   ├─ OR python main.py
  │   └─ GUI window opens
  │
  ├─→ Create First Task
  │   ├─ Type: "Project Name"
  │   ├─ Press Enter or click "Add"
  │   └─ Task appears in list
  │
  ├─→ Start Working
  │   ├─ Click task to select
  │   ├─ Click "Start" button
  │   ├─ ⏱️  Timer begins counting
  │   ├─ 📝 Add notes as needed
  │   └─ Time persists on screen
  │
  ├─→ Switch Tasks
  │   ├─ Click different task
  │   ├─ Previous task ⏸️  PAUSES
  │   ├─ New task ▶️  STARTS
  │   └─ Elapsed time preserved
  │
  ├─→ Minimize App
  │   ├─ Click minimize button
  │   ├─ App → System tray
  │   ├─ Double-click tray icon
  │   └─ App restores
  │
  ├─→ Work Throughout Day
  │   ├─ Add more tasks
  │   ├─ Switch between them
  │   ├─ Add notes
  │   └─ Timer accurately tracks
  │
  └─→ Close Application
      ├─ Click close button
      ├─ All data auto-saved
      ├─ 💾 tasks_data.json updated
      └─ EXIT (data preserved)
```

## Component Architecture

```
┌─────────────────────────────────────────────────┐
│         MANCOM TIMER APPLICATION                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  TimerApp (QMainWindow)                  │   │
│  │  - Window management                     │   │
│  │  - UI layout                             │   │
│  │  - Event coordination                    │   │
│  └──────────────────────────────────────────┘   │
│          ↓           ↓            ↓             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │TimerMgr  │  │TaskData  │  │DataStore │      │
│  │          │  │          │  │          │      │
│  │Manages   │  │Holds     │  │Persists  │      │
│  │timing    │  │task info │  │to JSON   │      │
│  │per task  │  │          │  │          │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                 │
│  Auto-save Timer: 30 second intervals          │
│  Signal System: Qt signal/slot pattern         │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Data Flow

```
USER ACTION          PROCESSING               STORAGE
─────────────────────────────────────────────────────

Click "Add"  ──→  Create TaskData    ──→  In-memory
                  Emit timer signal        list
                                    
Start timer  ──→  TimerManager      ──→  1/sec
                  starts Qt timer        updates
                                    
Switch task  ──→  Pause old timer   ──→  Save
                  Start new timer        elapsed
                                    
Add notes    ──→  Update TaskData   ──→  To task
                                    
Close app    ──→  DataStore.save()  ──→  Updated
                  All tasks           JSON file
                  to JSON file
```

## File Organization & Purpose

```
SOURCE CODE (Python)
├── main.py             [468 lines] Core application
│   ├─ TimerApp class  - Main window & UI
│   ├─ TimerManager    - Timer orchestration  
│   ├─ TaskData        - Data model
│   └─ DataStore       - JSON persistence
│
├── config.py           [125 lines] Configuration
│   ├─ Color palette
│   ├─ UI text strings
│   ├─ Styling sheets
│   └─ Settings
│
└── build.py            Executable builder
    └─ PyInstaller wrapper

BUILD & INSTALL
├── requirements.txt    PyQt5 dependency
├── install.bat        Windows installer
├── install.sh         Linux/macOS installer  
├── run.bat           Windows launcher
└── build.py          Build .exe helper

UTILITIES
├── create_icon.py      Generate icon.ico
└── .gitignore         Git exclusions

DATA
├── icon.ico            [Optional] Mancom logo
└── tasks_data.json     [Auto-created] Task storage

DOCUMENTATION [7 files]
├── INDEX.md               ← START HERE (navigation)
├── GETTING_STARTED.md     Main intro
├── QUICKSTART.md          Windows setup
├── README.md              Complete guide
├── FEATURES.md            Feature checklist
├── BRANDING.md            Logo customization
├── DEVELOPMENT.md         Extension guide
└── PROJECT_SUMMARY.md     Technical overview
```

## Timer Logic

```
STATE MACHINE
         ┌──────────────────────────────────────┐
         │                                      │
    ┌────▼────┐                        ┌────────┴──┐
    │ CREATED │                        │ DELETED   │
    └────┬────┘                        └───────────┘
         │
         ├─ start() ──────┐
         │                ▼
    ┌────┴────────────┐   ┌──────────────┐
    │   INITIALIZING  │──▶│   RUNNING    │
    └────────────────┘   │ ▶ Timer tick │
                         └──┬──────────┬─┘
                            │          │
                       pause()         stop()
                            │          │
                      ┌──────▼──┐  ┌───▼────────┐
                      │ PAUSED  │  │ COMPLETED  │
                      └──┬──────┘  └────────────┘
                         │
                    resume()
                         │
                      ┌──▼──┐
                      │────▶│ RUNNING
                      └─────┘
```

## Data Persistence Flow

```
RUNTIME
┌──────────────────────┐
│  In-Memory Tasks     │
│  [TaskData...]       │
│  Updated constantly  │
└──────┬───────────────┘
       │
       ├─ Auto-save (30s) ──────┐
       │                        │
       └─ On Close ────────────▶│
                                ▼
                    ┌──────────────────────┐
                    │ JSON Serialization   │
                    │ DataStore.save()     │
                    └──────┬───────────────┘
                           ▼
                    ┌──────────────────────┐
                    │ tasks_data.json File │
                    │ (Disk Storage)       │
                    └──────────────────────┘

STARTUP
         ┌──────────────────────┐
         │ tasks_data.json File │
         │ (Disk Storage)       │
         └──────┬───────────────┘
                ▼
         ┌──────────────────────┐
         │ JSON Deserialization │
         │ DataStore.load()     │
         └──────┬───────────────┘
                ▼
         ┌──────────────────────┐
         │  In-Memory Tasks     │
         │  Application Ready   │
         └──────────────────────┘
```

## Task Switching Example

```
TIME  TASK              ACTION                    STATE
───────────────────────────────────────────────────────
1:00  Client Meeting    Click "Start"       ▶ RUNNING
1:30  │                 (30 seconds)        ⏱️ 00:00:30
      │
      ├─ CODE REVIEW    Click on CODE       ⏸️ PAUSED
2:00  │                 REVIEW task
      │
      │                 CODE REVIEW         ▶ RUNNING  
      │                 Click "Start"       ⏱️ 00:00:00
2:30  │                 (30 seconds)        ⏱️ 00:00:30
      │
      └─ Client Call    Click on CLIENT     ⏸️ PAUSED
      (resumed)         CALL task
                        
      Client Call       Click "Start"       ▶ RUNNING
3:00  (resumed)         CONTINUES from      ⏱️ 00:01:00
                        previous time!

RESULT:
- Client Meeting: 2:00 total time
- Code Review: 0:30 total time  
- All time preserved, never lost!
```

## GUI Layout

```
┌─────────────────────────────────────────────────────┐
│ MANCOM TIMER & NOTES                          _  ■ ✕ │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────┐  ┌───────────────────────┐   │
│  │                 │  │ Task: Client Call     │   │
│  │  TASK LIST      │  │ Created: 2026-02-09  │   │
│  │                 │  │                       │   │
│  │ Add Task Input  │  │ Elapsed Time:         │   │
│  │ + [Add]         │  │ [00:02:15] (bold)     │   │
│  │                 │  │                       │   │
│  │ ▶ Task 1        │  │ Notes:                │   │
│  │   [00:02:15]    │  │ ┌───────────────────┐ │   │
│  │                 │  │ │ Add notes here... │ │   │
│  │ ▶ Task 2        │  │ │ (text editor)     │ │   │
│  │   [00:05:30]    │  │ └───────────────────┘ │   │
│  │                 │  │                       │   │
│  │ ▶ Task 3        │  │ [▶ Start] [⏸ Stop]   │   │
│  │   [00:01:05]    │  │                       │   │
│  │                 │  │                       │   │
│  │ [Delete]        │  │                       │   │
│  │                 │  │                       │   │
│  └─────────────────┘  └───────────────────────┘   │
│                                                     │
│  [minimize]  Status: Running  [Tray icon: ↓]      │
└─────────────────────────────────────────────────────┘

System Tray: ■ MancomTimer | Timer [HH:MM:SS]
             ├─ Show
             ├─ Hide
             ├─ Quit
```

## Deployment Options

```
OPTION 1: Share Python Version
└─ Share entire folder
   ├─ User installs: install.bat
   └─ User runs: run.bat
   (Requires Python installed)

OPTION 2: Standalone .exe
└─ Run: python build.py
   └─ Creates: dist/MancomTimer.exe
      ├─ Single file
      ├─ No Python needed
      ├─ Works on any Windows
      └─ Easy to distribute

OPTION 3: Network Share
└─ Place .exe on network drive
   ├─ Users run from \\server\apps\
   └─ Centralized update location
```

---

This architecture ensures:
✅ Clean separation of concerns
✅ Reliable data persistence  
✅ Responsive UI updates
✅ Accurate timer tracking
✅ Easy extensibility
✅ Professional user experience
