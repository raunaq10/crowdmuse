# HOW TO VIEW ATTENDANCE TABLE

## Quick Method (Easiest)

**Run this command:**
```bash
python scripts/show_attendance.py
```

This will display all attendance records in a readable table format.

---

## Method 1: Using Python Script

### Simple View Script
```bash
python scripts/show_attendance.py
```

### Detailed View Script
```bash
python scripts/view_attendance.py
```

---

## Method 2: Using SQLite Command Line

1. **Open SQLite:**
   ```bash
   sqlite3 attendance.db
   ```

2. **View all attendance records:**
   ```sql
   SELECT * FROM attendance;
   ```

3. **View with student names:**
   ```sql
   SELECT 
       a.id,
       s.name,
       s.rollNumber,
       a.date,
       a.time,
       a.room,
       a.status
   FROM attendance a
   JOIN students s ON a.studentId = s.id
   ORDER BY a.date DESC;
   ```

4. **Exit SQLite:**
   ```sql
   .quit
   ```

---

## Method 3: Using DB Browser for SQLite (GUI)

1. **Download DB Browser:**
   - https://sqlitebrowser.org/
   - Install it

2. **Open Database:**
   - Open DB Browser
   - Click "Open Database"
   - Navigate to: `C:\Users\singh\OneDrive\Desktop\attendance system\attendance.db`
   - Click Open

3. **View Attendance Table:**
   - Click "Browse Data" tab
   - Select "attendance" from the table dropdown
   - All records will be displayed in a table

---

## Method 4: Using VS Code

1. Install "SQLite Viewer" extension in VS Code
2. Right-click on `attendance.db`
3. Select "Open Database"
4. Click on "attendance" table to view

---

## Method 5: Using API (If Server Running)

### Get all attendance by student roll number:
```bash
GET http://localhost:3001/api/attendance/student/ADRLIM301
```

### Get attendance by date:
```bash
GET http://localhost:3001/api/attendance/date/2026-01-23
```

### Get attendance by room:
```bash
GET http://localhost:3001/api/attendance/room/Lab-101
```

---

## Method 6: Direct Python Code

Create a file `view.py`:
```python
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT a.*, s.name, s.rollNumber 
    FROM attendance a 
    JOIN students s ON a.studentId = s.id
""")

for row in cursor.fetchall():
    print(row)

conn.close()
```

Run: `python view.py`

---

## Database Location

**File:** `C:\Users\singh\OneDrive\Desktop\attendance system\attendance.db`

**Table:** `attendance`

---

## Quick Reference

| Method | Command |
|--------|---------|
| **Easiest** | `python scripts/show_attendance.py` |
| **SQLite CLI** | `sqlite3 attendance.db` then `SELECT * FROM attendance;` |
| **GUI Tool** | DB Browser for SQLite |
| **API** | `GET http://localhost:3001/api/attendance/student/{rollNumber}` |

---

## Current Status

Run `python scripts/show_attendance.py` to see current attendance records!
