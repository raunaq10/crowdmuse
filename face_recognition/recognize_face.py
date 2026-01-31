import cv2
import pickle
import numpy as np
from pathlib import Path

class FaceRecognizer:
    def __init__(self, model_path='face_recognition/models'):
        """
        Initialize the face recognizer with trained model
        
        Args:
            model_path: Path to the trained model directory
        """
        self.model_path = Path(model_path)
        
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Load trained recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        model_file = self.model_path / 'lbph_model.yml'
        
        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found: {model_file}")
        
        # Try loading with error handling for large files
        try:
            print(f"Loading model file: {model_file} (Size: {model_file.stat().st_size / (1024*1024*1024):.2f} GB)")
            self.recognizer.read(str(model_file))
            print("Model loaded successfully!")
        except cv2.error as e:
            if "bad allocation" in str(e).lower():
                raise MemoryError(
                    f"Failed to load model: Memory allocation error. "
                    f"The model file ({model_file.stat().st_size / (1024*1024*1024):.2f} GB) may be too large. "
                    f"Try retraining with fewer images or check available system memory."
                )
            raise
        
        # Load label mappings
        label_file = self.model_path / 'label_mappings.pkl'
        if not label_file.exists():
            raise FileNotFoundError(f"Label mappings not found: {label_file}")
        
        with open(label_file, 'rb') as f:
            mappings = pickle.load(f)
            self.label_to_name = mappings['label_to_name']
            self.name_to_label = mappings['name_to_label']
        
        print(f"Loaded model with {len(self.label_to_name)} known faces")
    
    def detect_face(self, image):
        """
        Detect face in an image
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of detected faces [(x, y, w, h), ...]
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def recognize(self, image, confidence_threshold=70):
        """
        Recognize faces in an image
        
        Args:
            image: Input image (BGR format)
            confidence_threshold: Confidence threshold (lower = more strict)
            
        Returns:
            List of recognition results: [(name, confidence, (x, y, w, h)), ...]
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detect_face(image)
        
        results = []
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            
            # Predict
            label_id, confidence = self.recognizer.predict(face_roi)
            
            # Lower confidence is better in LBPH
            if confidence < confidence_threshold:
                name = self.label_to_name.get(label_id, "Unknown")
                results.append((name, confidence, (x, y, w, h)))
            else:
                results.append(("Unknown", confidence, (x, y, w, h)))
        
        return results
    
    def recognize_from_file(self, image_path, confidence_threshold=70):
        """
        Recognize faces from an image file
        
        Args:
            image_path: Path to image file
            confidence_threshold: Confidence threshold
            
        Returns:
            List of recognition results
        """
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        return self.recognize(image, confidence_threshold)
    
    def recognize_from_camera(self, camera_index=0, confidence_threshold=70):
        """
        Real-time face recognition from camera
        
        Args:
            camera_index: Camera device index (usually 0)
            confidence_threshold: Confidence threshold
        """
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open camera {camera_index}")
        
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Recognize faces
            results = self.recognize(frame, confidence_threshold)
            
            # Draw results
            for name, confidence, (x, y, w, h) in results:
                # Draw rectangle
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Draw label
                label = f"{name} ({confidence:.1f})"
                cv2.putText(frame, label, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Show frame
            cv2.imshow('Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()


def main():
    import sys
    
    recognizer = FaceRecognizer()
    
    if len(sys.argv) > 1:
        # Recognize from image file
        image_path = sys.argv[1]
        results = recognizer.recognize_from_file(image_path)
        
        print(f"\nRecognized {len(results)} face(s):")
        for name, confidence, (x, y, w, h) in results:
            print(f"  - {name} (confidence: {confidence:.2f})")
    else:
        # Real-time recognition from camera
        print("Starting camera...")
        recognizer.recognize_from_camera()


if __name__ == '__main__':
    main()
