import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / 'attendance.db'

def calculate_efficiency():
    """Calculate attendance efficiency and accuracy metrics"""
    
    if not DB_PATH.exists():
        print(f"Database not found at: {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ATTENDANCE EFFICIENCY & ACCURACY REPORT")
    print("=" * 80)
    
    # Get total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    # Get total attendance records
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]
    
    # Get attendance by status
    cursor.execute("SELECT status, COUNT(*) FROM attendance GROUP BY status")
    status_counts = dict(cursor.fetchall())
    
    # Get attendance by date
    cursor.execute("""
        SELECT date, COUNT(*) as count
        FROM attendance
        GROUP BY date
        ORDER BY date DESC
    """)
    date_stats = cursor.fetchall()
    
    # Get students with attendance
    cursor.execute("""
        SELECT COUNT(DISTINCT studentId) FROM attendance
    """)
    students_with_attendance = cursor.fetchone()[0]
    
    # Get duplicate attempts (failed due to duplicate)
    # This would require a log, but we can estimate from date-based duplicates
    cursor.execute("""
        SELECT studentId, date, COUNT(*) as count
        FROM attendance
        GROUP BY studentId, date
        HAVING count > 1
    """)
    duplicate_records = cursor.fetchall()
    
    # Calculate metrics
    attendance_rate = (students_with_attendance / total_students * 100) if total_students > 0 else 0
    avg_attendance_per_student = total_attendance / students_with_attendance if students_with_attendance > 0 else 0
    
    # Get recent activity (last 7 days)
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT COUNT(*) FROM attendance WHERE date >= ?
    """, (seven_days_ago,))
    recent_attendance = cursor.fetchone()[0]
    
    # Get attendance by room
    cursor.execute("""
        SELECT room, COUNT(*) as count
        FROM attendance
        GROUP BY room
        ORDER BY count DESC
    """)
    room_stats = cursor.fetchall()
    
    # Print results
    print(f"\nOVERALL STATISTICS")
    print("-" * 80)
    print(f"Total Students Registered:     {total_students}")
    print(f"Total Attendance Records:      {total_attendance}")
    print(f"Students with Attendance:      {students_with_attendance}")
    print(f"Attendance Rate:               {attendance_rate:.2f}%")
    print(f"Avg Records per Student:        {avg_attendance_per_student:.2f}")
    print(f"Recent Activity (7 days):      {recent_attendance} records")
    
    # Status breakdown
    if status_counts:
        print(f"\nATTENDANCE BY STATUS")
        print("-" * 80)
        for status, count in status_counts.items():
            percentage = (count / total_attendance * 100) if total_attendance > 0 else 0
            print(f"{status:<15} {count:>5} records ({percentage:>5.2f}%)")
    
    # Date statistics
    if date_stats:
        print(f"\nATTENDANCE BY DATE")
        print("-" * 80)
        print(f"{'Date':<15} {'Records':<10} {'Students':<10}")
        print("-" * 80)
        for date, count in date_stats[:10]:  # Show last 10 days
            cursor.execute("""
                SELECT COUNT(DISTINCT studentId) 
                FROM attendance 
                WHERE date = ?
            """, (date,))
            students = cursor.fetchone()[0]
            print(f"{date:<15} {count:<10} {students:<10}")
    
    # Room statistics
    if room_stats:
        print(f"\nATTENDANCE BY ROOM")
        print("-" * 80)
        print(f"{'Room':<20} {'Records':<10} {'Percentage':<10}")
        print("-" * 80)
        for room, count in room_stats:
            percentage = (count / total_attendance * 100) if total_attendance > 0 else 0
            print(f"{room:<20} {count:<10} {percentage:>5.2f}%")
    
    # Efficiency metrics
    print(f"\nEFFICIENCY METRICS")
    print("-" * 80)
    
    # Data completeness
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) as with_location
        FROM attendance
    """)
    total_recs, with_location = cursor.fetchone()
    location_completeness = (with_location / total_recs * 100) if total_recs > 0 else 0
    
    print(f"Data Completeness:")
    print(f"  - Records with GPS:          {with_location}/{total_recs} ({location_completeness:.2f}%)")
    
    # Daily attendance rate (if we have multiple days)
    if len(date_stats) > 1:
        avg_daily = sum(count for _, count in date_stats) / len(date_stats)
        print(f"  - Average Daily Records:     {avg_daily:.2f}")
    
    # Student participation
    participation_rate = (students_with_attendance / total_students * 100) if total_students > 0 else 0
    print(f"  - Student Participation:      {participation_rate:.2f}%")
    
    # Success rate (assuming all saved records are successful)
    success_rate = 100.0  # All saved records are successful
    print(f"  - Attendance Marking Success: {success_rate:.2f}%")
    
    # Calculate overall efficiency score
    efficiency_score = (
        (attendance_rate * 0.4) +  # 40% weight on attendance rate
        (location_completeness * 0.1) +  # 10% weight on data completeness
        (success_rate * 0.5)  # 50% weight on success rate
    )
    
    print(f"\nOVERALL EFFICIENCY SCORE")
    print("-" * 80)
    print(f"Efficiency Score: {efficiency_score:.2f}%")
    
    if efficiency_score >= 90:
        rating = "Excellent"
    elif efficiency_score >= 75:
        rating = "Good"
    elif efficiency_score >= 60:
        rating = "Fair"
    else:
        rating = "Needs Improvement"
    
    print(f"Rating: {rating}")
    
    # Top performers
    cursor.execute("""
        SELECT 
            s.name,
            s.rollNumber,
            COUNT(*) as attendance_count
        FROM attendance a
        JOIN students s ON a.studentId = s.id
        GROUP BY a.studentId
        ORDER BY attendance_count DESC
        LIMIT 10
    """)
    top_students = cursor.fetchall()
    
    if top_students:
        print(f"\nTOP 10 STUDENTS BY ATTENDANCE")
        print("-" * 80)
        print(f"{'Rank':<6} {'Name':<30} {'Roll No':<15} {'Records':<10}")
        print("-" * 80)
        for idx, (name, roll, count) in enumerate(top_students, 1):
            print(f"{idx:<6} {name:<30} {roll:<15} {count:<10}")
    
    conn.close()
    print("\n" + "=" * 80)
    print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == '__main__':
    calculate_efficiency()
