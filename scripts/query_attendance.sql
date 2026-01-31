-- SQL Queries to view attendance data
-- Run these in any SQLite browser or command line

-- View all attendance records with student details
SELECT 
    a.id AS attendance_id,
    s.id AS student_id,
    s.name AS student_name,
    s.rollNumber,
    a.date,
    a.time,
    a.room,
    a.latitude,
    a.longitude,
    a.status,
    a.createdAt
FROM attendance a
JOIN students s ON a.studentId = s.id
ORDER BY a.createdAt DESC;

-- Count attendance by date
SELECT date, COUNT(*) as count
FROM attendance
GROUP BY date
ORDER BY date DESC;

-- Count attendance by room
SELECT room, COUNT(*) as count
FROM attendance
GROUP BY room
ORDER BY count DESC;

-- Count attendance by student
SELECT 
    s.name,
    s.rollNumber,
    COUNT(*) as attendance_count
FROM attendance a
JOIN students s ON a.studentId = s.id
GROUP BY a.studentId
ORDER BY attendance_count DESC;

-- View attendance for a specific student by roll number
SELECT 
    a.date,
    a.time,
    a.room,
    a.status
FROM attendance a
JOIN students s ON a.studentId = s.id
WHERE s.rollNumber = 'ADRLIM301'  -- Replace with actual roll number
ORDER BY a.date DESC;

-- View attendance for a specific date
SELECT 
    s.name,
    s.rollNumber,
    a.time,
    a.room,
    a.status
FROM attendance a
JOIN students s ON a.studentId = s.id
WHERE a.date = '2026-01-23'  -- Replace with actual date
ORDER BY a.time;
