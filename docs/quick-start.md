# Quick Start Guide - Inntinnsic

## For Developers

### Setup Environment

```bash
# 1. Install dependencies using pipenv
pipenv install

# 2. Run the application
pipenv run python main.py

# Or use the batch file
run.bat
```

### First Run

The application will automatically download the NudeNet AI model (~60MB) on first run. This requires an internet connection but only happens once.

## Building Standalone Executable

```bash
# Build using the provided script
build.bat

# Or manually
pipenv shell
pyinstaller build.spec --clean
```

The executable will be in `dist/Inntinnsic/Inntinnsic.exe`

## For End Users

### Running Without Installation

1. Ensure Python 3.11.9 is installed
2. Double-click `run.bat`
3. Wait for first-run model download
4. Start scanning!

### Using the Application

**Quick Scan (Recommended for First Time)**
1. Click "Quick Scan (Common Locations)"
2. Click "Start Scan"
3. Review results

**Custom Scan**
1. Click "Add Folder" or "Select Drive"
2. Choose locations to scan
3. Optional: Check "Include system directories" for deeper scan
4. Click "Start Scan"

**Export Results**
1. After scan completes
2. Click "Export Results"
3. Save to desired location

## Typical Scan Times

- **Quick Scan** (common locations): 5-15 minutes
- **Single folder** (e.g., Downloads): 2-10 minutes
- **Entire C:\ drive**: 1-4 hours (depending on file count)

## Tips

- Start with Quick Scan to test the application
- Scan specific folders if you know where to look
- Full drive scans are thorough but time-consuming
- You can stop a scan at any time
- Results are shown in real-time as flagged images are found

## Troubleshooting

**Application won't start**
- Ensure Python 3.11.9 is installed
- Run `pipenv install` to install dependencies

**"Model failed to load"**
- Check internet connection (first run only)
- Ensure at least 500MB free disk space

**Slow scanning**
- Disable "Include system directories"
- Scan specific folders instead of entire drives

**Too many false positives**
- Edit `config.py`
- Increase `DETECTION_THRESHOLD` from 0.6 to 0.7 or 0.8

## Safety & Privacy

✅ All processing is LOCAL - nothing sent to internet
✅ No data collection or tracking
✅ Works offline after initial setup
✅ You control what gets scanned

## Need Help?

- Read the full [README.md](README.md)
- Check [config.py](config.py) for customization options
- Review source code - everything is transparent
