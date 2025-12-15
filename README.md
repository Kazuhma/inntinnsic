# Inntinnsic - Image Safety Checker

A standalone Windows application for detecting potentially inappropriate images on your computer. Designed to help parents keep their children safe by scanning for images containing nudity.

**📚 Documentation:**
- [Quick Start Guide](docs/quick-start.md) - Fast setup and usage
- [Project Summary](docs/project-summary.md) - Technical architecture overview
- [Category Fix Notes](docs/category-fix.md) - Important detection category information

## Features

### v2.0 - Modern UI
- **Modern Windows 11 Design**: Beautiful interface built with CustomTkinter
- **Tab-Based Navigation**: Scan, Results, and Settings tabs for organized workflow
- **Visual Feedback**: Real-time progress tracking with modern progress bars
- **Smart Organization**: Path chips, result cards, and intuitive controls
- **Settings Panel**: Easily configure detection sensitivity and scan options

### Core Functionality
- **AI-Powered Detection**: Uses NudeNet deep learning model for accurate image classification
- **Flexible Scanning**:
  - Scan specific folders
  - Scan entire drives
  - Quick scan of common locations (Downloads, Pictures, Documents, browser caches)
- **Thorough Coverage**: Optional inclusion of system directories and browser caches
- **Export Results**: Save scan results to text file for review
- **Privacy-Focused**: All processing happens locally on your computer - no data sent to cloud

## Installation

### Option 1: Run from Source (Requires Python)

1. Install Python 3.11.9 from [python.org](https://www.python.org/downloads/)
2. Install pipenv: `pip install pipenv`
3. Clone or download this repository
4. Open terminal in the project directory
5. Run:
   ```bash
   pipenv install
   pipenv shell
   python main.py
   ```

### Option 2: Standalone Executable (No Python Required)

1. Download the latest release from the releases page
2. Extract the ZIP file
3. Run `Inntinnsic.exe`

## Building Standalone Executable

To build the standalone executable yourself:

```bash
# Using the batch file (Windows)
build.bat

# Or manually
pipenv shell
pyinstaller build.spec --clean
```

The executable will be created in `dist/Inntinnsic/Inntinnsic.exe`

## Usage

### First Run

On first run, the application will download the AI detection model (~60MB). This is a one-time download and will be cached for future use.

### Scanning

1. **Select Locations to Scan**:
   - Click "Add Folder" to choose specific directories
   - Click "Select Drive" to scan an entire drive (C:\, D:\, etc.)
   - Click "Quick Scan" to automatically add common locations:
     - Downloads folder
     - Pictures folder
     - Documents folder
     - Desktop
     - Browser caches (Chrome, Edge, Firefox, Brave, Opera)
     - Temp directories

2. **Configure Options**:
   - Check "Include system directories and caches" for more thorough scanning
   - Note: This makes scanning slower but more comprehensive

3. **Start Scan**:
   - Click "Start Scan" button
   - Monitor progress in the progress bar
   - Flagged images will appear in real-time in the results panel

4. **Review Results**:
   - Each flagged image shows:
     - Full file path
     - Detection category (e.g., "Exposed Genitalia")
     - Confidence level (percentage)
   - Click "Export Results" to save findings to a text file

### Understanding Results

The detector categorizes findings into these explicit categories (by default):
- **Anus Exposed**
- **Buttocks Exposed**
- **Female Breast Exposed**
- **Female Genitalia Exposed**
- **Male Genitalia Exposed**

Confidence threshold is set at 60% by default. Higher percentages indicate higher certainty.

**Note:** You can customize which categories to flag by editing `FLAGGED_CATEGORIES` in [config.py](config.py). For stricter filtering, you can also add covered categories like `FEMALE_BREAST_COVERED`, `BUTTOCKS_COVERED`, or `FEMALE_GENITALIA_COVERED`.

### Important Notes

- **False Positives**: AI detection isn't perfect. Medical images, art, or beach photos may be flagged
- **Performance**: Scanning large drives may take considerable time
- **Privacy**: All processing is done locally - images never leave your computer
- **Permissions**: The app needs read access to directories you're scanning

## Technical Details

### Detection Model

Uses [NudeNet](https://github.com/notAI-tech/NudeDetector), an open-source deep learning model trained to detect nudity in images.

### Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- WebP
- TIFF

### System Requirements

- **OS**: Windows 10/11
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for application and model files
- **Processor**: Any modern CPU (GPU not required)

## Project Structure

```
inntinnsic/
├── main.py                 # Entry point
├── scanner.py              # File system scanning logic
├── detector.py             # AI model inference
├── gui.py                  # User interface
├── config.py              # Settings and configuration
├── build.spec             # PyInstaller configuration
├── build.bat              # Build script for Windows
├── requirements.txt       # Python dependencies
├── Pipfile                # Pipenv configuration
└── README.md              # This file
```

## Configuration

You can modify `config.py` to adjust:

- **Detection Threshold**: `DETECTION_THRESHOLD` (0.0 - 1.0)
  - Lower = more sensitive (more false positives)
  - Higher = less sensitive (may miss some content)

- **Flagged Categories**: Edit `FLAGGED_CATEGORIES` list to customize what gets flagged

- **Max File Size**: `MAX_FILE_SIZE` - skip very large files

- **Skip Directories**: `SKIP_DIRECTORIES` - directories to always skip

### Testing Category Detection

If you want to verify which categories NudeNet detects in a specific image:

```bash
pipenv run python test_categories.py <path_to_image>
```

This will show you:
- Exact category names the model returns
- Whether your config.py categories match
- All available NudeNet categories for reference

## Troubleshooting

### "Model failed to load"
- Ensure you have internet connection on first run (to download model)
- Check available disk space (~500MB needed)

### "Access Denied" errors
- Run as administrator if scanning system directories
- Some directories are protected by Windows

### Slow scanning
- Disable "Include system directories" option
- Scan specific folders instead of entire drives
- Close other applications to free up resources

### False positives
- Increase `DETECTION_THRESHOLD` in config.py
- Review flagged images manually

## Privacy & Security

- **No Cloud Processing**: All detection happens locally on your computer
- **No Data Collection**: The app doesn't send any data anywhere
- **No Internet Required**: After initial model download, works completely offline
- **Open Source**: You can review all source code

## Legal & Ethical Considerations

This tool is designed for:
- **Parental control** on family computers
- **Personal device monitoring**
- **Authorized security audits**

**Do NOT use to**:
- Monitor others without consent
- Violate privacy laws
- Access unauthorized systems

Always ensure you have legal authority to scan the systems and directories you're checking.

## License

This project uses the NudeNet model which is licensed under GPL-3.0. See NudeNet repository for details.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions

## Acknowledgments

- [NudeNet](https://github.com/notAI-tech/NudeDetector) for the detection model
- Python community for excellent libraries

---

**Version**: 1.0.0
**Name Origin**: "Inntinnsic" inspired by the truth-sayers from Fourth Wing - seeking truth to protect what matters most.
