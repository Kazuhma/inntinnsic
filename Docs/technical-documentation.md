# Inntinnsic Technical Documentation

## Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Core Services](#core-services)
5. [Data Models](#data-models)
6. [AI Model Integration](#ai-model-integration)
7. [File System Operations](#file-system-operations)
8. [Configuration Management](#configuration-management)
9. [UI Architecture](#ui-architecture)
10. [Build and Deployment](#build-and-deployment)
11. [Threading and Concurrency](#threading-and-concurrency)
12. [Error Handling](#error-handling)
13. [Logging and Debugging](#logging-and-debugging)

## Overview

Inntinnsic is a .NET MAUI desktop application for Windows that provides parental control functionality through AI-powered image content detection. The application uses the NudeNet ONNX model to analyze images on the local file system and flag potentially inappropriate content.

**Version:** 3.0.0
**Target Framework:** .NET 8.0
**Platform:** Windows 10.0.19041.0+
**Application ID:** com.companyname.inntinnsic

## Technology Stack

### Core Frameworks
- **.NET MAUI:** Cross-platform UI framework (Windows-only deployment)
- **.NET 8.0:** Runtime and base class libraries
- **C# 12:** Programming language with nullable reference types enabled

### Key Dependencies
- **Microsoft.ML.OnnxRuntime 1.23.2:** ONNX model inference engine
- **SkiaSharp 3.119.1:** Image processing and manipulation
- **Microsoft.WindowsAppSDK 1.8.x:** Windows platform integration
- **VijayAnand.MauiToolkit 3.x:** MAUI utility extensions

### Development Tools
- **Microsoft.Extensions.Logging.Debug 8.x:** Debug logging (DEBUG builds only)
- **Visual Studio 2022:** Recommended IDE

## Project Structure

```
d:\Dev\inntinnsic-maui/
├── Models/                      # Data models and DTOs
│   ├── DetectionResult.cs       # Image analysis results
│   └── UserSettings.cs          # Configuration persistence
├── Services/                    # Business logic layer
│   ├── ImageDetector.cs         # ONNX model inference engine
│   ├── FileScanner.cs           # File system traversal
│   └── ModelDownloader.cs       # Model file management
├── Views/                       # UI Pages (XAML + Code-behind)
│   ├── MainPage.xaml/.cs        # Primary scanning interface
│   ├── ResultsPage.xaml/.cs     # Results review interface
│   ├── SettingsPage.xaml/.cs    # Configuration interface
│   └── VersionTemplate.xaml/.cs # Version display component
├── Resources/                   # Static assets
│   ├── Colors.xaml              # Color palette
│   ├── Styles.xaml              # Global control styles
│   ├── Fonts/                   # OpenSans font files
│   └── Images/                  # SVG assets
├── Platforms/                   # Platform-specific code
│   └── Windows/                 # Windows-only implementations
├── Config.cs                    # Application constants
├── App.xaml/.cs                 # Application root
├── MainWindow.xaml/.cs          # Window configuration
├── MauiProgram.cs               # Dependency injection setup
└── Inntinnsic.csproj            # Project file
```

### Architecture Pattern
The application follows a **layered architecture**:
- **Presentation Layer:** XAML views with code-behind
- **Business Logic Layer:** Services (ImageDetector, FileScanner, ModelDownloader)
- **Data Layer:** File-based persistence (JSON settings, ONNX model)

## Core Services

### ImageDetector Service

**Location:** `Services/ImageDetector.cs`

**Responsibility:** Performs AI-powered image analysis using the NudeNet ONNX model.

#### Key Methods

```csharp
public static async Task<ImageDetector> CreateAsync()
```
- Asynchronously loads the ONNX model from disk
- Runs on a background thread to prevent UI blocking
- Initializes ONNX InferenceSession with optimizations

```csharp
public async Task<DetectionResult> AnalyzeImageAsync(string imagePath)
```
- Single image analysis entry point
- Loads image with SkiaSharp
- Preprocesses to 320x320 tensor
- Runs inference
- Post-processes outputs with NMS
- Returns DetectionResult with flagged status

```csharp
public async Task<List<DetectionResult>> BatchAnalyzeAsync(
    IEnumerable<string> imagePaths,
    IProgress<ScanProgress> progress,
    CancellationToken cancellationToken)
```
- Batch processing with progress reporting
- Cancellation support via CancellationToken
- Updates progress after each image
- Gracefully handles per-image errors

#### Internal Pipeline

**Preprocessing** (`PreprocessImage`)
1. Load image with SkiaSharp
2. Resize to 320x320 (model requirement)
3. Convert RGB to normalized float array [0, 1]
4. Rearrange to NCHW format: [1, 3, 320, 320]
5. Create DenseTensor for ONNX input

**Inference**
```csharp
var results = _session.Run(inputs);
```
- Executes ONNX model on CPU
- Configured with ORT_ENABLE_ALL optimization level

**Post-processing** (`PostprocessOutputs`)
1. Extract output tensors (handles two formats)
2. Apply confidence thresholding (default 0.6)
3. Filter by flagged categories (user-configured)
4. Run Non-Maximum Suppression (NMS)
5. Map category indices to string names

#### Model Format Support

The service handles two ONNX output formats:

**Format 1: Traditional (Primary)**
- Three separate tensors: `boxes`, `scores`, `labels`
- Direct extraction of bounding boxes and classifications

**Format 2: HuggingFace YOLOv8**
- Single tensor: [1, 22, 2100]
- 2100 anchor predictions
- 22 values per prediction: 4 bbox coords + 18 class probabilities
- Dynamically parsed with max probability extraction

#### Non-Maximum Suppression (NMS)

```csharp
private List<Detection> ApplyNMS(List<Detection> detections, float iouThreshold = 0.45f)
```

**Algorithm:**
1. Sort detections by confidence (descending)
2. For each detection:
   - Keep if not suppressed
   - Calculate IoU with all remaining detections
   - Suppress overlapping detections of the same category
3. Return filtered list

**IoU Calculation:**
```
IoU = (Intersection Area) / (Union Area)
```

### FileScanner Service

**Location:** `Services/FileScanner.cs`

**Responsibility:** Recursively discovers image files in specified directories.

#### Key Methods

```csharp
public async Task<List<string>> FindImagesAsync(
    IEnumerable<string> rootPaths,
    IProgress<(int filesFound, string currentPath)> progress,
    CancellationToken cancellationToken)
```
- Entry point for file discovery
- Processes multiple root paths
- Reports progress every 100 files
- Respects cancellation tokens

```csharp
private async Task ScanDirectoryAsync(
    string path,
    List<string> results,
    IProgress<(int filesFound, string currentPath)> progress,
    CancellationToken cancellationToken)
```
- Recursive directory traversal
- Filters by extension and file size
- Skips excluded directories and hidden files (configurable)
- Exception-resilient (continues on access denied)

#### Filtering Logic

**Extension Validation:**
```csharp
private readonly HashSet<string> _validExtensions = new() {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"
};
```

**File Size Limits:**
- Minimum: 0 bytes (skip empty files)
- Maximum: 50 MB (configurable via Config.MaxFileSize)

**Directory Exclusions:**
```csharp
SkipDirectories = {
    "$RECYCLE.BIN", "System Volume Information", "Windows",
    "Program Files", "Program Files (x86)", "ProgramData",
    "node_modules", ".git", ".venv"
};
```

**Hidden File Handling:**
- Controlled by `UserSettings.SkipHiddenFiles`
- Checks `FileAttributes.Hidden` flag

#### Performance Characteristics
- Single-threaded recursive traversal
- Lazy evaluation (can be enumerated)
- Progress updates throttled to every 100 files
- Typical throughput: ~1000 files/second (metadata checks only)

### ModelDownloader Service

**Location:** `Services/ModelDownloader.cs`

**Responsibility:** Downloads and manages the NudeNet ONNX model file.

#### Key Methods

```csharp
public static bool IsModelDownloaded()
```
- Checks if model file exists at expected path
- Path: `%LOCALAPPDATA%/Inntinnsic/nudenet.onnx`

```csharp
public static async Task DownloadModelAsync(IProgress<double> progress)
```
- Downloads from HuggingFace repository
- Source: `https://huggingface.co/vladmandic/nudenet/resolve/main/nudenet.onnx`
- Supports progress reporting (percentage)
- 10-minute timeout
- Cleanup on failure (removes partial downloads)

```csharp
public static async Task<double> GetModelFileSizeInMB()
```
- Queries model size via HTTP HEAD request
- Returns size in megabytes (approximately 40 MB)

#### Download Process
1. Create directory if not exists
2. Send GET request with buffering disabled
3. Read stream in 8192-byte chunks
4. Calculate progress percentage
5. Report progress to UI
6. Verify complete download
7. Remove file on exception

## Data Models

### DetectionResult Model

**Location:** `Models/DetectionResult.cs`

```csharp
public class Detection
{
    public string Category { get; set; }        // e.g., "FEMALE_BREAST_EXPOSED"
    public float Confidence { get; set; }       // [0.0, 1.0]
    public float[] BoundingBox { get; set; }    // [x, y, width, height]
}

public class DetectionResult
{
    public string FilePath { get; set; }
    public bool IsFlagged { get; set; }         // Any detection matches flagged categories
    public List<Detection> Detections { get; set; }
    public DateTime ScannedAt { get; set; }
    public string ErrorMessage { get; set; }    // Populated on errors
}

public class ScanProgress
{
    public int CurrentIndex { get; set; }
    public int TotalFiles { get; set; }
    public string CurrentFile { get; set; }
    public int FlaggedCount { get; set; }
    public double ProgressPercentage =>
        TotalFiles > 0 ? (double)CurrentIndex / TotalFiles * 100 : 0;
}
```

### UserSettings Model

**Location:** `Models/UserSettings.cs`

```csharp
public class UserSettings
{
    public float DetectionSensitivity { get; set; } = 0.6f;  // [0.3, 0.9]
    public HashSet<string> FlaggedCategories { get; set; }
    public bool AutoExportResults { get; set; } = false;
    public bool SkipHiddenFiles { get; set; } = true;
    public bool ConfirmFileDeletions { get; set; } = true;
}
```

**Persistence:**
- Format: Pretty-printed JSON
- Location: `%LOCALAPPDATA%/Inntinnsic/settings.json`
- Serialization: `System.Text.Json.JsonSerializer`

**Example JSON:**
```json
{
  "DetectionSensitivity": 0.6,
  "FlaggedCategories": [
    "ANUS_EXPOSED",
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_GENITALIA_EXPOSED"
  ],
  "AutoExportResults": false,
  "SkipHiddenFiles": true,
  "ConfirmFileDeletions": true
}
```

## AI Model Integration

### NudeNet Model Specifications

**Architecture:** YOLOv8-based object detector
**Source:** HuggingFace (vladmandic/nudenet)
**Size:** ~40 MB
**Input:** Single image tensor [1, 3, 320, 320]
**Output:** Bounding boxes and class probabilities

#### Detection Categories (18 total)

```csharp
private readonly Dictionary<int, string> _categoryMap = new()
{
    { 0, "FEMALE_GENITALIA_COVERED" },
    { 1, "FACE_FEMALE" },
    { 2, "BUTTOCKS_EXPOSED" },
    { 3, "FEMALE_BREAST_EXPOSED" },
    { 4, "FEMALE_GENITALIA_EXPOSED" },
    { 5, "MALE_BREAST_EXPOSED" },
    { 6, "ANUS_EXPOSED" },
    { 7, "FEET_EXPOSED" },
    { 8, "BELLY_COVERED" },
    { 9, "FEET_COVERED" },
    { 10, "ARMPITS_COVERED" },
    { 11, "ARMPITS_EXPOSED" },
    { 12, "FACE_MALE" },
    { 13, "BELLY_EXPOSED" },
    { 14, "MALE_GENITALIA_EXPOSED" },
    { 15, "ANUS_COVERED" },
    { 16, "FEMALE_BREAST_COVERED" },
    { 17, "BUTTOCKS_COVERED" }
};
```

#### Default Flagged Categories
- ANUS_EXPOSED
- BUTTOCKS_EXPOSED
- FEMALE_BREAST_EXPOSED
- FEMALE_GENITALIA_EXPOSED
- MALE_GENITALIA_EXPOSED

### Inference Pipeline

**Step 1: Image Loading**
```csharp
using var bitmap = SKBitmap.Decode(imagePath);
```

**Step 2: Preprocessing**
```csharp
// Resize to model input size
using var resizedBitmap = bitmap.Resize(
    new SKImageInfo(320, 320),
    SKFilterQuality.Medium
);

// Extract RGB pixels
var pixels = resizedBitmap.Pixels;

// Normalize to [0, 1] and convert to NCHW format
var inputArray = new float[1 * 3 * 320 * 320];
for (int i = 0; i < pixels.Length; i++) {
    var pixel = pixels[i];
    inputArray[i] = pixel.Red / 255f;                        // R channel
    inputArray[320 * 320 + i] = pixel.Green / 255f;          // G channel
    inputArray[2 * 320 * 320 + i] = pixel.Blue / 255f;       // B channel
}
```

**Step 3: Inference**
```csharp
var tensor = new DenseTensor<float>(inputArray, new[] { 1, 3, 320, 320 });
var inputs = new List<NamedOnnxValue> {
    NamedOnnxValue.CreateFromTensor(inputName, tensor)
};
var results = _session.Run(inputs);
```

**Step 4: Post-processing**
- Extract bounding boxes and scores
- Apply confidence threshold
- Filter by flagged categories
- Run NMS to remove duplicates

### Model Configuration

**ONNX SessionOptions:**
```csharp
var options = new SessionOptions {
    GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL
};
```

**Runtime:** CPU-only (no GPU acceleration currently)

## File System Operations

### Common Scan Locations

**Location:** `Config.GetCommonLocations()`

```csharp
public static List<string> GetCommonLocations()
{
    var locations = new List<string>();
    var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);

    // User folders
    locations.Add(Path.Combine(userProfile, "Downloads"));
    locations.Add(Path.Combine(userProfile, "Pictures"));
    locations.Add(Path.Combine(userProfile, "Documents"));
    locations.Add(Path.Combine(userProfile, "Desktop"));
    locations.Add(Path.Combine(userProfile, "Videos"));

    // Browser caches
    var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
    locations.Add(Path.Combine(appData, "Google\\Chrome\\User Data\\Default\\Cache"));
    locations.Add(Path.Combine(appData, "Microsoft\\Edge\\User Data\\Default\\Cache"));
    // ... Firefox, Brave, Opera, etc.

    // System temp
    locations.Add(Path.GetTempPath());
    locations.Add("C:\\Windows\\Temp");

    return locations.Where(Directory.Exists).ToList();
}
```

### Drive Enumeration

```csharp
public List<string> GetAvailableDrives()
{
    return DriveInfo.GetDrives()
        .Where(d => d.IsReady && d.DriveType == DriveType.Fixed)
        .Select(d => d.Name)
        .ToList();
}
```

### File Operations

**Delete with Confirmation:**
```csharp
private async void OnPreviewDeleteClicked(object sender, EventArgs e)
{
    bool confirmed = true;
    if (_settings.ConfirmFileDeletions) {
        confirmed = await DisplayAlert(
            "Confirm Deletion",
            $"Permanently delete this file?\\n{selected.FilePath}",
            "Delete", "Cancel"
        );
    }

    if (confirmed) {
        File.Delete(selected.FilePath);
        _results.Remove(selected);
        LoadResults();
    }
}
```

**Open in Explorer:**
```csharp
private void OnPreviewOpenFolderClicked(object sender, EventArgs e)
{
    var folder = Path.GetDirectoryName(selected.FilePath);
    Process.Start("explorer.exe", $"/select,\"{selected.FilePath}\"");
}
```

## Configuration Management

### Static Configuration (Config.cs)

```csharp
public static class Config
{
    public const float DetectionThreshold = 0.6f;
    public const long MaxFileSize = 50 * 1024 * 1024; // 50 MB

    public static readonly HashSet<string> ImageExtensions = new() {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"
    };

    public static readonly HashSet<string> SkipDirectories = new() {
        "$RECYCLE.BIN", "System Volume Information", "Windows",
        "Program Files", "Program Files (x86)", "ProgramData",
        "node_modules", ".git", ".venv"
    };

    public static HashSet<string> GetDefaultFlaggedCategories() => new() {
        "ANUS_EXPOSED",
        "BUTTOCKS_EXPOSED",
        "FEMALE_BREAST_EXPOSED",
        "FEMALE_GENITALIA_EXPOSED",
        "MALE_GENITALIA_EXPOSED"
    };
}
```

### User Settings Persistence

**Save:**
```csharp
private async void OnSaveClicked(object sender, EventArgs e)
{
    var settings = new UserSettings {
        DetectionSensitivity = (float)SensitivitySlider.Value,
        FlaggedCategories = GetSelectedCategories(),
        AutoExportResults = AutoExportCheckbox.IsChecked,
        SkipHiddenFiles = SkipHiddenCheckbox.IsChecked,
        ConfirmFileDeletions = ConfirmDeletionsCheckbox.IsChecked
    };

    var dir = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "Inntinnsic"
    );
    Directory.CreateDirectory(dir);

    var path = Path.Combine(dir, "settings.json");
    var json = JsonSerializer.Serialize(settings, new JsonSerializerOptions {
        WriteIndented = true
    });
    await File.WriteAllTextAsync(path, json);
}
```

**Load:**
```csharp
protected override async void OnAppearing()
{
    var path = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "Inntinnsic",
        "settings.json"
    );

    if (File.Exists(path)) {
        var json = await File.ReadAllTextAsync(path);
        _settings = JsonSerializer.Deserialize<UserSettings>(json);
    } else {
        _settings = new UserSettings {
            FlaggedCategories = Config.GetDefaultFlaggedCategories()
        };
    }

    LoadSettings();
}
```

## UI Architecture

### Navigation Flow

```
App.xaml.cs
  └─ MainPage (Root)
       ├─ Navigation.PushAsync(SettingsPage)
       └─ Navigation.PushAsync(ResultsPage)
```

### MVVM-Light Pattern
The application uses a simplified MVVM approach:
- **Views:** XAML files with data binding
- **Code-Behind:** Event handlers and UI logic
- **No Formal ViewModels:** State managed directly in code-behind
- **Services:** Injected via constructor or static access

### Dependency Injection

**Registration (MauiProgram.cs):**
```csharp
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    builder.UseMauiApp<App>();

    // Services (if needed)
    // builder.Services.AddSingleton<IImageDetector, ImageDetector>();

    return builder.Build();
}
```

Currently, services are instantiated directly rather than via DI.

### Resource Dictionary Hierarchy

```
App.xaml
  ├─ Resources/Colors.xaml
  └─ Resources/Styles.xaml
       └─ Style targets: Button, Label, Entry, CheckBox, etc.
```

**Example Style:**
```xml
<Style TargetType="Button">
    <Setter Property="BackgroundColor" Value="{StaticResource Primary}" />
    <Setter Property="TextColor" Value="White" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="16,12" />
    <Setter Property="FontFamily" Value="OpenSansSemiBold" />
    <Setter Property="FontSize" Value="14" />
</Style>
```

### Custom Controls

**Version Display Template:**
```xml
<!-- VersionTemplate.xaml -->
<Label Text="{Binding Version}"
       FontSize="12"
       TextColor="{StaticResource TextMuted}" />
```

**Usage:**
```xml
<ContentView>
    <local:VersionTemplate Version="3.0.0" />
</ContentView>
```

## Build and Deployment

### Build Configuration

**Release Build:**
```bash
dotnet build -c Release
```

**Publish (Self-Contained):**
```bash
dotnet publish -c Release -r win-x64 --self-contained
```

### Project Settings

```xml
<PropertyGroup>
  <TargetFrameworks>net8.0-windows10.0.19041.0</TargetFrameworks>
  <OutputType>WinExe</OutputType>
  <RuntimeIdentifier>win-x64</RuntimeIdentifier>
  <UseMaui>true</UseMaui>
  <SingleProject>true</SingleProject>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>

  <!-- App Metadata -->
  <ApplicationTitle>Inntinnsic</ApplicationTitle>
  <ApplicationId>com.companyname.inntinnsic</ApplicationId>
  <ApplicationDisplayVersion>3.0.0</ApplicationDisplayVersion>
  <ApplicationVersion>1</ApplicationVersion>

  <!-- Windows Specific -->
  <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'windows'">
    10.0.17763.0
  </SupportedOSPlatformVersion>
</PropertyGroup>
```

### NuGet Restore
```bash
dotnet restore
```

### Platform Exclusions

Non-Windows platforms are explicitly excluded:
```xml
<ItemGroup>
  <Compile Remove="**\*.Android.cs" />
  <Compile Remove="**\*.iOS.cs" />
  <Compile Remove="**\*.MacCatalyst.cs" />
  <Compile Remove="**\*.Tizen.cs" />
  <None Include="**\*.Android.cs" />
  <None Include="**\*.iOS.cs" />
  <None Include="**\*.MacCatalyst.cs" />
  <None Include="**\*.Tizen.cs" />
</ItemGroup>
```

### Output Artifacts

**Debug Build:**
- Location: `bin\Debug\net8.0-windows10.0.19041.0\win-x64\`
- Files: `Inntinnsic.exe`, DLLs, resources

**Release Build:**
- Location: `bin\Release\net8.0-windows10.0.19041.0\win-x64\publish\`
- Size: ~150 MB (with .NET runtime)
- Single folder deployment (xcopy deployment)

### Deployment Requirements

**Target System:**
- Windows 10 build 19041+ (Version 2004)
- x64 processor
- ~200 MB disk space (app + model)
- Write access to `%LOCALAPPDATA%`

**No Installation Required:**
- Self-contained deployment includes .NET runtime
- No registry modifications
- Portable (can run from any folder)

## Threading and Concurrency

### UI Thread Marshaling

**Pattern:**
```csharp
await Task.Run(async () => {
    // Background work
    var result = await LongRunningOperation();

    // Update UI
    MainThread.BeginInvokeOnMainThread(() => {
        StatusLabel.Text = "Complete";
        ProgressBar.Progress = 1.0;
    });
});
```

**MainPage Scan Progress:**
```csharp
var progress = new Progress<ScanProgress>(p => {
    var now = DateTime.Now;
    var shouldUpdate = (now - _lastUiUpdate).TotalMilliseconds >= 200;

    if (shouldUpdate) {
        MainThread.BeginInvokeOnMainThread(() => {
            ProgressBar.Progress = p.ProgressPercentage / 100.0;
            ScannedCountLabel.Text = $"{p.CurrentIndex} Images Scanned";
            FlaggedCountLabel.Text = $"{p.FlaggedCount} Flagged";
            StatusLabel.Text = Path.GetFileName(p.CurrentFile);
        });
        _lastUiUpdate = now;
    }
});
```

### Cancellation Support

**Pattern:**
```csharp
private CancellationTokenSource _cancellationTokenSource;

private async void OnStartScanClicked(object sender, EventArgs e)
{
    _cancellationTokenSource = new CancellationTokenSource();

    try {
        await PerformScanAsync(_cancellationTokenSource.Token);
    } catch (OperationCanceledException) {
        StatusLabel.Text = "Scan cancelled";
    }
}

private void OnStopScanClicked(object sender, EventArgs e)
{
    _cancellationTokenSource?.Cancel();
}
```

### Thread Safety

**ImageDetector Loading:**
```csharp
public static async Task<ImageDetector> CreateAsync()
{
    return await Task.Run(() => {
        var session = new InferenceSession(modelPath, options);
        return new ImageDetector(session);
    });
}
```

**Rationale:** Prevents UI freeze during 40 MB model load (~1-2 seconds).

## Error Handling

### Exception Handling Strategy

**Service Layer:**
```csharp
public async Task<DetectionResult> AnalyzeImageAsync(string imagePath)
{
    try {
        using var bitmap = SKBitmap.Decode(imagePath);
        // ... processing
        return new DetectionResult {
            FilePath = imagePath,
            IsFlagged = detections.Any(),
            Detections = detections,
            ScannedAt = DateTime.Now
        };
    } catch (Exception ex) {
        Debug.WriteLine($"Error analyzing {imagePath}: {ex.Message}");
        return new DetectionResult {
            FilePath = imagePath,
            ErrorMessage = ex.Message,
            ScannedAt = DateTime.Now
        };
    }
}
```

**UI Layer:**
```csharp
private async void OnStartScanClicked(object sender, EventArgs e)
{
    try {
        await StartScanAsync();
    } catch (Exception ex) {
        await DisplayAlert("Error", $"Scan failed: {ex.Message}", "OK");
        StatusLabel.Text = "Error occurred";
    }
}
```

### Graceful Degradation

**File Access Errors:**
- Skip files that cannot be read (access denied)
- Continue scanning remaining files
- Log error to debug output

**Model Download Failures:**
- Display user-friendly error message
- Cleanup partial downloads
- Allow retry

**Invalid Image Files:**
- Return DetectionResult with ErrorMessage
- Include in results but mark as error
- Do not crash the scan

## Logging and Debugging

### Debug Logging

**Location:** `%LOCALAPPDATA%/Inntinnsic/detection_debug.log`

**Example Output:**
```
[2024-01-15 14:32:15] Analyzing: C:\Users\Alice\Pictures\photo.jpg
[2024-01-15 14:32:15] Model input name: images
[2024-01-15 14:32:15] Model outputs: output0 (DenseTensor[1,22,2100])
[2024-01-15 14:32:15] Found 3 detections before NMS
[2024-01-15 14:32:15] After NMS: 2 detections
[2024-01-15 14:32:15]   - FEMALE_BREAST_EXPOSED (0.85)
[2024-01-15 14:32:15]   - FACE_FEMALE (0.72)
```

**Implementation:**
```csharp
private void LogToFile(string message)
{
    var logPath = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "Inntinnsic",
        "detection_debug.log"
    );

    var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
    File.AppendAllText(logPath, $"[{timestamp}] {message}\n");
}
```

### Visual Studio Debug Output

```csharp
Debug.WriteLine($"Scanned {count} files, found {flagged} flagged images");
```

**Conditional Compilation:**
```csharp
#if DEBUG
    builder.Logging.AddDebug();
#endif
```

### Performance Profiling

**Recommended Tools:**
- Visual Studio Diagnostics Tools
- PerfView for CPU sampling
- dotMemory for memory analysis

**Key Metrics:**
- Image preprocessing time (~20-50ms per image)
- ONNX inference time (~100-300ms per image on CPU)
- NMS overhead (~5-10ms for typical detection counts)

---

## Security Considerations

### Data Privacy
- **No Cloud Communication:** All processing is local
- **No Telemetry:** No data sent to external servers
- **In-Memory Results:** Scan results not persisted automatically
- **Debug Logs:** Contain file paths but not image data

### File System Access
- **Read Permissions:** Required for scanning
- **Write Permissions:** Only for deletion feature (user-initiated)
- **No Elevated Privileges:** Runs as standard user

### Threat Model
- **Out of Scope:** Network attacks (no network after model download)
- **In Scope:** Unintended file deletion (mitigated by confirmation dialog)

---

## Performance Optimization Opportunities

### Current Bottlenecks
1. **CPU-Only Inference:** ~100-300ms per image
   - Mitigation: Add GPU support via DirectML or CUDA
2. **Single-Threaded Processing:** Sequential image analysis
   - Mitigation: Parallelize batch processing
3. **Full Image Decoding:** Even for small previews
   - Mitigation: Generate thumbnails for ResultsPage

### Recommended Improvements
- **Parallel Processing:** Process multiple images concurrently
- **GPU Acceleration:** Use DirectML backend for ONNX Runtime
- **Incremental Results:** Display results as they're found (don't wait for completion)
- **Smart Scheduling:** Prioritize recently modified files

---

## Known Limitations

1. **Windows Only:** No macOS/Linux support
2. **No GPU Acceleration:** Inference on CPU only
3. **Fixed Model:** Cannot swap ONNX models without code changes
4. **No Batch Export:** Results not exportable to CSV/JSON
5. **No Scan History:** Previous scans not saved
6. **Limited Format Support:** 8 image formats only
7. **No Video Analysis:** Images only, no video frame extraction

---

## Future Enhancement Ideas

- Cloud sync for multi-device parental control
- Scheduled automated scans
- Email notifications for new flagged content
- Quarantine folder instead of deletion
- Category-specific confidence thresholds
- Real-time monitoring (file system watcher)
- Support for archived files (ZIP, RAR)
- Duplicate image detection
- False positive reporting mechanism

---

## Glossary

**ONNX:** Open Neural Network Exchange format for AI models
**NMS:** Non-Maximum Suppression, algorithm to remove duplicate detections
**IoU:** Intersection over Union, overlap metric for bounding boxes
**Tensor:** Multi-dimensional array used in neural network operations
**NCHW:** Tensor layout format (Batch, Channels, Height, Width)
**YOLOv8:** You Only Look Once version 8, object detection architecture
**SkiaSharp:** Cross-platform 2D graphics library

---

## References

- [.NET MAUI Documentation](https://learn.microsoft.com/en-us/dotnet/maui/)
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [NudeNet Model Repository](https://github.com/vladmandic/nudenet)
- [SkiaSharp Documentation](https://learn.microsoft.com/en-us/xamarin/xamarin-forms/user-interface/graphics/skiasharp/)

---

**Document Version:** 1.0
**Last Updated:** December 2024
**Maintained By:** Development Team
