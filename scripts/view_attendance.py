import sqlite3
from pathlib import Path
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent.parent / 'attendance.db'

def view_attendance():
    """View all attendance records"""
    if not DB_PATH.exists():
        print(f"Database not found at: {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ATTENDANCE RECORDS DATABASE")
    print("=" * 80)
    print(f"Database Location: {DB_PATH}")
    print("=" * 80)
    
    # Check if attendance table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'")
    if not cursor.fetchone():
        print("ERROR: Attendance table does not exist!")
        conn.close()
        return
    
    # Get table structure
    cursor.execute("PRAGMA table_info(attendance)")
    columns = cursor.fetchall()
    print("\nATTENDANCE TABLE STRUCTURE:")
    print("-" * 80)
    for col in columns:
        print(f"  {col[1]:<15} | Type: {col[2]:<15} | Nullable: {not col[3]}")
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM attendance")
    count = cursor.fetchone()[0]
    print(f"\nTotal Attendance Records: {count}")
    
    if count == 0:
        print("\n" + "=" * 80)
        print("NO ATTENDANCE RECORDS FOUND")
        print("=" * 80)
        print("\nTo mark attendance:")
        print("1. Use the web interface: http://localhost:5000")
        print("2. Use the API: POST http://localhost:3001/api/attendance")
        print("3. Recognize a face and mark attendance through the web app")
    else:
        # Show all attendance records with student info
        print("\n" + "=" * 80)
        print("ALL ATTENDANCE RECORDS")
        print("=" * 80)
        
        cursor.execute("""
            SELECT 
                a.id,
                a.studentId,
                s.name as student_name,
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
            ORDER BY a.createdAt DESC
        """)
        
        records = cursor.fetchall()
        
        print(f"\n{'ID':<5} {'Student Name':<25} {'Roll No':<12} {'Date':<12} {'Time':<10} {'Room':<15} {'Status':<10}")
        print("-" * 80)
        
        for r in records:
            geo = f"({r[7]:.4f}, {r[8]:.4f})" if r[7] and r[8] else "N/A"
            print(f"{r[0]:<5} {r[2]:<25} {r[3]:<12} {r[4]:<12} {r[5]:<10} {r[6]:<15} {r[9]:<10}")
            if r[7] and r[8]:
                print(f"      Location: {geo}")
        
        # Statistics
        print("\n" + "=" * 80)
        print("ATTENDANCE STATISTICS")
        print("=" * 80)
        
        # By date
        cursor.execute("SELECT date, COUNT(*) FROM attendance GROUP BY date ORDER BY date DESC")
        date_stats = cursor.fetchall()
        print("\nAttendance by Date:")
        for date, count in date_stats:
            print(f"  {date}: {count} records")
        
        # By room
        cursor.execute("SELECT room, COUNT(*) FROM attendance GROUP BY room ORDER BY COUNT(*) DESC")
        room_stats = cursor.fetchall()
        print("\nAttendance by Room:")
        for room, count in room_stats:
            print(f"  {room}: {count} records")
        
        # By student
        cursor.execute("""
            SELECT s.name, s.rollNumber, COUNT(*) as count
            FROM attendance a
            JOIN students s ON a.studentId = s.id
            GROUP BY a.studentId
            ORDER BY count DESC
            LIMIT 10
        """)
        student_stats = cursor.fetchall()
        print("\nTop 10 Students by Attendance Count:")
        for name, roll, count in student_stats:
            print(f"  {name} ({roll}): {count} records")
    
    conn.close()
    print("\n" + "=" * 80)
    print(f"Database file: {DB_PATH}")
    print("=" * 80)

if __name__ == '__main__':
    view_attendance()
