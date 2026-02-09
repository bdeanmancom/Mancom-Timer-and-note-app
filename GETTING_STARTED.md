# 🚀 GETTING STARTED - Mancom Timer & Notes

Welcome! Your complete Windows task timer and note-taking application is ready to use.

## ⚡ Quick Start (30 seconds)

### Windows Users:
```
1. Double-click: install.bat
2. Double-click: run.bat
3. Start tracking time!
```

### Linux/macOS Users:
```bash
bash install.sh
python main.py
```

## 📋 What This App Does

```
YOU                          MANCOM TIMER APP
│                            │
├─ Start "Client Call"  ───> ⏱️  Timer starts
├─ Take notes          ───> 📝 Notes saved
├─ Switch "Code Review" ───> ⏸️  "Client Call" pauses
│                            ▶️  "Code Review" starts  
├─ Switch back        ───> ⏱️  "Client Call" resumes
│                            📊 Both times tracked
└─ Close app           ───> 💾 Everything saved

All your data persists. Time is never lost!
```

## 🎯 Main Features

| Feature | How It Works |
|---------|-------------|
| **Task Timer** | Create tasks and each gets its own timer |
| **Auto-Pause** | Switching tasks auto-pauses the previous one |
| **Notes** | Each task has its own notes section |
| **Data Saved** | Auto-saves every 30 seconds + on close |
| **System Tray** | Minimize to tray, double-click to restore |
| **Mancom Branding** | Professional UI with your company colors |

## 📦 What's Included

```
🗂️ Complete Application Files:
   ├─ main.py (468 lines) - Full working application
   ├─ config.py (125 lines) - Settings & theming
   ├─ requirements.txt - Dependencies
   ├─ install.bat/.sh - Easy installation
   ├─ run.bat - Quick launcher
   ├─ build.py - Build standalone .exe
   └─ Documentation (6 files)
```

## 📚 Documentation Guide

| Document | For Whom | What To Read |
|----------|----------|-------------|
| **QUICKSTART.md** | Windows users | Step-by-step setup |
| **README.md** | Everyone | Complete feature guide |
| **FEATURES.md** | Project managers | Full feature checklist |
| **BRANDING.md** | Designers | Add Mancom logo |
| **DEVELOPMENT.md** | Developers | Extend the app |
| **PROJECT_SUMMARY.md** | Leads/Managers | Project overview |

## 🎮 How To Use

### Adding Tasks
1. Type task name: "Client Call", "Code Review", etc.
2. Press Enter or click "Add"
3. Click the task to select it
4. Click "Start" - timer begins!

### Taking Notes
- While a task is selected
- Type in the Notes section on the right
- Notes auto-save with the task

### Switching Tasks
1. Click a different task
2. Click "Start"
3. Previous task timer auto-pauses
4. New task timer auto-starts

### Minimizing
- Click minimize button → App goes to system tray
- Double-click tray icon → App restores
- Right-click tray → See options

## 🏗️ Building a Standalone .exe

If you want a single file to distribute:

```bash
# After running install.bat:
python build.py

# Find your .exe:
dist/MancomTimer.exe
```

No Python needed! Share it with anyone.

## 🔧 Customization

### Add Your Logo
1. Get your Mancom Inc logo (PNG or ICO format)
2. Save as `icon.ico` in the app folder
3. Rebuild: `python build.py`
4. Done! Your logo appears in the taskbar and tray

### Change Colors
- Edit `config.py` in the `COLORS` section
- Change company branding text throughout
- Re-run the app

### Add Features
- See `DEVELOPMENT.md` for extension guide
- Code is modular and well-documented
- Add categories, priorities, exports, etc.

## 📊 Data Location

Tasks are saved in: `tasks_data.json`

- 💾 Backup by copying this file
- 📤 Share tasks between computers
- 🗑️ Delete to start fresh (⚠️ data loss!)

## ❓ Common Questions

**Q: Can I run this without Python?**
A: Yes! Build it with `python build.py` to get `MancomTimer.exe`

**Q: Will my data be saved?**
A: Yes! Auto-saved every 30 seconds and on close.

**Q: Can I add my company logo?**
A: Yes! See BRANDING.md for instructions (2 minutes)

**Q: Does it work on Mac/Linux?**
A: Yes! Run `bash install.sh` then `python main.py`

**Q: Can I extend this app?**
A: Yes! See DEVELOPMENT.md for the guide.

**Q: What if I have issues?**
A: Check README.md Troubleshooting section or see QUICKSTART.md

## 🎓 Next Steps

### For Immediate Use:
1. ✅ Run `install.bat`
2. ✅ Run `run.bat`
3. ✅ Start tracking tasks!

### For Company Deployment:
1. ✅ Add your Mancom logo (see BRANDING.md)
2. ✅ Build .exe with `python build.py`
3. ✅ Share `dist/MancomTimer.exe` with your team
4. ✅ Everyone can use it without Python!

### For Development:
1. ✅ Read DEVELOPMENT.md
2. ✅ Customize as needed
3. ✅ Rebuild and deploy

## 🎉 You're Ready!

Everything is set up and ready to use. 

**Start with**: Double-click `run.bat`

**Questions?** Check the README.md or relevant documentation files.

**Enjoy your new timer app!** ⏱️

---

**Mancom, Inc - Professional Time & Task Management**

Built with PyQt5 | Production Ready | Fully Documented
