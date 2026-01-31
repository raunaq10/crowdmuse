import sqlite3
from pathlib import Path
import json
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent.parent / 'attendance.db'

def view_database():
    """View database contents"""
    if not DB_PATH.exists():
        print(f"Database not found at: {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 60)
    print("ATTENDANCE SYSTEM DATABASE")
    print("=" * 60)
    print(f"Database Location: {DB_PATH}")
    print(f"File Size: {DB_PATH.stat().st_size / 1024:.2f} KB")
    print(f"Last Modified: {datetime.fromtimestamp(DB_PATH.stat().st_mtime)}")
    print("=" * 60)
    
    # Get table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables: {', '.join([t[0] for t in tables])}\n")
    
    # Students count
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    print(f"Total Students: {student_count}")
    
    # Attendance count
    cursor.execute("SELECT COUNT(*) FROM attendance")
    attendance_count = cursor.fetchone()[0]
    print(f"Total Attendance Records: {attendance_count}\n")
    
    # Show sample students
    print("=" * 60)
    print("SAMPLE STUDENTS (First 10)")
    print("=" * 60)
    cursor.execute("""
        SELECT id, name, rollNumber, year, stream, 
               (SELECT COUNT(*) FROM json_each(photos)) as photo_count,
               createdAt 
        FROM students 
        ORDER BY id 
        LIMIT 10
    """)
    
    students = cursor.fetchall()
    for s in students:
        print(f"ID: {s[0]:<4} | {s[1]:<25} | Roll: {s[2]:<12} | Year: {s[3]:<6} | Photos: {s[5]}")
    
    # Show sample attendance
    if attendance_count > 0:
        print("\n" + "=" * 60)
        print("SAMPLE ATTENDANCE RECORDS (First 10)")
        print("=" * 60)
        cursor.execute("""
            SELECT a.id, s.name, s.rollNumber, a.date, a.time, a.room, a.status
            FROM attendance a
            JOIN students s ON a.studentId = s.id
            ORDER BY a.createdAt DESC
            LIMIT 10
        """)
        
        records = cursor.fetchall()
        for r in records:
            print(f"ID: {r[0]:<4} | {r[1]:<25} ({r[2]}) | {r[3]} {r[4]} | Room: {r[5]} | {r[6]}")
    else:
        print("\nNo attendance records yet.")
    
    # Statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    
    # Students by year
    cursor.execute("SELECT year, COUNT(*) FROM students GROUP BY year")
    year_stats = cursor.fetchall()
    print("\nStudents by Year:")
    for year, count in year_stats:
        print(f"  {year}: {count}")
    
    # Students by stream
    cursor.execute("SELECT stream, COUNT(*) FROM students GROUP BY stream")
    stream_stats = cursor.fetchall()
    print("\nStudents by Stream:")
    for stream, count in stream_stats:
        print(f"  {stream}: {count}")
    
    # Attendance by date
    if attendance_count > 0:
        cursor.execute("SELECT date, COUNT(*) FROM attendance GROUP BY date ORDER BY date DESC LIMIT 5")
        date_stats = cursor.fetchall()
        print("\nRecent Attendance by Date:")
        for date, count in date_stats:
            print(f"  {date}: {count} records")
    
    conn.close()
    print("\n" + "=" * 60)
    print(f"Database file: {DB_PATH}")
    print("=" * 60)

if __name__ == '__main__':
    view_database()
