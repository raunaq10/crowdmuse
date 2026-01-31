import requests
import json
from datetime import datetime

# Backend API URL
BACKEND_URL = "http://localhost:3001"

def mark_test_attendance():
    """Mark test attendance records"""
    print("=" * 60)
    print("MARKING TEST ATTENDANCE")
    print("=" * 60)
    
    # Get all students
    try:
        response = requests.get(f"{BACKEND_URL}/api/students")
        if response.status_code != 200:
            print(f"Error fetching students: {response.status_code}")
            return
        
        students = response.json()['data']
        print(f"Found {len(students)} students\n")
        
        # Mark attendance for first 5 students
        test_students = students[:5]
        
        for student in test_students:
            attendance_data = {
                'studentId': student['id'],
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S'),
                'room': 'Lab-101',
                'status': 'Present'
            }
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/attendance",
                    json=attendance_data
                )
                
                if response.status_code == 201:
                    print(f"✓ Marked attendance for: {student['name']} ({student['rollNumber']})")
                else:
                    print(f"✗ Failed for {student['name']}: {response.json().get('message', 'Unknown error')}")
            except Exception as e:
                print(f"✗ Error marking attendance for {student['name']}: {e}")
        
        print("\n" + "=" * 60)
        print("Test attendance marked!")
        print("=" * 60)
        print("\nNow run: python scripts/view_attendance.py")
        print("to see the attendance records in the database.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure the backend server is running on http://localhost:3001")

if __name__ == '__main__':
    mark_test_attendance()
