const express = require('express');
const router = express.Router();
const studentController = require('../controllers/studentController');
const upload = require('../middleware/upload');
const { validateStudentRegistration } = require('../middleware/validation');

// Register a new student with image upload
router.post(
  '/',
  upload.array('photos', 10), // Allow up to 10 images
  validateStudentRegistration,
  studentController.registerStudent
);

// Get all students (for model training)
router.get('/', studentController.getAllStudents);

// Get student by roll number
router.get('/:rollNumber', studentController.getStudentByRollNumber);

module.exports = router;
