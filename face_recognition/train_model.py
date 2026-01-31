import cv2
import numpy as np
import os
import pickle
from pathlib import Path

class FaceRecognitionTrainer:
    def __init__(self, dataset_path, model_save_path='face_recognition/models'):
        """
        Initialize the face recognition trainer
        
        Args:
            dataset_path: Path to the dataset folder (e.g., '../dataset')
            model_save_path: Path to save the trained model
        """
        self.dataset_path = Path(dataset_path)
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize face detector (Haar Cascade)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Initialize LBPH Face Recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1,
            neighbors=8,
            grid_x=8,
            grid_y=8
        )
        
        self.faces = []
        self.labels = []
        self.label_to_name = {}
        self.name_to_label = {}
        
    def detect_face(self, image):
        """
        Detect face in an image using Haar Cascade
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Detected face region (grayscale) or None
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # Return the largest face (assuming it's the main subject)
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        x, y, w, h = faces[0]
        
        # Extract face region
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize to standard size for training
        face_roi = cv2.resize(face_roi, (200, 200))
        
        return face_roi
    
    def load_dataset(self):
        """
        Load images from dataset folder and prepare for training
        
        Dataset structure expected:
        dataset/
        ├── pins_Student Name/
        │   ├── image1.jpg
        │   ├── image2.jpg
        │   └── ...
        """
        print("Loading dataset...")
        
        # Get all student folders
        student_folders = [f for f in self.dataset_path.iterdir() 
                          if f.is_dir() and f.name.startswith('pins_')]
        
        if len(student_folders) == 0:
            print(f"Error: No student folders found in {self.dataset_path}")
            return False
        
        print(f"Found {len(student_folders)} student folders\n")
        
        label_id = 0
        total_images = 0
        successful_detections = 0
        
        for student_folder in sorted(student_folders):
            # Extract student name (remove 'pins_' prefix)
            student_name = student_folder.name.replace('pins_', '')
            
            if student_name not in self.name_to_label:
                self.name_to_label[student_name] = label_id
                self.label_to_name[label_id] = student_name
                label_id += 1
            
            current_label = self.name_to_label[student_name]
            
            # Get all image files
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                image_files.extend(student_folder.glob(ext))
            
            print(f"Processing {student_name}... ({len(image_files)} images)", end=' ')
            
            processed_count = 0
            
            for img_path in image_files:
                try:
                    # Read image
                    image = cv2.imread(str(img_path))
                    if image is None:
                        continue
                    
                    # Detect face
                    face = self.detect_face(image)
                    
                    if face is not None:
                        self.faces.append(face)
                        self.labels.append(current_label)
                        successful_detections += 1
                        processed_count += 1
                    
                    total_images += 1
                    
                except Exception as e:
                    print(f"\nWarning: Error processing {img_path}: {e}")
                    continue
            
            print(f"OK ({processed_count} faces detected)")
        
        print(f"\nDataset Summary:")
        print(f"   Total images processed: {total_images}")
        print(f"   Faces successfully detected: {successful_detections}")
        print(f"   Students: {len(self.name_to_label)}")
        print(f"   Average faces per student: {successful_detections / len(self.name_to_label):.1f}")
        
        return len(self.faces) > 0
    
    def train(self):
        """
        Train the LBPH face recognizer
        """
        if len(self.faces) == 0:
            print("Error: No faces found to train on!")
            return False
        
        print(f"\nTraining LBPH Face Recognizer...")
        print(f"   Training on {len(self.faces)} face samples")
        print(f"   Number of classes: {len(self.name_to_label)}")
        
        try:
            # Convert to numpy arrays
            faces_array = np.array(self.faces, dtype='uint8')
            labels_array = np.array(self.labels, dtype='int32')
            
            # Train the recognizer
            self.recognizer.train(faces_array, labels_array)
            
            print("Training completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error during training: {e}")
            return False
    
    def save_model(self):
        """
        Save the trained model and label mappings
        """
        try:
            # Save the recognizer model
            model_file = self.model_save_path / 'lbph_model.yml'
            self.recognizer.write(str(model_file))
            print(f"Model saved to: {model_file}")
            
            # Save label mappings
            label_file = self.model_save_path / 'label_mappings.pkl'
            with open(label_file, 'wb') as f:
                pickle.dump({
                    'label_to_name': self.label_to_name,
                    'name_to_label': self.name_to_label
                }, f)
            print(f"Label mappings saved to: {label_file}")
            
            # Save a readable text file with mappings
            text_file = self.model_save_path / 'label_mappings.txt'
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write("Label to Name Mappings:\n")
                f.write("=" * 50 + "\n")
                for label_id, name in sorted(self.label_to_name.items()):
                    f.write(f"Label {label_id}: {name}\n")
            print(f"Text mappings saved to: {text_file}")
            
            return True
            
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def run(self):
        """
        Run the complete training pipeline
        """
        print("=" * 60)
        print("Face Recognition Model Training")
        print("=" * 60)
        print(f"Dataset path: {self.dataset_path}")
        print(f"Model save path: {self.model_save_path}\n")
        
        # Load dataset
        if not self.load_dataset():
            return False
        
        # Train model
        if not self.train():
            return False
        
        # Save model
        if not self.save_model():
            return False
        
        print("\n" + "=" * 60)
        print("Training pipeline completed successfully!")
        print("=" * 60)
        
        return True


def main():
    # Configuration
    # Adjust these paths based on your project structure
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    dataset_path = project_root / 'dataset'
    model_save_path = script_dir / 'models'
    
    # Create trainer and run
    trainer = FaceRecognitionTrainer(
        dataset_path=str(dataset_path),
        model_save_path=str(model_save_path)
    )
    
    success = trainer.run()
    
    if success:
        print("\nNext steps:")
        print("   1. Use the trained model for face recognition")
        print("   2. The model file is: face_recognition/models/lbph_model.yml")
        print("   3. Label mappings are in: face_recognition/models/label_mappings.pkl")
    else:
        print("\nError: Training failed. Please check the errors above.")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
