import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'attendance.db'

def add_test_record():
    """Add a test attendance record"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get first student
    cursor.execute('SELECT id, name, rollNumber FROM students LIMIT 1')
    student = cursor.fetchone()
    
    if not student:
        print("No students found in database!")
        conn.close()
        return
    
    # Insert test attendance
    cursor.execute("""
        INSERT INTO attendance (studentId, date, time, room, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student[0],
        datetime.now().strftime('%Y-%m-%d'),
        datetime.now().strftime('%H:%M:%S'),
        'Lab-101',
        'Present'
    ))
    
    conn.commit()
    print(f"Test attendance record created for: {student[1]} ({student[2]})")
    conn.close()

if __name__ == '__main__':
    add_test_record()
