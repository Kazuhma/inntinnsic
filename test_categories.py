"""
Test script to verify NudeNet detection categories
This helps verify what category names the model actually returns
"""
import sys
from pathlib import Path

def test_categories():
    """Test NudeNet to see what categories it actually returns"""
    print("="*60)
    print("NudeNet Category Verification Test")
    print("="*60)
    print()

    # Import detector
    try:
        from nudenet import NudeDetector
        print("[OK] NudeNet imported successfully")
    except ImportError:
        print("[ERROR] NudeNet not installed. Run: pipenv install nudenet")
        return False

    # Check if user provided a test image
    if len(sys.argv) < 2:
        print()
        print("Usage: python test_categories.py <path_to_test_image>")
        print()
        print("This script will analyze a test image and show you exactly")
        print("what category names NudeNet returns, so you can verify the")
        print("FLAGGED_CATEGORIES in config.py are correct.")
        print()
        print("Example:")
        print("  python test_categories.py C:\\Users\\YourName\\Pictures\\test.jpg")
        print()
        return False

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"[ERROR] Image not found: {image_path}")
        return False

    print(f"[INFO] Test image: {image_path}")
    print()
    print("Loading NudeNet detector (this may take a moment)...")

    try:
        detector = NudeDetector()
        print("[OK] Detector loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load detector: {e}")
        return False

    print()
    print("Analyzing image...")
    print("-" * 60)

    try:
        detections = detector.detect(str(image_path))

        if not detections:
            print("[INFO] No detections found in this image")
            print()
            print("This could mean:")
            print("  - The image is clean (no nudity detected)")
            print("  - The image doesn't contain detectable content")
            print("  - Try a different test image")
            return True

        print(f"[OK] Found {len(detections)} detection(s)")
        print()

        # Show all detections
        for i, detection in enumerate(detections, 1):
            category = detection.get('class', 'unknown')
            confidence = detection.get('score', 0.0)
            box = detection.get('box', None)

            print(f"Detection #{i}:")
            print(f"  Category:   '{category}'")  # Show exact category name
            print(f"  Confidence: {confidence:.1%}")
            if box:
                print(f"  Bounding Box: {box}")
            print()

        # Show unique categories
        unique_categories = set(d['class'] for d in detections)
        print("-" * 60)
        print("Unique categories detected:")
        for cat in sorted(unique_categories):
            print(f"  - '{cat}'")

        print()
        print("-" * 60)
        print("Configuration Check:")
        print()

        # Import current config
        from config import FLAGGED_CATEGORIES

        print("Current FLAGGED_CATEGORIES in config.py:")
        for cat in FLAGGED_CATEGORIES:
            print(f"  - '{cat}'")

        print()

        # Check for mismatches
        detected_not_in_config = unique_categories - set(FLAGGED_CATEGORIES)
        config_not_in_detected = set(FLAGGED_CATEGORIES) - unique_categories

        if detected_not_in_config:
            print("[WARNING] Categories detected but NOT in config.py:")
            for cat in detected_not_in_config:
                print(f"  - '{cat}'")
            print()

        if config_not_in_detected:
            print("[INFO] Config categories not found in this image:")
            print("  (This is normal - they just weren't detected in THIS image)")
            for cat in config_not_in_detected:
                print(f"  - '{cat}'")
            print()

        # Show all available categories from NudeNet
        print("-" * 60)
        print("NudeNet v3.4+ Available Categories (from PyPI documentation):")
        print()

        # These are the ACTUAL categories from NudeNet v3.4+
        all_categories = [
            'FEMALE_GENITALIA_COVERED',
            'FACE_FEMALE',
            'BUTTOCKS_EXPOSED',
            'FEMALE_BREAST_EXPOSED',
            'FEMALE_GENITALIA_EXPOSED',
            'MALE_BREAST_EXPOSED',
            'ANUS_EXPOSED',
            'FEET_EXPOSED',
            'BELLY_COVERED',
            'FEET_COVERED',
            'ARMPITS_COVERED',
            'ARMPITS_EXPOSED',
            'FACE_MALE',
            'BELLY_EXPOSED',
            'MALE_GENITALIA_EXPOSED',
            'ANUS_COVERED',
            'FEMALE_BREAST_COVERED',
            'BUTTOCKS_COVERED',
        ]

        print("Explicit content categories (typically flagged):")
        explicit = [
            'ANUS_EXPOSED',
            'BUTTOCKS_EXPOSED',
            'FEMALE_BREAST_EXPOSED',
            'FEMALE_GENITALIA_EXPOSED',
            'MALE_GENITALIA_EXPOSED',
        ]
        for cat in explicit:
            in_config = "✓" if cat in FLAGGED_CATEGORIES else " "
            print(f"  [{in_config}] {cat}")

        print()
        print("Covered/partial categories (optional, for stricter filtering):")
        covered = [
            'ANUS_COVERED',
            'BUTTOCKS_COVERED',
            'FEMALE_BREAST_COVERED',
            'FEMALE_GENITALIA_COVERED',
            'MALE_BREAST_EXPOSED',
        ]
        for cat in covered:
            in_config = "✓" if cat in FLAGGED_CATEGORIES else " "
            print(f"  [{in_config}] {cat}")

        print()
        print("Body part categories (usually not flagged):")
        body_parts = [
            'BELLY_COVERED',
            'BELLY_EXPOSED',
            'FEET_COVERED',
            'FEET_EXPOSED',
            'ARMPITS_COVERED',
            'ARMPITS_EXPOSED',
            'FACE_FEMALE',
            'FACE_MALE',
        ]
        for cat in body_parts:
            in_config = "✓" if cat in FLAGGED_CATEGORIES else " "
            print(f"  [{in_config}] {cat}")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to analyze image: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_categories()
    print()
    print("="*60)
    if success:
        print("[SUCCESS] Test complete")
    else:
        print("[FAILURE] Test failed")
    print("="*60)
