# Inntinnsic Quick Reference

Quick reference guide for users and developers. Print this page for easy access!

---

## User Quick Reference

### First-Time Setup

1. Run `Inntinnsic.exe`
2. Click "Download Model" when prompted
3. Wait for 40 MB download to complete
4. Start scanning!

### Performing a Scan

**Quick Scan (Recommended):**
```
1. Click "Quick Scan" button
2. Click "Start Scan"
3. Wait for completion
4. Click "View Results"
```

**Custom Folders:**
```
1. Click "Add Folder"
2. Select folder(s)
3. Click "Start Scan"
4. Wait for completion
5. Click "View Results"
```

### Reviewing Results

**Actions for Each Flagged Image:**
- **Open Folder:** See file location in Windows Explorer
- **Delete:** Permanently remove file (cannot be undone!)
- **Ignore:** Remove from results but keep file

**Confidence Levels:**
- 90-100%: Very high confidence
- 70-89%: High confidence
- 60-69%: Moderate confidence (may be false positive)

### Settings Guide

**Detection Sensitivity:**
- Low (0.3-0.5): More detections, more false positives
- Medium (0.5-0.7): Balanced (default: 0.6)
- High (0.7-0.9): Fewer false positives, might miss some content

**Content Categories (Default Flagged):**
- Female Breast Exposed ✓
- Female Genitalia Exposed ✓
- Male Genitalia Exposed ✓
- Anus Exposed ✓
- Buttocks Exposed ✓
- Belly Exposed (optional)

**Content Blurring (🔞 Toggle):**
- Tap icon to toggle blur on/off
- Bright = Blur enabled (default)
- Faded = Blur disabled
- Blurs detected regions in image previews

**Scan Options:**
- Skip Hidden Files: ✓ (recommended)
- Confirm File Deletions: ✓ (recommended for safety)

### File Locations

| Item | Location |
|------|----------|
| Application | Wherever you extracted it |
| Settings | `%LOCALAPPDATA%\Inntinnsic\settings.json` |
| AI Model | `%LOCALAPPDATA%\Inntinnsic\nudenet.onnx` |
| Debug Logs | `%LOCALAPPDATA%\Inntinnsic\detection_debug.log` |

**To Access AppData:**
1. Press `Windows + R`
2. Type `%LOCALAPPDATA%\Inntinnsic`
3. Press Enter

### Supported Image Formats

✅ JPEG (.jpg, .jpeg)
✅ PNG (.png)
✅ GIF (.gif)
✅ BMP (.bmp)
✅ WebP (.webp)
✅ TIFF (.tiff, .tif)

**File Size Limits:**
- Maximum: 50 MB
- Larger files are automatically skipped

### Common Issues

| Problem | Solution |
|---------|----------|
| Model download fails | Check internet, try again later |
| Scan very slow | Reduce folders, close other apps |
| Too many false positives | Increase sensitivity to 0.7+ |
| App won't start | Run as Administrator |
| Can't delete files | Close apps using the file |

### Keyboard Shortcuts

❌ Not currently supported - use mouse/touch only

---

## Developer Quick Reference

### Project Info

**Technology Stack:**
- Framework: .NET MAUI
- Runtime: .NET 8.0
- Language: C# 12
- Platform: Windows 10/11 (x64)
- AI: ONNX Runtime 1.23.2
- Graphics: SkiaSharp 3.119.1

**Version:** 3.1.0
**Repo:** https://github.com/Kazuhma/inntinnsic
**License:** MIT

### Project Structure

```
inntinnsic/
├── Models/          # Data models
├── Services/        # Business logic
├── Views/           # UI (XAML + code-behind)
├── Resources/       # Assets, styles
├── Platforms/       # Windows-specific code
├── Docs/            # Documentation
├── Config.cs        # Configuration constants
└── *.csproj         # Project file
```

### Build Commands

```bash
# Restore dependencies
dotnet restore

# Build (Debug)
dotnet build

# Build (Release)
dotnet build -c Release

# Run
dotnet run

# Clean
dotnet clean

# Publish (self-contained)
dotnet publish -c Release -r win-x64 --self-contained
```

### Visual Studio Shortcuts

| Action | Shortcut |
|--------|----------|
| Build Solution | `Ctrl+Shift+B` |
| Run (Debug) | `F5` |
| Run (No Debug) | `Ctrl+F5` |
| Find in Files | `Ctrl+Shift+F` |
| Go to Definition | `F12` |
| Format Document | `Ctrl+K, Ctrl+D` |

### Key Files to Know

**Entry Points:**
- `MauiProgram.cs` - App initialization
- `App.xaml.cs` - Application lifecycle
- `MainPage.xaml.cs` - Main UI logic

**Core Services:**
- `Services/ImageDetector.cs` - AI inference (complex!)
- `Services/FileScanner.cs` - File discovery
- `Services/ModelDownloader.cs` - Model management

**Configuration:**
- `Config.cs` - All constants
- `Models/UserSettings.cs` - User preferences

### Code Snippets

**Progress Reporting:**
```csharp
var progress = new Progress<ScanProgress>(p =>
{
    MainThread.BeginInvokeOnMainThread(() =>
    {
        ProgressBar.Progress = p.ProgressPercentage / 100.0;
    });
});
```

**Async File Operation:**
```csharp
await Task.Run(async () =>
{
    // Background work
    var results = await ProcessFiles();

    // Update UI
    MainThread.BeginInvokeOnMainThread(() =>
    {
        StatusLabel.Text = "Complete";
    });
});
```

**Navigation:**
```csharp
// Push new page
await Navigation.PushAsync(new ResultsPage(results));

// Pop back
await Navigation.PopAsync();
```

**Display Alert:**
```csharp
await DisplayAlert("Title", "Message", "OK");

bool confirmed = await DisplayAlert(
    "Confirm",
    "Are you sure?",
    "Yes",
    "No"
);
```

### Git Workflow

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "feat: Add my feature"

# Push and create PR
git push origin feature/my-feature
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance

### Configuration Constants

**File Scanning:**
```csharp
Config.MaxFileSize              // 50 MB
Config.ImageExtensions          // .jpg, .png, etc.
Config.SkipDirectories          // System folders
```

**Detection:**
```csharp
Config.DetectionThreshold       // 0.6 (default)
Config.GetDefaultFlaggedCategories()
```

**Paths:**
```csharp
Config.GetCommonLocations()     // Quick Scan folders
```

### ONNX Model Details

**Model:** NudeNet (YOLOv8-based)
**Source:** HuggingFace (vladmandic/nudenet)
**Size:** ~40 MB
**Input:** [1, 3, 320, 320] tensor (RGB image)
**Output:** 18 content categories with bounding boxes

**Categories (18 total):**
1. FEMALE_GENITALIA_COVERED
2. FACE_FEMALE
3. BUTTOCKS_EXPOSED
4. FEMALE_BREAST_EXPOSED
5. FEMALE_GENITALIA_EXPOSED
6. MALE_BREAST_EXPOSED
7. ANUS_EXPOSED
8. FEET_EXPOSED
9. BELLY_COVERED
10. FEET_COVERED
11. ARMPITS_COVERED
12. ARMPITS_EXPOSED
13. FACE_MALE
14. BELLY_EXPOSED
15. MALE_GENITALIA_EXPOSED
16. ANUS_COVERED
17. FEMALE_BREAST_COVERED
18. BUTTOCKS_COVERED

### Debugging Tips

**Breakpoint Locations:**
```
MainPage.StartScanAsync()              // Scan start
ImageDetector.AnalyzeImageAsync()      // Per-image
FileScanner.ScanDirectoryAsync()       // File discovery
```

**View Debug Logs:**
```
Location: %LOCALAPPDATA%\Inntinnsic\detection_debug.log
```

**Common Debug Commands:**
```csharp
Debug.WriteLine($"Processing: {fileName}");
Debug.WriteLine($"Detections: {results.Count}");
```

### NuGet Packages

```xml
<PackageReference Include="Microsoft.ML.OnnxRuntime" Version="1.23.2" />
<PackageReference Include="SkiaSharp" Version="3.119.1" />
<PackageReference Include="Microsoft.WindowsAppSDK" Version="1.8.*" />
<PackageReference Include="VijayAnand.MauiToolkit" Version="3.*" />
```

### Naming Conventions

```csharp
// Classes, Methods, Properties
public class ImageDetector { }
public void AnalyzeImage() { }
public string FilePath { get; set; }

// Local variables, parameters
var imageCount = 10;
public void Process(string imagePath) { }

// Private fields
private int _totalScanned;

// Constants
public const int MaxFileSize = 50 * 1024 * 1024;
```

### Testing Checklist

Before submitting PR:
- ✅ Clean build (no warnings/errors)
- ✅ Model download works
- ✅ Scan completes successfully
- ✅ Results display correctly
- ✅ Settings save and load
- ✅ File deletion works (with confirmation)
- ✅ Edge cases tested (empty folder, access denied, cancel)

---

## Architecture Quick Reference

### Layers

```
┌─────────────────────────────┐
│  Presentation (Views)       │  XAML + Code-Behind
├─────────────────────────────┤
│  Business Logic (Services)  │  ImageDetector, FileScanner
├─────────────────────────────┤
│  Data (File System)         │  JSON, ONNX model
└─────────────────────────────┘
```

### Data Flow

```
User → MainPage → FileScanner → ImageDetector → ResultsPage
                     ↓               ↓
                 File Paths      Detections
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| MainPage | Scan orchestration, UI |
| ResultsPage | Display results, file actions |
| SettingsPage | Configuration UI |
| ImageDetector | ONNX inference |
| FileScanner | File discovery |
| ModelDownloader | Model lifecycle |

### Threading Model

- **Main Thread:** UI rendering
- **Background Threads:** Model loading, scanning, inference
- **Progress Updates:** Marshaled to main thread via `MainThread.BeginInvokeOnMainThread()`

---

## API Reference (Key Methods)

### ImageDetector

```csharp
// Load model
static Task<ImageDetector> CreateAsync()

// Single image
Task<DetectionResult> AnalyzeImageAsync(string imagePath)

// Batch with progress
Task<List<DetectionResult>> BatchAnalyzeAsync(
    IEnumerable<string> imagePaths,
    IProgress<ScanProgress> progress,
    CancellationToken cancellationToken
)
```

### FileScanner

```csharp
// Find images recursively
Task<List<string>> FindImagesAsync(
    IEnumerable<string> rootPaths,
    IProgress<(int filesFound, string currentPath)> progress,
    CancellationToken cancellationToken
)

// Get available drives
List<string> GetAvailableDrives()
```

### ModelDownloader

```csharp
// Check if model exists
static bool IsModelDownloaded()

// Download model
static Task DownloadModelAsync(IProgress<double> progress)

// Get size (for progress UI)
static Task<double> GetModelFileSizeInMB()
```

### Config

```csharp
// Detection settings
Config.DetectionThreshold                    // 0.6f
Config.GetDefaultFlaggedCategories()         // HashSet<string>

// File filtering
Config.MaxFileSize                           // 50 MB
Config.ImageExtensions                       // HashSet<string>
Config.SkipDirectories                       // HashSet<string>

// Quick Scan
Config.GetCommonLocations()                  // List<string>
```

---

## Troubleshooting Quick Reference

### Build Issues

| Error | Fix |
|-------|-----|
| Workload not found | `dotnet workload install windows` |
| NuGet restore fails | `dotnet nuget locals all --clear` |
| Native library missing | `dotnet clean && dotnet build` |

### Runtime Issues

| Problem | Fix |
|---------|-----|
| Model download fails | Check internet, firewall |
| Slow scanning | Reduce folders, close apps |
| Access denied errors | Check permissions, run as admin |
| UI freezes | Report bug (should not happen!) |

### Development Issues

| Problem | Fix |
|---------|-----|
| XAML intellisense not working | Restart Visual Studio |
| Hot reload fails | Full rebuild (`Ctrl+Shift+B`) |
| Can't attach debugger | Check project is set as startup |

---

## Performance Reference

### Typical Performance

| Metric | Value |
|--------|-------|
| Scan Speed | 100-300 images/min |
| Inference Time | 100-300ms per image (CPU) |
| Model Load Time | 1-2 seconds |
| Memory Usage | 200-500 MB |

### Optimization Opportunities

**Current Bottlenecks:**
1. CPU-only inference (no GPU)
2. Sequential processing (no parallelism)
3. Full image decoding (even for large files)

**Potential Improvements:**
- GPU acceleration (5-10x speedup)
- Parallel processing (2-4x speedup)
- Smart caching (avoid re-scanning)

---

## Resources

### Documentation

- [Technical Documentation](technical-documentation.md)
- [User Documentation](user-documentation.md)
- [System Architecture](system-architecture.md)
- [New Joiner Guide](new-joiner-guide.md)

### External Links

- [.NET MAUI Docs](https://learn.microsoft.com/en-us/dotnet/maui/)
- [ONNX Runtime Docs](https://onnxruntime.ai/docs/)
- [SkiaSharp Docs](https://learn.microsoft.com/en-us/xamarin/xamarin-forms/user-interface/graphics/skiasharp/)
- [NudeNet Model](https://github.com/vladmandic/nudenet)

### Support

- GitHub Issues: [Report bugs/features]
- GitHub Discussions: [Ask questions]
- Team Chat: [Internal link]

---

## Quick Tips

**For Users:**
- Start with Quick Scan to get familiar
- Increase sensitivity if too many false positives
- Use "Ignore" liberally - AI isn't perfect
- Keep "Confirm Deletions" enabled for safety

**For Developers:**
- Read architecture doc before making big changes
- Test on real images (not just samples)
- Add debug logs for complex logic
- Ask questions early and often

**Performance:**
- CPU-heavy during scanning
- Close other apps for faster scans
- Typical: 100-300 images/minute
- Large drives take hours (be patient!)

**Privacy:**
- All processing is local
- No data uploaded anywhere
- Scan results not saved between sessions
- Debug logs contain paths, not images

---

**Quick Reference Version:** 1.1
**Last Updated:** January 2025
**Print-Friendly:** Yes (6 pages)
