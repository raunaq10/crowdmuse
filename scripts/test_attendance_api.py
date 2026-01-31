import requests
import json
from datetime import datetime

BACKEND_URL = "http://localhost:3001"

def test_mark_attendance():
    """Test marking attendance via API"""
    print("=" * 60)
    print("TESTING ATTENDANCE API")
    print("=" * 60)
    
    # Get first student
    try:
        response = requests.get(f"{BACKEND_URL}/api/students")
        if response.status_code != 200:
            print(f"Error: Cannot get students - {response.status_code}")
            return
        
        students = response.json()['data']
        if len(students) == 0:
            print("No students found!")
            return
        
        student = students[0]
        print(f"Testing with student: {student['name']} (ID: {student['id']})")
        
        # Try to mark attendance
        attendance_data = {
            'studentId': student['id'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'room': 'Test-Room',
            'status': 'Present'
        }
        
        print(f"\nSending attendance data:")
        print(json.dumps(attendance_data, indent=2))
        
        response = requests.post(
            f"{BACKEND_URL}/api/attendance",
            json=attendance_data
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("\nSUCCESS: Attendance marked!")
        elif response.status_code == 409:
            print("\nNOTE: Attendance already marked for this student today (duplicate)")
        else:
            print(f"\nERROR: Failed to mark attendance")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend server!")
        print("Make sure backend is running: node server.js")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_mark_attendance()
