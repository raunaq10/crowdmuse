# HOW TO RUN THE ATTENDANCE SCRIPT

## Method 1: From Command Line (Easiest)

### Step 1: Open PowerShell or Command Prompt
- Press `Windows + R`
- Type `powershell` or `cmd`
- Press Enter

### Step 2: Navigate to Project Folder
```bash
cd "C:\Users\singh\OneDrive\Desktop\attendance system"
```

### Step 3: Run the Script
```bash
python scripts/show_attendance.py
```

---

## Method 2: From VS Code Terminal

1. Open VS Code in your project folder
2. Press `` Ctrl + ` `` (backtick) to open terminal
3. Run:
```bash
python scripts/show_attendance.py
```

---

## Method 3: Direct Path (From Anywhere)

```bash
python "C:\Users\singh\OneDrive\Desktop\attendance system\scripts\show_attendance.py"
```

---

## Method 4: Create a Batch File (Double-Click to Run)

Create a file `view_attendance.bat` in your project root:

```batch
@echo off
cd /d "C:\Users\singh\OneDrive\Desktop\attendance system"
python scripts/show_attendance.py
pause
```

Then just double-click `view_attendance.bat` to run!

---

## Current Project Location

**Folder:** `C:\Users\singh\OneDrive\Desktop\attendance system`

**Script Location:** `scripts\show_attendance.py`

---

## Quick Reference

| Location | Command |
|----------|---------|
| **In project folder** | `python scripts/show_attendance.py` |
| **From anywhere** | `python "C:\Users\singh\OneDrive\Desktop\attendance system\scripts\show_attendance.py"` |
| **VS Code terminal** | `python scripts/show_attendance.py` |

---

## Troubleshooting

**If "python" is not recognized:**
- Use `py` instead: `py scripts/show_attendance.py`
- Or use full path: `C:\Python311\python.exe scripts/show_attendance.py`

**If script not found:**
- Make sure you're in the project folder
- Check that `scripts\show_attendance.py` exists
