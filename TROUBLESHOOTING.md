# TROUBLESHOOTING: "Failed to mark attendance"

## Common Issues and Solutions

### Issue 1: Duplicate Attendance (Most Common)

**Error:** "Attendance already marked for this student on this date"

**Cause:** You're trying to mark attendance for a student who already has attendance marked today.

**Solution:**
- Try a different student
- Wait until tomorrow (attendance is per day)
- Or delete the existing record if it was a mistake

**Check who's already marked:**
```bash
python scripts/show_attendance.py
```

---

### Issue 2: Web App Not Running

**Error:** "Failed to mark attendance" or connection errors

**Cause:** The Flask web app (port 5000) is not running.

**Solution:**
1. Run `START_SERVERS.bat` (double-click it)
2. Or manually start:
   ```bash
   cd face_recognition
   python web_app.py
   ```

**Check if running:**
- Open: http://localhost:5000/health
- Should show: `{"success": true, "model_loaded": true}`

---

### Issue 3: Backend API Not Running

**Error:** "Cannot connect to backend server"

**Cause:** The Node.js backend (port 3001) is not running.

**Solution:**
1. Run `START_SERVERS.bat` (double-click it)
2. Or manually start:
   ```bash
   node server.js
   ```

**Check if running:**
- Open: http://localhost:3001/health
- Should show: `{"success": true, "message": "Server is running"}`

---

### Issue 4: Student Not Found

**Error:** "Student not found"

**Cause:** The recognized face doesn't match any student in the database.

**Solution:**
- Make sure the student is registered in the system
- Check: http://localhost:3001/api/students
- Re-train the model if needed

---

## Quick Fix Checklist

1. ✅ **Both servers running?**
   - Backend: http://localhost:3001/health
   - Web App: http://localhost:5000/health

2. ✅ **Student already marked today?**
   - Run: `python scripts/show_attendance.py`
   - Check if student appears in today's records

3. ✅ **Student exists in database?**
   - Check: http://localhost:3001/api/students

4. ✅ **Face recognition working?**
   - Upload image at http://localhost:5000
   - Should recognize the student name

---

## How to Test

1. **Test Backend API directly:**
   ```bash
   python scripts/test_attendance_api.py
   ```

2. **View current attendance:**
   ```bash
   python scripts/show_attendance.py
   ```

3. **Check servers:**
   - Backend: http://localhost:3001/health
   - Web App: http://localhost:5000/health

---

## Error Messages Explained

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| "Attendance already marked" | Duplicate for today | Try different student or wait |
| "Cannot connect to backend" | Backend not running | Start backend server |
| "Student not found" | Student not in database | Register student first |
| "No face detected" | Image has no face | Use better quality image |
