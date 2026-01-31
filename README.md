# Student Attendance System with Face Recognition

A complete backend system for managing student attendance using face recognition technology. Built with Node.js/Express backend and OpenCV-based face recognition (LBPH + Haar Cascade).

## 🚀 Features

- **Student Registration**: Register students with multiple face images
- **Face Recognition**: LBPH-based face recognition with Haar Cascade detection
- **Attendance Management**: Mark attendance with duplicate prevention
- **Reports & Queries**: Get attendance by student, date, or room
- **RESTful API**: Clean API design with proper validation
- **Web Interface**: Flask-based web app for face recognition

## 📋 Prerequisites

- Node.js (v14 or higher)
- Python 3.7+
- npm

## 🛠️ Installation

### Backend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the backend server:
```bash
npm start
```

Server runs on `http://localhost:3001`

### Face Recognition Setup

1. Install Python dependencies:
```bash
cd face_recognition
pip install -r requirements.txt
```

2. Train the model (if you have a dataset):
```bash
python train_model.py
```

3. Start the web interface:
```bash
python web_app.py
```

Web interface runs on `http://localhost:5000`

## 📁 Project Structure

```
attendance-system/
├── config/           # Database configuration
├── controllers/      # Business logic
├── models/          # Data models
├── routes/          # API routes
├── middleware/      # Validation & upload
├── face_recognition/ # Face recognition module
│   ├── train_model.py
│   ├── recognize_face.py
│   └── web_app.py
├── scripts/         # Utility scripts
└── server.js        # Main server file
```

## 📡 API Endpoints

### Students
- `POST /api/students` - Register student (multipart/form-data)
- `GET /api/students` - Get all students
- `GET /api/students/:rollNumber` - Get student by roll number

### Attendance
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/student/:rollNumber` - Get by student
- `GET /api/attendance/date/:date` - Get by date
- `GET /api/attendance/room/:room` - Get by room

See `API_EXAMPLES.md` for detailed examples.

## 🗄️ Database

SQLite database (`attendance.db`) is automatically created with:
- `students` table
- `attendance` table

## 🤖 Face Recognition

- **Algorithm**: LBPH (Local Binary Patterns Histograms)
- **Detection**: Haar Cascade
- **Training**: Use `face_recognition/train_model.py`
- **Recognition**: Use `face_recognition/recognize_face.py` or web interface

## 📊 Scripts

- `scripts/bulkImport.js` - Import dataset into database
- `scripts/show_attendance.py` - View attendance records
- `scripts/attendance_efficiency.py` - Check efficiency metrics
- `scripts/compare_training_datasets.py` - Compare dataset configurations

## 🚀 Quick Start

1. Clone the repository
2. Run `npm install`
3. Run `npm start` (backend)
4. Run `python face_recognition/web_app.py` (web interface)
5. Open `http://localhost:5000`

## 📝 License

ISC
