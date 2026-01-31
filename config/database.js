const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, '..', 'attendance.db');

// Create database connection
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    console.log('Connected to SQLite database');
    initializeDatabase();
  }
});

// Initialize database tables
function initializeDatabase() {
  // Students table
  db.run(`
    CREATE TABLE IF NOT EXISTS students (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      rollNumber TEXT UNIQUE NOT NULL,
      year TEXT NOT NULL,
      stream TEXT NOT NULL,
      photos TEXT NOT NULL,
      createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
      updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `, (err) => {
    if (err) {
      console.error('Error creating students table:', err.message);
    } else {
      console.log('Students table ready');
      
      // Attendance table (create after students table)
      db.run(`
        CREATE TABLE IF NOT EXISTS attendance (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          studentId INTEGER NOT NULL,
          date TEXT NOT NULL,
          time TEXT NOT NULL,
          room TEXT NOT NULL,
          latitude REAL,
          longitude REAL,
          status TEXT DEFAULT 'Present',
          createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (studentId) REFERENCES students(id),
          UNIQUE(studentId, date)
        )
      `, (err) => {
        if (err) {
          console.error('Error creating attendance table:', err.message);
        } else {
          console.log('Attendance table ready');
          
          // Create indexes after tables are created
          db.run(`CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date)`, (err) => {
            if (err) console.error('Error creating date index:', err.message);
          });
          
          db.run(`CREATE INDEX IF NOT EXISTS idx_attendance_room ON attendance(room)`, (err) => {
            if (err) console.error('Error creating room index:', err.message);
          });
          
          db.run(`CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(studentId)`, (err) => {
            if (err) console.error('Error creating student index:', err.message);
            else console.log('Database initialization complete');
          });
        }
      });
    }
  });
}

// Promisify database methods for easier async/await usage
db.promise = {
  run: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.run(sql, params, function(err) {
        if (err) reject(err);
        else resolve({ lastID: this.lastID, changes: this.changes });
      });
    });
  },
  get: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  },
  all: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.all(sql, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  }
};

module.exports = db;
