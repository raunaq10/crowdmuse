# API Usage Examples

## Base URL
```
http://localhost:3000/api
```

## 1. Register a Student

**Endpoint:** `POST /api/students`

**Content-Type:** `multipart/form-data`

**Body:**
- `name`: String (required)
- `rollNumber`: String (required, unique)
- `year`: String (required, e.g., "1st", "2nd", "3rd", "4th")
- `stream`: String (required, e.g., "Computer Science", "Electrical Engineering")
- `photos`: File[] (required, at least 1 image, max 10 images)

**Example using cURL:**
```bash
curl -X POST http://localhost:3000/api/students \
  -F "name=John Doe" \
  -F "rollNumber=CS2024001" \
  -F "year=2nd" \
  -F "stream=Computer Science" \
  -F "photos=@/path/to/image1.jpg" \
  -F "photos=@/path/to/image2.jpg"
```

**Response:**
```json
{
  "success": true,
  "message": "Student registered successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "rollNumber": "CS2024001",
    "year": "2nd",
    "stream": "Computer Science",
    "photos": ["/uploads/CS2024001-1234567890-987654321.jpg", "/uploads/CS2024001-1234567891-987654322.jpg"],
    "createdAt": "2024-01-15 10:30:00",
    "updatedAt": "2024-01-15 10:30:00"
  }
}
```

## 2. Get All Students (for Model Training)

**Endpoint:** `GET /api/students`

**Example:**
```bash
curl http://localhost:3000/api/students
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "rollNumber": "CS2024001",
      "year": "2nd",
      "stream": "Computer Science",
      "photos": ["/uploads/CS2024001-1234567890-987654321.jpg"],
      "createdAt": "2024-01-15 10:30:00",
      "updatedAt": "2024-01-15 10:30:00"
    }
  ]
}
```

## 3. Get Student by Roll Number

**Endpoint:** `GET /api/students/:rollNumber`

**Example:**
```bash
curl http://localhost:3000/api/students/CS2024001
```

## 4. Mark Attendance

**Endpoint:** `POST /api/attendance`

**Content-Type:** `application/json`

**Body:**
```json
{
  "studentId": 1,
  "date": "2024-01-15",
  "time": "09:30:00",
  "room": "Lab-101",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "status": "Present"
}
```

**Example:**
```bash
curl -X POST http://localhost:3000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "studentId": 1,
    "date": "2024-01-15",
    "time": "09:30:00",
    "room": "Lab-101",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "status": "Present"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Attendance marked successfully",
  "data": {
    "id": 1,
    "studentId": 1,
    "name": "John Doe",
    "rollNumber": "CS2024001",
    "date": "2024-01-15",
    "time": "09:30:00",
    "room": "Lab-101",
    "geoLocation": {
      "lat": 28.6139,
      "lng": 77.2090
    },
    "status": "Present",
    "createdAt": "2024-01-15 09:30:00"
  }
}
```

**Note:** Duplicate attendance for the same student on the same date will return a 409 error.

## 5. Get Attendance by Roll Number

**Endpoint:** `GET /api/attendance/student/:rollNumber`

**Example:**
```bash
curl http://localhost:3000/api/attendance/student/CS2024001
```

**Response:**
```json
{
  "success": true,
  "student": {
    "name": "John Doe",
    "rollNumber": "CS2024001",
    "year": "2nd",
    "stream": "Computer Science"
  },
  "count": 5,
  "data": [
    {
      "id": 1,
      "studentId": 1,
      "name": "John Doe",
      "rollNumber": "CS2024001",
      "date": "2024-01-15",
      "time": "09:30:00",
      "room": "Lab-101",
      "geoLocation": {
        "lat": 28.6139,
        "lng": 77.2090
      },
      "status": "Present"
    }
  ]
}
```

## 6. Get Attendance by Date

**Endpoint:** `GET /api/attendance/date/:date`

**Date Format:** `YYYY-MM-DD`

**Example:**
```bash
curl http://localhost:3000/api/attendance/date/2024-01-15
```

## 7. Get Attendance by Room

**Endpoint:** `GET /api/attendance/room/:room`

**Example:**
```bash
curl http://localhost:3000/api/attendance/room/Lab-101
```

## Error Responses

All error responses follow this format:
```json
{
  "success": false,
  "message": "Error description",
  "errors": [
    {
      "msg": "Validation error message",
      "param": "fieldName",
      "location": "body"
    }
  ]
}
```

## Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `409` - Conflict (duplicate entry)
- `500` - Internal Server Error
