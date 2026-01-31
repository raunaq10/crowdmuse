const db = require('../config/database');

class Student {
  static async create(studentData) {
    const { name, rollNumber, year, stream, photos } = studentData;
    const photosJson = JSON.stringify(photos);
    
    const result = await db.promise.run(
      `INSERT INTO students (name, rollNumber, year, stream, photos) 
       VALUES (?, ?, ?, ?, ?)`,
      [name, rollNumber, year, stream, photosJson]
    );
    
    return this.findById(result.lastID);
  }

  static async findById(id) {
    const student = await db.promise.get(
      'SELECT * FROM students WHERE id = ?',
      [id]
    );
    
    if (student) {
      student.photos = JSON.parse(student.photos);
    }
    
    return student;
  }

  static async findByRollNumber(rollNumber) {
    const student = await db.promise.get(
      'SELECT * FROM students WHERE rollNumber = ?',
      [rollNumber]
    );
    
    if (student) {
      student.photos = JSON.parse(student.photos);
    }
    
    return student;
  }

  static async findAll() {
    const students = await db.promise.all(
      'SELECT * FROM students ORDER BY createdAt DESC'
    );
    
    return students.map(student => ({
      ...student,
      photos: JSON.parse(student.photos)
    }));
  }

  static async update(id, studentData) {
    const { name, year, stream, photos } = studentData;
    const photosJson = JSON.stringify(photos);
    
    await db.promise.run(
      `UPDATE students 
       SET name = ?, year = ?, stream = ?, photos = ?, updatedAt = CURRENT_TIMESTAMP 
       WHERE id = ?`,
      [name, year, stream, photosJson, id]
    );
    
    return this.findById(id);
  }

  static async delete(id) {
    return await db.promise.run('DELETE FROM students WHERE id = ?', [id]);
  }
}

module.exports = Student;
