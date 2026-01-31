import os
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
CURRENT_DATASET = PROJECT_ROOT / 'dataset'
BACKUP_DATASET = PROJECT_ROOT / 'dataset_backup'
CURRENT_MODEL = PROJECT_ROOT / 'face_recognition' / 'models' / 'lbph_model.yml'

def count_images_in_folder(folder_path):
    """Count image files in a folder"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', 
                       '.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP']
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in image_extensions):
                count += 1
    return count

def analyze_dataset(dataset_path, name):
    """Analyze a dataset folder"""
    if not dataset_path.exists():
        return None
    
    print(f"\n{'=' * 80}")
    print(f"ANALYZING {name.upper()}")
    print(f"{'=' * 80}")
    print(f"Path: {dataset_path}")
    
    student_folders = [f for f in dataset_path.iterdir() 
                      if f.is_dir() and f.name.startswith('pins_')]
    
    if len(student_folders) == 0:
        print("No student folders found!")
        return None
    
    total_images = 0
    student_stats = []
    
    for folder in sorted(student_folders):
        student_name = folder.name.replace('pins_', '')
        image_count = count_images_in_folder(folder)
        total_images += image_count
        student_stats.append((student_name, image_count))
    
    avg_images = total_images / len(student_folders) if student_folders else 0
    min_images = min(count for _, count in student_stats) if student_stats else 0
    max_images = max(count for _, count in student_stats) if student_stats else 0
    
    print(f"\nDataset Statistics:")
    print(f"  Total Students:        {len(student_folders)}")
    print(f"  Total Images:          {total_images:,}")
    print(f"  Average per Student:   {avg_images:.1f}")
    print(f"  Min Images:            {min_images}")
    print(f"  Max Images:            {max_images}")
    
    # Distribution analysis
    distribution = defaultdict(int)
    for _, count in student_stats:
        if count < 10:
            distribution['<10'] += 1
        elif count < 50:
            distribution['10-50'] += 1
        elif count < 100:
            distribution['50-100'] += 1
        elif count < 200:
            distribution['100-200'] += 1
        else:
            distribution['200+'] += 1
    
    print(f"\nImage Distribution:")
    for range_name in ['<10', '10-50', '50-100', '100-200', '200+']:
        count = distribution[range_name]
        if count > 0:
            percentage = (count / len(student_folders) * 100)
            print(f"  {range_name:>8} images: {count:>3} students ({percentage:>5.1f}%)")
    
    return {
        'students': len(student_folders),
        'total_images': total_images,
        'avg_images': avg_images,
        'min_images': min_images,
        'max_images': max_images,
        'student_stats': student_stats
    }

def estimate_accuracy(dataset_stats):
    """Estimate face recognition accuracy based on dataset quality"""
    if not dataset_stats:
        return None
    
    avg_images = dataset_stats['avg_images']
    min_images = dataset_stats['min_images']
    
    # Accuracy estimation based on training data quality
    # More images per person = better accuracy (generally)
    base_accuracy = 85.0  # Base accuracy for LBPH
    
    # Adjust based on average images per student
    if avg_images >= 200:
        accuracy_boost = 10.0
    elif avg_images >= 100:
        accuracy_boost = 7.0
    elif avg_images >= 50:
        accuracy_boost = 5.0
    elif avg_images >= 20:
        accuracy_boost = 3.0
    elif avg_images >= 10:
        accuracy_boost = 1.0
    else:
        accuracy_boost = -5.0
    
    # Penalty for students with very few images
    low_image_students = sum(1 for _, count in dataset_stats['student_stats'] if count < 10)
    low_image_penalty = (low_image_students / dataset_stats['students']) * 5.0
    
    estimated_accuracy = base_accuracy + accuracy_boost - low_image_penalty
    estimated_accuracy = max(60.0, min(98.0, estimated_accuracy))  # Clamp between 60-98%
    
    return estimated_accuracy

def compare_datasets():
    """Compare current and backup datasets"""
    print("=" * 80)
    print("TRAINING DATASET COMPARISON & ACCURACY ANALYSIS")
    print("=" * 80)
    
    # Analyze current dataset
    current_stats = analyze_dataset(CURRENT_DATASET, "CURRENT DATASET")
    
    # Analyze backup dataset
    backup_stats = analyze_dataset(BACKUP_DATASET, "BACKUP DATASET (FULL)")
    
    if not current_stats or not backup_stats:
        print("\nCannot compare - one or both datasets not found!")
        return
    
    # Compare
    print(f"\n{'=' * 80}")
    print("COMPARISON")
    print(f"{'=' * 80}")
    
    print(f"\n{'Metric':<30} {'Current':<20} {'Backup (Full)':<20} {'Difference':<15}")
    print("-" * 85)
    
    students_diff = backup_stats['students'] - current_stats['students']
    images_diff = backup_stats['total_images'] - current_stats['total_images']
    avg_diff = backup_stats['avg_images'] - current_stats['avg_images']
    
    print(f"{'Total Students':<30} {str(current_stats['students']):<20} {str(backup_stats['students']):<20} {students_diff:>+15}")
    print(f"{'Total Images':<30} {str(current_stats['total_images']):<20} {str(backup_stats['total_images']):<20} {images_diff:>+15,}")
    avg_current_str = f"{current_stats['avg_images']:.1f}"
    avg_backup_str = f"{backup_stats['avg_images']:.1f}"
    print(f"{'Avg Images/Student':<30} {avg_current_str:<20} {avg_backup_str:<20} {avg_diff:>+15.1f}")
    print(f"{'Min Images':<30} {str(current_stats['min_images']):<20} {str(backup_stats['min_images']):<20} {(backup_stats['min_images']-current_stats['min_images']):>+15}")
    print(f"{'Max Images':<30} {str(current_stats['max_images']):<20} {str(backup_stats['max_images']):<20} {(backup_stats['max_images']-current_stats['max_images']):>+15}")
    
    # Estimate accuracy
    print(f"\n{'=' * 80}")
    print("ESTIMATED ACCURACY")
    print(f"{'=' * 80}")
    
    current_accuracy = estimate_accuracy(current_stats)
    backup_accuracy = estimate_accuracy(backup_stats)
    
    print(f"\nCurrent Dataset (Reduced):")
    print(f"  Estimated Accuracy: {current_accuracy:.2f}%")
    print(f"  Model Size: ~360 MB")
    print(f"  Training Time: Faster")
    print(f"  Memory Usage: Lower")
    
    print(f"\nBackup Dataset (Full):")
    print(f"  Estimated Accuracy: {backup_accuracy:.2f}%")
    print(f"  Model Size: ~2 GB (estimated)")
    print(f"  Training Time: Slower")
    print(f"  Memory Usage: Higher (may cause allocation errors)")
    
    accuracy_improvement = backup_accuracy - current_accuracy
    print(f"\nPotential Accuracy Improvement: {accuracy_improvement:+.2f}%")
    
    # Model size comparison
    if CURRENT_MODEL.exists():
        current_size_mb = CURRENT_MODEL.stat().st_size / (1024 * 1024)
        print(f"\nCurrent Model Size: {current_size_mb:.2f} MB")
    
    estimated_backup_size_mb = (backup_stats['total_images'] / current_stats['total_images']) * 360
    print(f"Estimated Backup Model Size: {estimated_backup_size_mb:.2f} MB")
    
    # Recommendations
    print(f"\n{'=' * 80}")
    print("RECOMMENDATIONS")
    print(f"{'=' * 80}")
    
    if accuracy_improvement > 5:
        print(f"\nThe backup dataset may provide {accuracy_improvement:.1f}% better accuracy.")
        print("However, consider:")
        print("  - Model size will be much larger (~{:.0f} MB)".format(estimated_backup_size_mb))
        print("  - May cause memory allocation errors")
        print("  - Training will take longer")
        print("\nAlternative: Use a balanced approach (20-30 images per student)")
    elif accuracy_improvement > 0:
        print(f"\nBackup dataset may provide slight improvement ({accuracy_improvement:.1f}%)")
        print("But current dataset is more efficient and practical.")
    else:
        print(f"\nCurrent dataset is optimal for this use case.")
        print("More images don't always mean better accuracy with LBPH.")
    
    # Efficiency score
    print(f"\n{'=' * 80}")
    print("EFFICIENCY SCORE")
    print(f"{'=' * 80}")
    
    current_efficiency = (
        (current_accuracy * 0.6) +  # 60% weight on accuracy
        ((360 / estimated_backup_size_mb * 100) * 0.2) +  # 20% weight on model size
        (100 * 0.2)  # 20% weight on reliability (current works, backup may not)
    )
    
    backup_efficiency = (
        (backup_accuracy * 0.6) +  # 60% weight on accuracy
        ((estimated_backup_size_mb / estimated_backup_size_mb * 100) * 0.2) +  # 20% weight on model size
        (50 * 0.2)  # 20% weight on reliability (may have memory issues)
    )
    
    print(f"\nCurrent Dataset Efficiency: {current_efficiency:.2f}%")
    print(f"Backup Dataset Efficiency: {backup_efficiency:.2f}%")
    
    if current_efficiency > backup_efficiency:
        print(f"\nVerdict: Current dataset is MORE EFFICIENT")
        print("The reduced dataset provides better balance of accuracy and performance.")
    else:
        print(f"\nVerdict: Backup dataset may be more accurate")
        print("But consider memory and performance trade-offs.")

if __name__ == '__main__':
    compare_datasets()
