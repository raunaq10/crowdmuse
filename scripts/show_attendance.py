import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'attendance.db'

def show_attendance_table():
    """Show the attendance table in a readable format"""
    
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 100)
    print("ATTENDANCE TABLE - ALL RECORDS")
    print("=" * 100)
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'")
    if not cursor.fetchone():
        print("ERROR: Attendance table does not exist!")
        conn.close()
        return
    
    # Get all records with student names
    cursor.execute("""
        SELECT 
            a.id,
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
        LEFT JOIN students s ON a.studentId = s.id
        ORDER BY a.createdAt DESC
    """)
    
    records = cursor.fetchall()
    
    if len(records) == 0:
        print("\nNO ATTENDANCE RECORDS FOUND")
        print("\nThe attendance table is empty.")
        print("Mark some attendance first using:")
        print("  - Web interface: http://localhost:5000")
        print("  - API: POST http://localhost:3001/api/attendance")
    else:
        print(f"\nTotal Records: {len(records)}\n")
        print(f"{'ID':<5} {'Student Name':<30} {'Roll No':<15} {'Date':<12} {'Time':<10} {'Room':<15} {'Status':<10}")
        print("-" * 100)
        
        for r in records:
            student_name = r[1] if r[1] else f"Student ID: {r[0]}"
            roll_no = r[2] if r[2] else "N/A"
            geo = f"({r[6]:.4f},{r[7]:.4f})" if r[6] and r[7] else ""
            
            print(f"{r[0]:<5} {student_name:<30} {roll_no:<15} {r[3]:<12} {r[4]:<10} {r[5]:<15} {r[8]:<10}")
            if geo:
                print(f"      Location: {geo}")
    
    conn.close()
    print("\n" + "=" * 100)
    print(f"Database: {DB_PATH}")
    print("=" * 100)

if __name__ == '__main__':
    show_attendance_table()
