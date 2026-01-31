const express = require('express');
const router = express.Router();
const attendanceController = require('../controllers/attendanceController');
const { validateAttendance } = require('../middleware/validation');

// Mark attendance for a recognized student
router.post(
  '/',
  validateAttendance,
  attendanceController.markAttendance
);

// Get attendance history by roll number
router.get('/student/:rollNumber', attendanceController.getAttendanceByRollNumber);

// Get attendance records by date
router.get('/date/:date', attendanceController.getAttendanceByDate);

// Get attendance records by room
router.get('/room/:room', attendanceController.getAttendanceByRoom);

module.exports = router;
