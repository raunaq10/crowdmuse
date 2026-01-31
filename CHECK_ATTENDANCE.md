# HOW TO CHECK ATTENDANCE

## Method 1: Python Script (Easiest & Fastest)

**Run this command:**
```bash
python scripts/show_attendance.py
```

This shows all attendance records in a formatted table.

---

## Method 2: Via Web Browser

1. **Open:** http://localhost:5000
2. The web interface shows recognized faces and attendance status
3. You can view attendance history through the interface

**Note:** Make sure both servers are running (use `START_SERVERS.bat`)

---

## Method 3: Via API (Using Browser or Tools)

### Get Attendance by Student Roll Number
```
GET http://localhost:3001/api/attendance/student/ADRLIM301
```

**Example in browser:**
- Open: http://localhost:3001/api/attendance/student/ADRLIM301

### Get Attendance by Date
```
GET http://localhost:3001/api/attendance/date/2026-01-30
```

**Example in browser:**
- Open: http://localhost:3001/api/attendance/date/2026-01-30

### Get Attendance by Room
```
GET http://localhost:3001/api/attendance/room/Lab-101
```

**Example in browser:**
- Open: http://localhost:3001/api/attendance/room/Lab-101

---

## Method 4: Using SQLite Directly

1. **Open SQLite:**
   ```bash
   sqlite3 attendance.db
   ```

2. **View all attendance:**
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

---

## Method 5: Using DB Browser (GUI Tool)

1. Download: https://sqlitebrowser.org/
2. Open `attendance.db`
3. Click "Browse Data" tab
4. Select "attendance" table
5. View all records in a table format

---

## Quick Reference

| Method | Command/URL |
|--------|-------------|
| **Script** | `python scripts/show_attendance.py` |
| **Web Interface** | http://localhost:5000 |
| **API - By Student** | http://localhost:3001/api/attendance/student/{rollNumber} |
| **API - By Date** | http://localhost:3001/api/attendance/date/{YYYY-MM-DD} |
| **API - By Room** | http://localhost:3001/api/attendance/room/{roomName} |

---

## Current Attendance Status

Run `python scripts/show_attendance.py` to see current records!
