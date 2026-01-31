const { body, validationResult } = require('express-validator');

// Validation middleware
const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      errors: errors.array()
    });
  }
  next();
};

// Student registration validation
const validateStudentRegistration = [
  body('name')
    .trim()
    .notEmpty()
    .withMessage('Name is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Name must be between 2 and 100 characters'),
  
  body('rollNumber')
    .trim()
    .notEmpty()
    .withMessage('Roll number is required')
    .isLength({ min: 1, max: 50 })
    .withMessage('Roll number must be between 1 and 50 characters'),
  
  body('year')
    .trim()
    .notEmpty()
    .withMessage('Year is required')
    .matches(/^(1st|2nd|3rd|4th|First|Second|Third|Fourth|\d{1,2}(st|nd|rd|th)?)$/i)
    .withMessage('Year must be a valid year designation'),
  
  body('stream')
    .trim()
    .notEmpty()
    .withMessage('Stream/Department is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Stream must be between 2 and 100 characters'),
  
  handleValidationErrors
];

// Attendance marking validation
const validateAttendance = [
  body('studentId')
    .notEmpty()
    .withMessage('Student ID is required')
    .isInt({ min: 1 })
    .withMessage('Student ID must be a valid integer'),
  
  body('date')
    .trim()
    .notEmpty()
    .withMessage('Date is required')
    .matches(/^\d{4}-\d{2}-\d{2}$/)
    .withMessage('Date must be in YYYY-MM-DD format'),
  
  body('time')
    .trim()
    .notEmpty()
    .withMessage('Time is required')
    .matches(/^\d{2}:\d{2}:\d{2}$/)
    .withMessage('Time must be in HH:MM:SS format'),
  
  body('room')
    .trim()
    .notEmpty()
    .withMessage('Room/Classroom identifier is required')
    .isLength({ min: 1, max: 50 })
    .withMessage('Room must be between 1 and 50 characters'),
  
  body('latitude')
    .optional()
    .isFloat({ min: -90, max: 90 })
    .withMessage('Latitude must be between -90 and 90'),
  
  body('longitude')
    .optional()
    .isFloat({ min: -180, max: 180 })
    .withMessage('Longitude must be between -180 and 180'),
  
  body('status')
    .optional()
    .isIn(['Present', 'Absent', 'Late'])
    .withMessage('Status must be Present, Absent, or Late'),
  
  handleValidationErrors
];

module.exports = {
  validateStudentRegistration,
  validateAttendance,
  handleValidationErrors
};
