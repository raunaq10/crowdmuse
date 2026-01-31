const db = require('../config/database');

class Attendance {
  static async create(attendanceData) {
    const { studentId, date, time, room, latitude, longitude, status = 'Present' } = attendanceData;
    
    try {
      const result = await db.promise.run(
        `INSERT INTO attendance (studentId, date, time, room, latitude, longitude, status) 
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [studentId, date, time, room, latitude || null, longitude || null, status]
      );
      
      return this.findById(result.lastID);
    } catch (err) {
      // Check if it's a unique constraint violation (duplicate attendance)
      if (err.message.includes('UNIQUE constraint failed')) {
        throw new Error('Attendance already marked for this student on this date');
      }
      throw err;
    }
  }

  static async findById(id) {
    const attendance = await db.promise.get(
      `SELECT a.*, s.name, s.rollNumber, s.year, s.stream 
       FROM attendance a 
       JOIN students s ON a.studentId = s.id 
       WHERE a.id = ?`,
      [id]
    );
    
    if (attendance) {
      attendance.geoLocation = attendance.latitude && attendance.longitude 
        ? { lat: attendance.latitude, lng: attendance.longitude }
        : null;
      delete attendance.latitude;
      delete attendance.longitude;
    }
    
    return attendance;
  }

  static async findByRollNumber(rollNumber) {
    const records = await db.promise.all(
      `SELECT a.*, s.name, s.rollNumber, s.year, s.stream 
       FROM attendance a 
       JOIN students s ON a.studentId = s.id 
       WHERE s.rollNumber = ? 
       ORDER BY a.date DESC, a.time DESC`,
      [rollNumber]
    );
    
    return records.map(record => ({
      ...record,
      geoLocation: record.latitude && record.longitude 
        ? { lat: record.latitude, lng: record.longitude }
        : null,
      latitude: undefined,
      longitude: undefined
    }));
  }

  static async findByDate(date) {
    const records = await db.promise.all(
      `SELECT a.*, s.name, s.rollNumber, s.year, s.stream 
       FROM attendance a 
       JOIN students s ON a.studentId = s.id 
       WHERE a.date = ? 
       ORDER BY a.time DESC`,
      [date]
    );
    
    return records.map(record => ({
      ...record,
      geoLocation: record.latitude && record.longitude 
        ? { lat: record.latitude, lng: record.longitude }
        : null,
      latitude: undefined,
      longitude: undefined
    }));
  }

  static async findByRoom(room) {
    const records = await db.promise.all(
      `SELECT a.*, s.name, s.rollNumber, s.year, s.stream 
       FROM attendance a 
       JOIN students s ON a.studentId = s.id 
       WHERE a.room = ? 
       ORDER BY a.date DESC, a.time DESC`,
      [room]
    );
    
    return records.map(record => ({
      ...record,
      geoLocation: record.latitude && record.longitude 
        ? { lat: record.latitude, lng: record.longitude }
        : null,
      latitude: undefined,
      longitude: undefined
    }));
  }

  static async checkDuplicate(studentId, date) {
    const record = await db.promise.get(
      'SELECT id FROM attendance WHERE studentId = ? AND date = ?',
      [studentId, date]
    );
    
    return !!record;
  }
}

module.exports = Attendance;
