# ATTENDANCE DATABASE GUIDE

## Database Location
**File Path:** `C:\Users\singh\OneDrive\Desktop\attendance system\attendance.db`

## ATTENDANCE TABLE STRUCTURE

The attendance records are stored in the `attendance` table with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `studentId` | INTEGER | Foreign key to students table |
| `date` | TEXT | Date in YYYY-MM-DD format |
| `time` | TEXT | Time in HH:MM:SS format |
| `room` | TEXT | Room/classroom identifier |
| `latitude` | REAL | Optional GPS latitude |
| `longitude` | REAL | Optional GPS longitude |
| `status` | TEXT | Attendance status (Present/Absent/Late) |
| `createdAt` | DATETIME | Timestamp when record was created |

## How to View Attendance Data

### Method 1: Using Python Script
```bash
python scripts/view_attendance.py
```

### Method 2: Using SQLite Command Line
```bash
sqlite3 attendance.db
```

Then run:
```sql
-- View all attendance records
SELECT * FROM attendance;

-- View with student names
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

### Method 3: Using DB Browser for SQLite
1. Download: https://sqlitebrowser.org/
2. Open `attendance.db`
3. Go to "Browse Data" tab
4. Select "attendance" table

### Method 4: Using API
```bash
# Get attendance by roll number
GET http://localhost:3001/api/attendance/student/{rollNumber}

# Get attendance by date
GET http://localhost:3001/api/attendance/date/2026-01-23

# Get attendance by room
GET http://localhost:3001/api/attendance/room/Lab-101
```

## How Attendance Gets Saved

When attendance is marked (via web interface or API), the data is saved to:
- **Table:** `attendance`
- **Database:** `attendance.db`
- **Location:** Project root folder

### Example Record
```json
{
  "id": 1,
  "studentId": 1,
  "date": "2026-01-23",
  "time": "10:30:00",
  "room": "Lab-101",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "status": "Present",
  "createdAt": "2026-01-23 10:30:00"
}
```

## Current Status
- **Total Students:** 105
- **Total Attendance Records:** 0 (none marked yet)

## To Mark Attendance

1. **Via Web Interface:**
   - Open: http://localhost:5000
   - Upload student image
   - Click "Mark Attendance"

2. **Via API:**
   ```bash
   POST http://localhost:3001/api/attendance
   {
     "studentId": 1,
     "date": "2026-01-23",
     "time": "10:30:00",
     "room": "Lab-101",
     "status": "Present"
   }
   ```

## SQL Queries

See `scripts/query_attendance.sql` for ready-to-use SQL queries.
