# Build Instructions for Inntinnsic

This document explains how to build a standalone executable from the Inntinnsic source code.

## Prerequisites

1. **Python 3.11.9** installed
2. **Pipenv** installed (`pip install pipenv`)
3. **All dependencies** installed (`pipenv install`)
4. **Windows 10/11** (for Windows builds)

## Quick Build

The easiest way to build:

```bash
build.bat
```

This script will:
1. Activate the pipenv virtual environment
2. Run PyInstaller with the build.spec configuration
3. Clean previous build artifacts
4. Create a standalone executable in `dist/Inntinnsic/`

## Manual Build

If you prefer to build manually:

```bash
# Activate virtual environment
pipenv shell

# Clean previous builds (optional)
rmdir /s /q build dist

# Run PyInstaller
pyinstaller build.spec --clean
```

## Output Location

After building, you'll find:

```
dist/
└── Inntinnsic/
    ├── Inntinnsic.exe          # Main executable
    ├── _internal/               # Dependencies folder
    │   ├── nudenet/
    │   │   └── 320n.onnx       # AI model file (IMPORTANT!)
    │   ├── onnxruntime/
    │   └── ... other dependencies
    └── ... other files
```

## Important Files Included

The build process automatically includes:

### NudeNet Model Files
- **320n.onnx** - The ONNX model file for nudity detection (~60MB)
- Located in: `_internal/nudenet/320n.onnx`
- Collected via PyInstaller hooks

### Dependencies
- **onnxruntime** - For running the AI model
- **PIL/Pillow** - Image processing
- **tkinter** - GUI framework
- **numpy, sklearn** - NudeNet dependencies

## Build Configuration

The build is configured in [build.spec](../build.spec):

### Key Settings

```python
# Collect NudeNet model files automatically
nudenet_datas = collect_data_files('nudenet', include_py_files=False)

# Hidden imports (ensure all dependencies are included)
hiddenimports=[
    'nudenet',
    'nudenet.nudenet',
    'PIL',
    'onnxruntime',
    'onnxruntime.capi',
    'onnxruntime.capi._pybind_state',
    # ... more
]

# Use custom hooks directory
hookspath=['hooks']

# No console window (GUI app)
console=False
```

### Custom Hooks

The [hooks/hook-nudenet.py](../hooks/hook-nudenet.py) file ensures:
- NudeNet model file (320n.onnx) is included
- All NudeNet submodules are collected
- ONNX runtime dependencies are bundled

## Troubleshooting Build Issues

### Issue: "320n.onnx not found" error when running exe

**Cause:** NudeNet model file wasn't included in the build

**Solution:**
1. Verify `hooks/hook-nudenet.py` exists
2. Check `build.spec` has `hookspath=['hooks']`
3. Rebuild with `--clean` flag:
   ```bash
   pyinstaller build.spec --clean
   ```

### Issue: "onnxruntime not found" error

**Cause:** ONNX runtime DLLs not included

**Solution:**
1. Add to hidden imports in `build.spec`:
   ```python
   'onnxruntime.capi._pybind_state'
   ```
2. Rebuild

### Issue: Import errors for sklearn, numpy, etc.

**Cause:** Missing hidden imports

**Solution:**
Add the missing module to `hiddenimports` in `build.spec`

### Issue: Build is very large (>500MB)

**Explanation:** This is expected because:
- NudeNet model: ~60MB
- ONNX runtime: ~100MB
- NumPy/SciKit-Learn: ~100MB
- Other dependencies: ~100-200MB

To reduce size:
1. Use UPX compression (already enabled)
2. Exclude unused modules in `build.spec`

## Testing the Build

After building, test the executable:

### 1. Basic Launch Test
```bash
cd dist/Inntinnsic
Inntinnsic.exe
```

The application should launch without errors.

### 2. Model Loading Test
In the app:
1. Click "Quick Scan"
2. Click "Start Scan"
3. Verify the model loads (first time may take a few seconds)

### 3. Detection Test
Use a test image to verify detection works:
1. Scan a folder with known test images
2. Verify flagged images appear correctly
3. Check categories match expected detections

## Distribution

### Creating a Release Package

1. **Build the executable** (as above)
2. **Create distribution folder:**
   ```
   Inntinnsic-v1.0.2/
   ├── Inntinnsic.exe
   ├── _internal/
   ├── README.txt (copy from README.md)
   └── LICENSE.txt (if applicable)
   ```
3. **Zip the folder:**
   ```bash
   # PowerShell
   Compress-Archive -Path "dist/Inntinnsic" -DestinationPath "Inntinnsic-v1.0.2-win64.zip"
   ```

### Distribution Checklist

Before distributing:
- [ ] Test on clean Windows VM (no Python installed)
- [ ] Verify model loads correctly
- [ ] Test scanning functionality
- [ ] Check all UI elements work
- [ ] Verify export results feature
- [ ] Test with various image formats
- [ ] Run antivirus scan (false positives are common with PyInstaller)

## File Size Expectations

Typical build sizes:
- **Executable only:** ~1MB
- **Complete distribution:** 400-600MB (with all dependencies)
- **Compressed ZIP:** 150-250MB

## Advanced: One-File Build

To create a single-file executable instead of a folder:

**Warning:** Single-file builds:
- Are slower to start (extracts to temp on each run)
- May trigger antivirus false positives
- Don't work well with large model files

**Not recommended for this application** due to the large model file.

If you still want to try, modify `build.spec`:
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # Add these
    a.zipfiles,    # Add these
    a.datas,       # Add these
    [],
    name='Inntinnsic',
    onefile=True,  # Add this
    # ... rest of options
)
```

## Build Performance

Typical build times:
- **First build:** 5-10 minutes
- **Incremental build:** 2-5 minutes
- **With --clean flag:** 5-10 minutes

Factors affecting build time:
- Number of dependencies
- UPX compression (can be disabled for faster builds)
- Disk speed (SSD vs HDD)

## Version Management

Update version before building:

1. Edit [config.py](../config.py):
   ```python
   APP_VERSION = "1.0.3"  # Update this
   ```

2. Build with updated version

3. The version number will appear in the app title bar

## Platform-Specific Notes

### Windows
- Works out of the box
- No special permissions required
- May need to add firewall exception

### Other Platforms
This build.spec is configured for Windows. For other platforms:
- Linux: Modify `console=False` and test
- macOS: Additional code signing may be required

---

**Last Updated:** 2024-12-13
**Build Configuration Version:** 1.0.2
