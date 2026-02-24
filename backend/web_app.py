from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from recognize_face import FaceRecognizer
import requests
import base64
from io import BytesIO
from PIL import Image
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Initialize face recognizer
recognizer = None
try:
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    model_path = script_dir / 'models'
    print(f"Attempting to load model from: {model_path}")
    print(f"Model file exists: {(model_path / 'lbph_model.yml').exists()}")
    
    # Try loading with increased memory
    import gc
    gc.collect()
    
    recognizer = FaceRecognizer(model_path=str(model_path))
    print("Face recognition model loaded successfully!")
except Exception as e:
    print(f"Error loading face recognition model: {e}")
    import traceback
    traceback.print_exc()
    print("\nNote: Model loading failed. The web interface will work but face recognition will be disabled.")
    recognizer = None

# Backend API URL
BACKEND_URL = "http://localhost:3001"

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """Recognize face from uploaded image"""
    if recognizer is None:
        return jsonify({
            'success': False,
            'message': 'Face recognition model not loaded'
        }), 500
    
    try:
        # Check if image is uploaded
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No image file selected'
            }), 400
        
        # Read image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({
                'success': False,
                'message': 'Invalid image file'
            }), 400
        
        # Recognize faces
        results = recognizer.recognize(image, confidence_threshold=70)
        
        if len(results) == 0:
            return jsonify({
                'success': False,
                'message': 'No face detected in image'
            }), 400
        
        # Get the best match (lowest confidence = best match)
        best_match = min(results, key=lambda x: x[1])
        name, confidence, (x, y, w, h) = best_match
        
        # Get student info from backend
        student_info = None
        if name != "Unknown":
            try:
                response = requests.get(f'{BACKEND_URL}/api/students')
                if response.status_code == 200:
                    students = response.json()['data']
                    student_info = next((s for s in students if s['name'] == name), None)
            except Exception as e:
                print(f"Error fetching student info: {e}")
        
        return jsonify({
            'success': True,
            'recognized': {
                'name': name,
                'confidence': float(confidence),
                'face_location': {
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h)
                }
            },
            'student': student_info,
            'all_detections': [
                {
                    'name': n,
                    'confidence': float(c),
                    'location': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
                }
                for n, c, (x, y, w, h) in results
            ]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing image: {str(e)}'
        }), 500

@app.route('/api/mark-attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance for a recognized student"""
    try:
        data = request.json
        student_id = data.get('studentId')
        
        if not student_id:
            return jsonify({
                'success': False,
                'message': 'Student ID is required'
            }), 400
        
        # Prepare attendance data
        from datetime import datetime
        attendance_data = {
            'studentId': student_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'room': data.get('room', 'Default Room'),
            'status': 'Present'
        }
        
        # Only include latitude/longitude if they are valid numbers
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is not None and latitude != '':
            try:
                lat_float = float(latitude)
                if -90 <= lat_float <= 90:
                    attendance_data['latitude'] = lat_float
            except (ValueError, TypeError):
                pass  # Skip invalid latitude
        
        if longitude is not None and longitude != '':
            try:
                lng_float = float(longitude)
                if -180 <= lng_float <= 180:
                    attendance_data['longitude'] = lng_float
            except (ValueError, TypeError):
                pass  # Skip invalid longitude
        
        # Mark attendance via backend API
        response = requests.post(
            f'{BACKEND_URL}/api/attendance',
            json=attendance_data
        )
        
        if response.status_code == 201:
            return jsonify({
                'success': True,
                'message': 'Attendance marked successfully',
                'data': response.json()
            })
        else:
            error_msg = 'Failed to mark attendance'
            error_details = []
            try:
                error_data = response.json()
                error_msg = error_data.get('message', error_data.get('error', error_msg))
                
                # Get validation errors if present
                if 'errors' in error_data:
                    error_details = [err.get('msg', '') for err in error_data['errors']]
                    if error_details:
                        error_msg = 'Validation failed: ' + '; '.join(error_details)
            except:
                error_msg = f'HTTP {response.status_code}: {response.text[:100]}'
            
            return jsonify({
                'success': False,
                'message': error_msg,
                'status_code': response.status_code,
                'errors': error_details if error_details else None
            }), response.status_code
    
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'message': 'Cannot connect to backend server. Make sure it is running on http://localhost:3001'
        }), 503
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'message': f'Request error: {str(e)}'
        }), 500
    except Exception as e:
        import traceback
        print(f"Error in mark_attendance: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error marking attendance: {str(e)}'
        }), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students from backend"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/students')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching students: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Face recognition service is running',
        'model_loaded': recognizer is not None
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Face Recognition Web Service")
    print("=" * 60)
    print(f"Backend API: {BACKEND_URL}")
    print("Starting server on http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
