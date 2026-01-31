const fs = require('fs');
const path = require('path');
const Student = require('../models/Student');
const db = require('../config/database');

// Configuration
const DATASET_PATH = path.join(__dirname, '..', 'dataset');
const UPLOADS_PATH = path.join(__dirname, '..', 'uploads');

// Supported image extensions
const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

/**
 * Extract student info from folder name
 * Handles formats like: "pins_Adriana Lima", "pins_Alex Lawther", etc.
 */
function parseStudentInfo(folderName) {
  // Remove "pins_" prefix if present
  let cleanName = folderName.replace(/^pins_/i, '');
  
  // Generate roll number from name (first 3 letters of first name + first 3 letters of last name + random number)
  const nameParts = cleanName.trim().split(/\s+/);
  let rollNumber;
  
  if (nameParts.length >= 2) {
    // Has first and last name
    const firstName = nameParts[0].substring(0, 3).toUpperCase();
    const lastName = nameParts[nameParts.length - 1].substring(0, 3).toUpperCase();
    const randomNum = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    rollNumber = `${firstName}${lastName}${randomNum}`;
  } else {
    // Single name
    const name = nameParts[0].substring(0, 6).toUpperCase().replace(/[^A-Z]/g, '');
    const randomNum = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    rollNumber = `${name}${randomNum}`;
  }
  
  return {
    name: cleanName,
    rollNumber: rollNumber
  };
}

/**
 * Copy image to uploads folder and return relative path
 */
function copyImageToUploads(sourcePath, rollNumber, index) {
  const ext = path.extname(sourcePath).toLowerCase();
  if (!IMAGE_EXTENSIONS.includes(ext)) {
    return null;
  }
  
  const filename = `${rollNumber}-import-${Date.now()}-${index}${ext}`;
  const destPath = path.join(UPLOADS_PATH, filename);
  
  try {
    fs.copyFileSync(sourcePath, destPath);
    return `/uploads/${filename}`;
  } catch (error) {
    console.error(`Error copying ${sourcePath}:`, error.message);
    return null;
  }
}

/**
 * Get all image files from a directory (recursively)
 */
function getImageFiles(dirPath) {
  const imageFiles = [];
  
  function scanDirectory(currentPath) {
    try {
      const items = fs.readdirSync(currentPath);
      
      for (const item of items) {
        const itemPath = path.join(currentPath, item);
        const stat = fs.statSync(itemPath);
        
        if (stat.isDirectory()) {
          // Recursively scan subdirectories
          scanDirectory(itemPath);
        } else if (stat.isFile()) {
          const ext = path.extname(item).toLowerCase();
          if (IMAGE_EXTENSIONS.includes(ext)) {
            imageFiles.push(itemPath);
          }
        }
      }
    } catch (error) {
      console.error(`Error scanning ${currentPath}:`, error.message);
    }
  }
  
  scanDirectory(dirPath);
  return imageFiles;
}

/**
 * Import a single student from a folder
 */
async function importStudent(folderPath, folderName) {
  try {
    const studentInfo = parseStudentInfo(folderName);
    const imageFiles = getImageFiles(folderPath);

    if (imageFiles.length === 0) {
      console.log(`⚠️  Skipping ${folderName}: No images found`);
      return null;
    }

    // Check if student already exists
    const existing = await Student.findByRollNumber(studentInfo.rollNumber);
    if (existing) {
      // If exists, try with a different roll number
      studentInfo.rollNumber = `${studentInfo.rollNumber}_${Date.now().toString().slice(-4)}`;
    }

    // Copy images to uploads folder
    const photoPaths = [];
    for (let i = 0; i < imageFiles.length; i++) {
      const photoPath = copyImageToUploads(imageFiles[i], studentInfo.rollNumber, i);
      if (photoPath) {
        photoPaths.push(photoPath);
      }
    }

    if (photoPaths.length === 0) {
      console.log(`⚠️  Skipping ${folderName}: No valid images copied`);
      return null;
    }

    // Create student record
    const student = await Student.create({
      name: studentInfo.name,
      rollNumber: studentInfo.rollNumber,
      year: '1st', // Default - you can modify this
      stream: 'General', // Default - you can modify this
      photos: photoPaths
    });

    console.log(`✅ Imported: ${studentInfo.name} (${studentInfo.rollNumber}) - ${photoPaths.length} images`);
    return student;
  } catch (error) {
    console.error(`❌ Error importing ${folderName}:`, error.message);
    return null;
  }
}

/**
 * Main import function
 */
async function bulkImport() {
  console.log('🚀 Starting bulk import...\n');

  // Check if dataset folder exists
  if (!fs.existsSync(DATASET_PATH)) {
    console.error(`❌ Dataset folder not found: ${DATASET_PATH}`);
    process.exit(1);
  }

  // Ensure uploads folder exists
  if (!fs.existsSync(UPLOADS_PATH)) {
    fs.mkdirSync(UPLOADS_PATH, { recursive: true });
    console.log('📁 Created uploads directory');
  }

  // Get all student folders
  const folders = fs.readdirSync(DATASET_PATH)
    .filter(item => {
      const itemPath = path.join(DATASET_PATH, item);
      return fs.statSync(itemPath).isDirectory();
    });

  if (folders.length === 0) {
    console.error('❌ No student folders found in dataset directory');
    process.exit(1);
  }

  console.log(`📁 Found ${folders.length} student folders\n`);

  let imported = 0;
  let skipped = 0;

  // Import each student
  for (const folder of folders) {
    const folderPath = path.join(DATASET_PATH, folder);
    const result = await importStudent(folderPath, folder);
    
    if (result) {
      imported++;
    } else {
      skipped++;
    }
  }

  console.log(`\n✨ Import complete!`);
  console.log(`   ✅ Imported: ${imported}`);
  console.log(`   ⏭️  Skipped: ${skipped}`);
  console.log(`   📊 Total: ${folders.length}`);

  // Close database connection
  db.close((err) => {
    if (err) {
      console.error('Error closing database:', err);
    } else {
      console.log('\n✅ Database connection closed');
    }
    process.exit(0);
  });
}

// Run import
bulkImport().catch(error => {
  console.error('Fatal error:', error);
  db.close();
  process.exit(1);
});
