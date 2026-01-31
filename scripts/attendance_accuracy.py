import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / 'attendance.db'

def check_accuracy():
    """Check attendance accuracy and correctness"""
    
    if not DB_PATH.exists():
        print(f"Database not found at: {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ATTENDANCE ACCURACY ANALYSIS")
    print("=" * 80)
    
    # Get all attendance records with student info
    cursor.execute("""
        SELECT 
            a.id,
            a.studentId,
            s.name,
            s.rollNumber,
            a.date,
            a.time,
            a.room,
            a.status,
            a.createdAt
        FROM attendance a
        JOIN students s ON a.studentId = s.id
        ORDER BY a.createdAt DESC
    """)
    
    records = cursor.fetchall()
    
    if len(records) == 0:
        print("\nNo attendance records found.")
        conn.close()
        return
    
    print(f"\nTotal Records Analyzed: {len(records)}\n")
    
    # Check for issues
    issues = []
    correct_records = 0
    
    for record in records:
        record_id, student_id, name, roll, date, time, room, status, created = record
        is_correct = True
        
        # Check 1: Valid student ID
        if student_id is None or student_id <= 0:
            issues.append(f"Record {record_id}: Invalid student ID")
            is_correct = False
        
        # Check 2: Valid date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except:
            issues.append(f"Record {record_id}: Invalid date format: {date}")
            is_correct = False
        
        # Check 3: Valid time format
        try:
            datetime.strptime(time, '%H:%M:%S')
        except:
            issues.append(f"Record {record_id}: Invalid time format: {time}")
            is_correct = False
        
        # Check 4: Room not empty
        if not room or room.strip() == '':
            issues.append(f"Record {record_id}: Empty room field")
            is_correct = False
        
        # Check 5: Valid status
        if status not in ['Present', 'Absent', 'Late']:
            issues.append(f"Record {record_id}: Invalid status: {status}")
            is_correct = False
        
        if is_correct:
            correct_records += 1
    
    # Calculate accuracy
    accuracy = (correct_records / len(records) * 100) if len(records) > 0 else 0
    
    print("=" * 80)
    print("ACCURACY RESULTS")
    print("=" * 80)
    print(f"Total Records:        {len(records)}")
    print(f"Correct Records:      {correct_records}")
    print(f"Incorrect Records:    {len(records) - correct_records}")
    print(f"Accuracy Rate:        {accuracy:.2f}%")
    
    if issues:
        print(f"\n⚠️  ISSUES FOUND: {len(issues)}")
        print("-" * 80)
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
    else:
        print(f"\nALL RECORDS ARE CORRECT!")
    
    # Data quality metrics
    print(f"\nDATA QUALITY METRICS")
    print("-" * 80)
    
    # Check for duplicates (same student, same date)
    cursor.execute("""
        SELECT studentId, date, COUNT(*) as count
        FROM attendance
        GROUP BY studentId, date
        HAVING count > 1
    """)
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"WARNING: Duplicate Records Found: {len(duplicates)}")
        for student_id, date, count in duplicates:
            cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
            name = cursor.fetchone()[0]
            print(f"  - {name} has {count} records on {date}")
    else:
        print(f"OK: No duplicate records (good!)")
    
    # Check for future dates
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date > ?", (today,))
    future_records = cursor.fetchone()[0]
    
    if future_records > 0:
        print(f"WARNING: Future-dated records: {future_records}")
    else:
        print(f"OK: No future-dated records")
    
    # Check for very old records
    from datetime import timedelta
    old_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date < ?", (old_date,))
    old_records = cursor.fetchone()[0]
    
    if old_records > 0:
        print(f"INFO: Records older than 1 year: {old_records}")
    
    conn.close()
    print("\n" + "=" * 80)

if __name__ == '__main__':
    check_accuracy()
