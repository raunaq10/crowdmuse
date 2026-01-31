const Attendance = require('../models/Attendance');
const Student = require('../models/Student');

// Mark attendance for a recognized student
const markAttendance = async (req, res) => {
  try {
    const { studentId, date, time, room, latitude, longitude, status } = req.body;

    // Verify student exists
    const student = await Student.findById(studentId);
    if (!student) {
      return res.status(404).json({
        success: false,
        message: 'Student not found'
      });
    }

    // Check for duplicate attendance (already handled by UNIQUE constraint, but we can check first)
    const isDuplicate = await Attendance.checkDuplicate(studentId, date);
    if (isDuplicate) {
      return res.status(409).json({
        success: false,
        message: 'Attendance already marked for this student on this date'
      });
    }

    // Create attendance record
    const attendance = await Attendance.create({
      studentId,
      date,
      time,
      room,
      latitude,
      longitude,
      status: status || 'Present'
    });

    res.status(201).json({
      success: true,
      message: 'Attendance marked successfully',
      data: attendance
    });
  } catch (error) {
    console.error('Error marking attendance:', error);
    
    if (error.message.includes('already marked')) {
      return res.status(409).json({
        success: false,
        message: error.message
      });
    }

    res.status(500).json({
      success: false,
      message: 'Error marking attendance',
      error: error.message
    });
  }
};

// Get attendance history by roll number
const getAttendanceByRollNumber = async (req, res) => {
  try {
    const { rollNumber } = req.params;
    
    // Verify student exists
    const student = await Student.findByRollNumber(rollNumber);
    if (!student) {
      return res.status(404).json({
        success: false,
        message: 'Student not found'
      });
    }

    const records = await Attendance.findByRollNumber(rollNumber);

    res.json({
      success: true,
      student: {
        name: student.name,
        rollNumber: student.rollNumber,
        year: student.year,
        stream: student.stream
      },
      count: records.length,
      data: records
    });
  } catch (error) {
    console.error('Error fetching attendance:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching attendance records',
      error: error.message
    });
  }
};

// Get attendance records by date
const getAttendanceByDate = async (req, res) => {
  try {
    const { date } = req.params;
    
    // Validate date format
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid date format. Use YYYY-MM-DD'
      });
    }

    const records = await Attendance.findByDate(date);

    res.json({
      success: true,
      date: date,
      count: records.length,
      data: records
    });
  } catch (error) {
    console.error('Error fetching attendance by date:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching attendance records',
      error: error.message
    });
  }
};

// Get attendance records by room
const getAttendanceByRoom = async (req, res) => {
  try {
    const { room } = req.params;
    const records = await Attendance.findByRoom(room);

    res.json({
      success: true,
      room: room,
      count: records.length,
      data: records
    });
  } catch (error) {
    console.error('Error fetching attendance by room:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching attendance records',
      error: error.message
    });
  }
};

module.exports = {
  markAttendance,
  getAttendanceByRollNumber,
  getAttendanceByDate,
  getAttendanceByRoom
};
