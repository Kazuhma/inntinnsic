"""
File system scanning module for finding images
"""
import os
from pathlib import Path
from config import IMAGE_EXTENSIONS, SKIP_DIRECTORIES, MAX_FILE_SIZE
import logging

class FileScanner:
    def __init__(self, progress_callback=None):
        """
        Initialize the file scanner

        Args:
            progress_callback: Optional callback function to report progress
        """
        self.progress_callback = progress_callback
        self.scanned_count = 0
        self.found_count = 0
        self._stop_scanning = False
        self.skip_hidden = True  # Default to skipping hidden files

    def stop(self):
        """Signal the scanner to stop"""
        self._stop_scanning = True

    def should_skip_directory(self, dir_path):
        """
        Check if a directory should be skipped

        Args:
            dir_path: Path object for the directory

        Returns:
            True if directory should be skipped
        """
        dir_name = dir_path.name

        # Skip hidden directories
        if dir_name.startswith('.'):
            return True

        # Skip directories in the skip list
        if dir_name in SKIP_DIRECTORIES:
            return True

        # Check if path contains any skip directory
        try:
            path_parts = str(dir_path).split(os.sep)
            for skip_dir in SKIP_DIRECTORIES:
                if skip_dir in path_parts:
                    return True
        except Exception:
            pass

        return False

    def is_valid_image(self, file_path):
        """
        Check if file is a valid image to process

        Args:
            file_path: Path object for the file

        Returns:
            True if file should be processed
        """
        try:
            # Skip hidden files if enabled
            if self.skip_hidden and file_path.name.startswith('.'):
                return False

            # Check extension
            if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
                return False

            # Check file size
            file_size = file_path.stat().st_size
            if file_size == 0 or file_size > MAX_FILE_SIZE:
                return False

            return True
        except (OSError, PermissionError) as e:
            logging.debug(f"Cannot access {file_path}: {e}")
            return False

    def find_images(self, paths, include_system=False):
        """
        Recursively find all image files in given paths

        Args:
            paths: List of paths to scan
            include_system: If True, scan system directories (slower, more thorough)

        Returns:
            List of Path objects for found images
        """
        image_files = []
        self._stop_scanning = False
        self.scanned_count = 0
        self.found_count = 0

        for path in paths:
            if self._stop_scanning:
                break

            path = Path(path)

            # Validate path exists
            if not path.exists():
                logging.warning(f"Path does not exist: {path}")
                if self.progress_callback:
                    self.progress_callback(f"⚠️ Path not found: {path}")
                continue

            # Handle single file
            if path.is_file():
                if self.is_valid_image(path):
                    image_files.append(path)
                    self.found_count += 1
                    if self.progress_callback:
                        self.progress_callback(f"Found: {self.found_count} images")
                continue

            # Scan directory
            try:
                for root, dirs, files in os.walk(path, topdown=True):
                    if self._stop_scanning:
                        break

                    root_path = Path(root)

                    # Filter out directories to skip
                    if not include_system:
                        dirs[:] = [d for d in dirs if not self.should_skip_directory(root_path / d)]
                    else:
                        # Even with system scan, skip some problematic directories
                        dirs[:] = [d for d in dirs if not (root_path / d).name.startswith('.')]

                    # Process files in current directory
                    for file in files:
                        if self._stop_scanning:
                            break

                        self.scanned_count += 1

                        # Update progress every 100 files
                        if self.scanned_count % 100 == 0 and self.progress_callback:
                            self.progress_callback(
                                f"Scanning... Found: {self.found_count} images (checked {self.scanned_count} files)"
                            )

                        try:
                            file_path = root_path / file
                            if self.is_valid_image(file_path):
                                image_files.append(file_path)
                                self.found_count += 1

                        except (PermissionError, OSError) as e:
                            logging.debug(f"Cannot access {file}: {e}")
                            continue

            except (PermissionError, OSError) as e:
                logging.warning(f"Cannot access directory {path}: {e}")
                if self.progress_callback:
                    self.progress_callback(f"⚠️ Access denied: {path}")

        return image_files

    def get_available_drives(self):
        """
        Get list of available drives on Windows

        Returns:
            List of drive letters (e.g., ['C:\\', 'D:\\'])
        """
        drives = []

        # Windows drive detection
        if os.name == 'nt':
            import string
            from ctypes import windll

            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drive = f"{letter}:\\"
                    if os.path.exists(drive):
                        drives.append(drive)
                bitmask >>= 1
        else:
            # For non-Windows systems, just return root
            drives = ['/']

        return drives
