import os
import shutil
from pathlib import Path
import random

# Configuration
DATASET_PATH = Path(__file__).parent.parent / 'dataset'
MAX_IMAGES_PER_STUDENT = 30  # Keep only 30 images per student
BACKUP = True  # Create backup before deleting

def cleanup_dataset():
    """
    Remove excess images from dataset, keeping only MAX_IMAGES_PER_STUDENT per student
    """
    print("=" * 60)
    print("Dataset Cleanup Script")
    print("=" * 60)
    print(f"Dataset path: {DATASET_PATH}")
    print(f"Max images per student: {MAX_IMAGES_PER_STUDENT}")
    print(f"Backup before cleanup: {BACKUP}\n")
    
    if not DATASET_PATH.exists():
        print(f"Error: Dataset folder not found: {DATASET_PATH}")
        return False
    
    # Create backup if requested
    if BACKUP:
        backup_path = DATASET_PATH.parent / 'dataset_backup'
        if not backup_path.exists():
            print("Creating backup...")
            try:
                shutil.copytree(DATASET_PATH, backup_path)
                print(f"Backup created at: {backup_path}\n")
            except Exception as e:
                print(f"Warning: Could not create backup: {e}")
                response = input("Continue without backup? (y/n): ")
                if response.lower() != 'y':
                    return False
    
    # Get all student folders
    student_folders = [f for f in DATASET_PATH.iterdir() 
                       if f.is_dir() and f.name.startswith('pins_')]
    
    if len(student_folders) == 0:
        print("No student folders found!")
        return False
    
    print(f"Found {len(student_folders)} student folders\n")
    
    total_removed = 0
    total_kept = 0
    students_processed = 0
    
    # Process each student folder
    for student_folder in sorted(student_folders):
        student_name = student_folder.name.replace('pins_', '')
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', 
                           '.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP']
        image_files = [f for f in student_folder.iterdir() 
                      if f.is_file() and f.suffix in image_extensions]
        
        if len(image_files) <= MAX_IMAGES_PER_STUDENT:
            print(f"OK {student_name}: {len(image_files)} images (no cleanup needed)")
            total_kept += len(image_files)
            students_processed += 1
            continue
        
        # Randomly select images to keep
        images_to_keep = random.sample(image_files, MAX_IMAGES_PER_STUDENT)
        images_to_remove = [f for f in image_files if f not in images_to_keep]
        
        # Remove excess images
        removed_count = 0
        for img_file in images_to_remove:
            try:
                img_file.unlink()
                removed_count += 1
            except Exception as e:
                print(f"  Warning: Could not delete {img_file.name}: {e}")
        
        print(f"OK {student_name}: Kept {len(images_to_keep)}, Removed {removed_count} images")
        total_kept += len(images_to_keep)
        total_removed += removed_count
        students_processed += 1
    
    print("\n" + "=" * 60)
    print("Cleanup Summary")
    print("=" * 60)
    print(f"Students processed: {students_processed}")
    print(f"Total images kept: {total_kept}")
    print(f"Total images removed: {total_removed}")
    print(f"Reduction: {total_removed / (total_kept + total_removed) * 100:.1f}%")
    print("=" * 60)
    
    if BACKUP:
        print(f"\nBackup available at: {backup_path}")
        print("You can restore from backup if needed.")
    
    return True

if __name__ == '__main__':
    print("\nWARNING: This will DELETE excess images from your dataset!")
    print(f"   Keeping only {MAX_IMAGES_PER_STUDENT} images per student.\n")
    
    if BACKUP:
        print("A backup will be created before cleanup.\n")
    
    response = input("Do you want to proceed? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        success = cleanup_dataset()
        if success:
            print("\nCleanup completed successfully!")
            print("\nNext steps:")
            print("1. Retrain the model: python face_recognition/train_model.py")
            print("2. The new model will be much smaller and should load without issues")
        else:
            print("\nCleanup failed. Please check the errors above.")
    else:
        print("\nCleanup cancelled.")
