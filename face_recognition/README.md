# Face Recognition Training Module

This module trains and uses a face recognition model using OpenCV's LBPH (Local Binary Patterns Histograms) face recognizer with Haar Cascade for face detection.

## Setup

1. Install required Python packages:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install opencv-python opencv-contrib-python numpy
```

**Note:** `opencv-contrib-python` is required for the LBPH face recognizer.

## Training

Train the model using your dataset:

```bash
python train_model.py
```

The script will:
- Load all images from `../dataset/` folder
- Detect faces using Haar Cascade
- Train LBPH recognizer on detected faces
- Save the model to `models/` folder

### Training Output

After training, you'll find:
- `models/lbph_model.yml` - Trained model file
- `models/label_mappings.pkl` - Label to name mappings (binary)
- `models/label_mappings.txt` - Human-readable label mappings

## Usage

### Recognize from Image File

```bash
python recognize_face.py path/to/image.jpg
```

### Real-time Recognition from Camera

```bash
python recognize_face.py
```

Press 'q' to quit the camera view.

### Using in Your Code

```python
from recognize_face import FaceRecognizer

# Initialize recognizer
recognizer = FaceRecognizer()

# Recognize from image file
results = recognizer.recognize_from_file('test_image.jpg')

for name, confidence, (x, y, w, h) in results:
    print(f"Found: {name} (confidence: {confidence:.2f})")
    
    # Use the name to get student ID from backend API
    # Then mark attendance via POST /api/attendance
```

## Integration with Backend

After recognizing a face, you can:

1. Get student ID from backend using roll number or name
2. Mark attendance via API:

```python
import requests

# After recognition
recognized_name = "Adriana Lima"  # From face recognition

# Get student from backend
response = requests.get(f'http://localhost:3001/api/students')
students = response.json()['data']

# Find student by name
student = next((s for s in students if s['name'] == recognized_name), None)

if student:
    # Mark attendance
    attendance_data = {
        'studentId': student['id'],
        'date': '2026-01-23',
        'time': '10:30:00',
        'room': 'Lab-101',
        'status': 'Present'
    }
    requests.post('http://localhost:3001/api/attendance', json=attendance_data)
```

## Model Parameters

The LBPH recognizer is configured with:
- **Radius**: 1
- **Neighbors**: 8
- **Grid**: 8x8

You can adjust these in `train_model.py` if needed.

## Troubleshooting

### No faces detected
- Check if images contain clear frontal faces
- Adjust `minSize` parameter in `detect_face()` method
- Ensure good lighting in images

### Low recognition accuracy
- Train with more images per person (recommended: 10+ images)
- Ensure images have good quality and lighting
- Adjust `confidence_threshold` in recognition

### Module not found errors
- Make sure you're in the `face_recognition/` directory
- Or use: `python -m face_recognition.train_model`
