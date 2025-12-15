"""
Setup verification script for Inntinnsic
Run this to verify all dependencies are installed correctly
"""
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing module imports...")

    tests = [
        ("Pillow (PIL)", "PIL"),
        ("tkinter", "tkinter"),
        ("NudeNet", "nudenet"),
        ("Config module", "config"),
        ("Scanner module", "scanner"),
        ("Detector module", "detector"),
        ("GUI module", "gui"),
    ]

    failed = []

    for name, module in tests:
        try:
            __import__(module)
            print(f"  [OK] {name}")
        except ImportError as e:
            print(f"  [FAIL] {name}: {e}")
            failed.append(name)

    return len(failed) == 0, failed

def test_scanner():
    """Test the scanner module"""
    print("\nTesting scanner functionality...")

    try:
        from scanner import FileScanner
        scanner = FileScanner()

        # Test drive detection
        drives = scanner.get_available_drives()
        print(f"  [OK] Found {len(drives)} drive(s): {', '.join(drives)}")

        return True
    except Exception as e:
        print(f"  [FAIL] Scanner test failed: {e}")
        return False

def test_detector():
    """Test the detector module (without loading the full model)"""
    print("\nTesting detector initialization...")

    try:
        from detector import ImageDetector
        print("  [INFO] Detector class loaded successfully")
        print("  [INFO] Model will download (~60MB) on first actual scan")
        print("  [SKIP] Not loading full model in test (saves time)")
        return True
    except Exception as e:
        print(f"  [FAIL] Detector test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")

    try:
        from config import (
            APP_NAME, APP_VERSION, IMAGE_EXTENSIONS,
            DETECTION_THRESHOLD, get_common_locations
        )

        print(f"  [OK] App Name: {APP_NAME}")
        print(f"  [OK] Version: {APP_VERSION}")
        print(f"  [OK] Supported formats: {len(IMAGE_EXTENSIONS)} types")
        print(f"  [OK] Detection threshold: {DETECTION_THRESHOLD}")

        locations = get_common_locations()
        total_locations = sum(len(paths) for paths in locations.values())
        print(f"  [OK] Common locations: {total_locations} paths configured")

        return True
    except Exception as e:
        print(f"  [FAIL] Config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Inntinnsic Setup Verification")
    print("="*60)
    print()

    # Python version check
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 11):
        print("  [WARNING] Python 3.11+ recommended")
    else:
        print("  [OK] Python version is compatible")
    print()

    # Run tests
    results = []

    import_success, failed_imports = test_imports()
    results.append(("Imports", import_success))

    if import_success:
        results.append(("Config", test_config()))
        results.append(("Scanner", test_scanner()))
        results.append(("Detector", test_detector()))
    else:
        print("\n[ERROR] Cannot proceed with other tests due to import failures")
        print("\nMissing modules:")
        for module in failed_imports:
            print(f"  - {module}")
        print("\nPlease run: pipenv install")
        return False

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    all_passed = all(result for _, result in results)

    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name}")

    print()

    if all_passed:
        print("[SUCCESS] All tests passed! Your environment is ready.")
        print()
        print("Next steps:")
        print("  1. Run the application: python main.py")
        print("  2. Or use the batch file: run.bat")
        print("  3. Build standalone exe: build.bat")
        return True
    else:
        print("[FAILURE] Some tests failed. Please review errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
