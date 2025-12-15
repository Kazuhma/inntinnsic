"""
Inntinnsic - Image Safety Checker
Main entry point for the application
"""
import sys
import os

# Ensure the application can find modules when run as a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Add to path
sys.path.insert(0, application_path)

from gui import main

if __name__ == "__main__":
    main()
