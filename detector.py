"""
Image detection module using NudeNet AI model
"""
from nudenet import NudeDetector
from PIL import Image
from config import DETECTION_THRESHOLD, FLAGGED_CATEGORIES
import logging
from pathlib import Path

class ImageDetector:
    def __init__(self, threshold=None):
        """Initialize the detector and load the AI model

        Args:
            threshold: Detection threshold (0.0-1.0). If None, uses DETECTION_THRESHOLD from config
        """
        print("Loading AI detection model...")
        try:
            # NudeNet will download model on first run (~60MB)
            # The model is stored in ~/.NudeNet/
            self.detector = NudeDetector()
            self.threshold = threshold if threshold is not None else DETECTION_THRESHOLD
            print("✓ Model loaded successfully!")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise

    def analyze_image(self, image_path):
        """
        Analyze a single image for inappropriate content

        Args:
            image_path: Path to the image file

        Returns:
            dict with keys:
                - path: original file path
                - flagged: boolean indicating if image was flagged
                - detections: list of detection details
                - error: error message if processing failed
        """
        try:
            # Validate file exists and is accessible
            image_path = Path(image_path)
            if not image_path.exists():
                return {
                    'path': image_path,
                    'flagged': False,
                    'detections': [],
                    'error': 'File not found'
                }

            # Try to open image first to validate it
            try:
                with Image.open(image_path) as img:
                    # Verify it's a valid image
                    img.verify()
            except Exception as e:
                return {
                    'path': image_path,
                    'flagged': False,
                    'detections': [],
                    'error': f'Invalid image: {str(e)}'
                }

            # Detect nudity using NudeNet
            detections = self.detector.detect(str(image_path))

            # Check if any flagged categories detected above threshold
            flagged_items = []
            for detection in detections:
                if (detection['class'] in FLAGGED_CATEGORIES and
                    detection['score'] >= self.threshold):
                    flagged_items.append({
                        'category': detection['class'],
                        'confidence': detection['score'],
                        'bbox': detection.get('box', None)  # Bounding box if available
                    })

            return {
                'path': image_path,
                'flagged': len(flagged_items) > 0,
                'detections': flagged_items,
                'error': None
            }

        except Exception as e:
            logging.error(f"Error processing {image_path}: {e}")
            return {
                'path': image_path,
                'flagged': False,
                'detections': [],
                'error': str(e)
            }

    def batch_analyze(self, image_paths, progress_callback=None):
        """
        Analyze multiple images with progress updates

        Args:
            image_paths: List of paths to analyze
            progress_callback: Optional callback(current, total, result)

        Returns:
            List of result dictionaries
        """
        results = []
        total = len(image_paths)

        for i, path in enumerate(image_paths):
            result = self.analyze_image(path)
            results.append(result)

            if progress_callback:
                progress_callback(i + 1, total, result)

        return results

    def get_summary(self, results):
        """
        Generate a summary of analysis results

        Args:
            results: List of result dictionaries from batch_analyze

        Returns:
            Dictionary with summary statistics
        """
        total = len(results)
        flagged = sum(1 for r in results if r['flagged'])
        errors = sum(1 for r in results if r['error'])
        clean = total - flagged - errors

        # Count by category
        category_counts = {}
        for result in results:
            if result['flagged']:
                for detection in result['detections']:
                    category = detection['category']
                    category_counts[category] = category_counts.get(category, 0) + 1

        return {
            'total_scanned': total,
            'flagged': flagged,
            'clean': clean,
            'errors': errors,
            'categories': category_counts
        }
