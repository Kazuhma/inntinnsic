"""
Configuration settings for Inntinnsic Image Safety Checker
"""
import os
from pathlib import Path

# Application metadata
APP_NAME = "Inntinnsic"
APP_VERSION = "2.4.0"
APP_DESCRIPTION = "Image Safety Checker for Parental Control"

# Supported image formats
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}

# Detection threshold (0.0 - 1.0, higher = more strict)
# 0.6 is a balanced default - increase for fewer false positives
DETECTION_THRESHOLD = 0.6

# Categories to flag (NudeNet provides these classifications)
# These are the ACTUAL category names from NudeNet v3.4+ (verified from PyPI)
FLAGGED_CATEGORIES = [
    'ANUS_EXPOSED',                    # Exposed anus
    'BUTTOCKS_EXPOSED',                # Exposed buttocks
    'FEMALE_BREAST_EXPOSED',           # Exposed female breast
    'FEMALE_GENITALIA_EXPOSED',        # Exposed female genitalia
    'MALE_GENITALIA_EXPOSED',          # Exposed male genitalia
]

# Note: For stricter filtering, you can also add covered/partial categories:
# FLAGGED_CATEGORIES = [
#     'ANUS_EXPOSED',
#     'ANUS_COVERED',
#     'BUTTOCKS_EXPOSED',
#     'BUTTOCKS_COVERED',
#     'FEMALE_BREAST_EXPOSED',
#     'FEMALE_BREAST_COVERED',
#     'FEMALE_GENITALIA_EXPOSED',
#     'FEMALE_GENITALIA_COVERED',
#     'MALE_GENITALIA_EXPOSED',
#     'MALE_BREAST_EXPOSED',
# ]

# Windows-specific quick access locations
def get_common_locations():
    """Returns commonly used directories that may contain images"""
    user_home = Path.home()
    locations = {
        'User Folders': [
            user_home / "Downloads",
            user_home / "Pictures",
            user_home / "Documents",
            user_home / "Desktop",
            user_home / "Videos",
        ],
        'Browser Caches': [
            user_home / "AppData/Local/Google/Chrome/User Data/Default/Cache",
            user_home / "AppData/Local/Google/Chrome/User Data/Default/Cache/Cache_Data",
            user_home / "AppData/Local/Microsoft/Edge/User Data/Default/Cache",
            user_home / "AppData/Local/Microsoft/Edge/User Data/Default/Cache/Cache_Data",
            user_home / "AppData/Roaming/Mozilla/Firefox/Profiles",
            user_home / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache",
            user_home / "AppData/Local/Opera Software/Opera Stable/Cache",
        ],
        'System Temp': [
            Path(os.getenv('TEMP', user_home / 'AppData/Local/Temp')),
            Path("C:/Windows/Temp"),
        ],
        'Common App Locations': [
            user_home / "AppData/Local/Packages",
            user_home / "AppData/Local/Microsoft/Windows/INetCache",
        ]
    }
    return locations

# Directories to skip (for performance and to avoid system issues)
SKIP_DIRECTORIES = {
    '$RECYCLE.BIN',
    'System Volume Information',
    'Windows',
    'Program Files',
    'Program Files (x86)',
    'ProgramData',
    'AppData/Local/Application Data',  # Circular symlink
    'AppData/Local/History',  # Circular symlink
    'node_modules',
    '.git',
    '.venv',
    'venv',
}

# Maximum file size to process (in bytes) - skip very large files
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# Logging configuration
LOG_FILE = Path.home() / "AppData/Local/Inntinnsic/scan_log.txt"
