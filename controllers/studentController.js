const Student = require('../models/Student');
const path = require('path');

// Register a new student with image upload
const registerStudent = async (req, res) => {
  try {
    const { name, rollNumber, year, stream } = req.body;

    // Check if roll number already exists
    const existingStudent = await Student.findByRollNumber(rollNumber);
    if (existingStudent) {
      return res.status(409).json({
        success: false,
        message: 'Student with this roll number already exists'
      });
    }

    // Get uploaded file paths
    const photos = req.files && req.files.length > 0
      ? req.files.map(file => `/uploads/${file.filename}`)
      : [];

    if (photos.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'At least one image is required for registration'
      });
    }

    // Create student
    const student = await Student.create({
      name,
      rollNumber,
      year,
      stream,
      photos
    });

    res.status(201).json({
      success: true,
      message: 'Student registered successfully',
      data: student
    });
  } catch (error) {
    console.error('Error registering student:', error);
    res.status(500).json({
      success: false,
      message: 'Error registering student',
      error: error.message
    });
  }
};

// Get all students (for model training)
const getAllStudents = async (req, res) => {
  try {
    const students = await Student.findAll();
    
    res.json({
      success: true,
      count: students.length,
      data: students
    });
  } catch (error) {
    console.error('Error fetching students:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching students',
      error: error.message
    });
  }
};

// Get student by roll number
const getStudentByRollNumber = async (req, res) => {
  try {
    const { rollNumber } = req.params;
    const student = await Student.findByRollNumber(rollNumber);

    if (!student) {
      return res.status(404).json({
        success: false,
        message: 'Student not found'
      });
    }

    res.json({
      success: true,
      data: student
    });
  } catch (error) {
    console.error('Error fetching student:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching student',
      error: error.message
    });
  }
};

module.exports = {
  registerStudent,
  getAllStudents,
  getStudentByRollNumber
};
