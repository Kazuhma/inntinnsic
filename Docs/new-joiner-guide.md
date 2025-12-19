# Inntinnsic New Joiner Guide

Welcome to the Inntinnsic development team! This guide will help you get up to speed quickly and start contributing to the project.

---

## Table of Contents

1. [Welcome](#welcome)
2. [Project Overview](#project-overview)
3. [Development Environment Setup](#development-environment-setup)
4. [Codebase Orientation](#codebase-orientation)
5. [Your First Week](#your-first-week)
6. [Development Workflow](#development-workflow)
7. [Common Tasks](#common-tasks)
8. [Code Standards](#code-standards)
9. [Testing Guidelines](#testing-guidelines)
10. [Getting Help](#getting-help)

---

## Welcome

### About the Project

Inntinnsic is a Windows desktop application that helps parents monitor and protect their children from inappropriate content by scanning image files using AI-powered detection.

**Key Facts:**
- **Technology:** .NET MAUI desktop application
- **Platform:** Windows 10/11 (x64)
- **Language:** C# 12 with .NET 8.0
- **AI Model:** ONNX Runtime with NudeNet detector
- **Team Size:** Small (2-5 developers)
- **License:** Open source (to be determined)

### Team Structure

- **Product Owner:** [To be assigned]
- **Lead Developer:** [To be assigned]
- **Developers:** [Team members]
- **QA/Testing:** [To be assigned]

### Project Goals

1. Provide free, privacy-focused parental control tool
2. Maintain 100% local processing (no cloud)
3. Achieve high accuracy with minimal false positives
4. Create intuitive, accessible user interface

---

## Project Overview

### What Problem Are We Solving?

Parents need tools to protect their children from inappropriate online content, but existing solutions often:
- Cost money (subscriptions)
- Upload private data to the cloud (privacy concerns)
- Are difficult to use (complex interfaces)
- Have poor accuracy (too many false positives/negatives)

Inntinnsic addresses these issues by providing a free, local, accurate, and easy-to-use solution.

### Key Features

1. **Folder Scanning:** Recursively scan directories for image files
2. **AI Detection:** ONNX-based object detection (NudeNet model)
3. **Results Review:** Browse flagged images with confidence scores
4. **File Management:** Delete, ignore, or investigate flagged content
5. **Configurable Settings:** Adjust sensitivity and categories
6. **Privacy-First:** All processing local, no cloud communication

### Technology Choices

**Why .NET MAUI?**
- Cross-platform potential (currently Windows-only, but can expand)
- Modern framework with active support
- Familiar to C# developers
- Good performance for desktop applications

**Why ONNX Runtime?**
- Industry standard for AI model deployment
- High performance (CPU and GPU support)
- Wide model compatibility
- Active development and support

**Why SkiaSharp?**
- Cross-platform 2D graphics
- Efficient image loading and processing
- Well-documented and maintained

---

## Development Environment Setup

### Prerequisites

Before you start, ensure you have:

1. **Windows 10/11 (x64)**
   - Development machine must be Windows for MAUI desktop development

2. **Visual Studio 2022 (17.8+)**
   - Download: [https://visualstudio.microsoft.com/](https://visualstudio.microsoft.com/)
   - Edition: Community (free) or Professional/Enterprise

3. **Workloads to Install:**
   - .NET Multi-platform App UI development
   - .NET desktop development

4. **Optional Tools:**
   - Git for Windows
   - GitHub Desktop (if you prefer GUI over command line)
   - Windows Terminal (better command line experience)

### Step-by-Step Setup

#### 1. Install Visual Studio 2022

1. Download Visual Studio Installer
2. Select "Visual Studio Community 2022" (or your licensed version)
3. In the Workloads tab, check:
   - ✅ .NET Multi-platform App UI development
   - ✅ .NET desktop development
4. Click "Install" and wait (large download, ~20-30 GB)

#### 2. Verify .NET Installation

```powershell
dotnet --version
# Should output: 8.0.x or later
```

#### 3. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/[organization]/inntinnsic.git

# Or using SSH
git clone git@github.com:[organization]/inntinnsic.git

cd inntinnsic
```

#### 4. Open the Project

1. Launch Visual Studio 2022
2. Click "Open a project or solution"
3. Navigate to `inntinnsic` directory
4. Open `Inntinnsic.csproj`

#### 5. Restore NuGet Packages

Visual Studio should automatically restore packages. If not:

```powershell
dotnet restore
```

#### 6. Build the Project

**Option A: Visual Studio**
- Press `Ctrl+Shift+B` or click Build > Build Solution

**Option B: Command Line**
```powershell
dotnet build
```

You should see:
```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

#### 7. Run the Application

**Option A: Visual Studio**
- Press `F5` (Debug) or `Ctrl+F5` (Run without debugging)

**Option B: Command Line**
```powershell
dotnet run
```

**Expected Behavior:**
- Application window opens
- You're prompted to download the model (if first run)
- Main page displays with action buttons

### Common Setup Issues

#### Issue: "Workload 'net8.0-windows' not found"

**Solution:** Install Windows Desktop Runtime
```powershell
dotnet workload install windows
```

#### Issue: NuGet Package Restore Fails

**Solution:** Clear NuGet cache
```powershell
dotnet nuget locals all --clear
dotnet restore
```

#### Issue: ONNX Runtime Native Library Not Found

**Solution:** Clean and rebuild
```powershell
dotnet clean
dotnet build
```

---

## Codebase Orientation

### Project Structure

```
inntinnsic/
├── Models/                  # Data models and DTOs
│   ├── DetectionResult.cs   # AI detection results
│   └── UserSettings.cs      # Configuration model
├── Services/                # Business logic
│   ├── ImageDetector.cs     # ONNX inference engine
│   ├── FileScanner.cs       # File system traversal
│   └── ModelDownloader.cs   # Model management
├── Views/                   # UI pages (XAML + code-behind)
│   ├── MainPage.xaml        # Primary interface
│   ├── MainPage.xaml.cs     # Main page logic
│   ├── ResultsPage.xaml     # Results review
│   ├── ResultsPage.xaml.cs  # Results logic
│   ├── SettingsPage.xaml    # Settings UI
│   └── SettingsPage.xaml.cs # Settings logic
├── Resources/               # Assets and styles
│   ├── Colors.xaml          # Color definitions
│   ├── Styles.xaml          # UI styles
│   ├── Fonts/               # Font files
│   └── Images/              # Icons and graphics
├── Platforms/               # Platform-specific code
│   └── Windows/             # Windows-only code
├── Docs/                    # Documentation
│   ├── technical-documentation.md
│   ├── user-documentation.md
│   ├── system-architecture.md
│   ├── new-joiner-guide.md  # This document!
│   └── quick-reference.md
├── Config.cs                # Static configuration
├── App.xaml.cs              # Application entry point
├── MauiProgram.cs           # DI and initialization
└── Inntinnsic.csproj        # Project file
```

### Key Files to Know

**Start Here:**
1. **MauiProgram.cs** - Application initialization, dependency setup
2. **App.xaml.cs** - Application lifecycle, theme configuration
3. **MainPage.xaml.cs** - Main user interface logic (your most frequent edit)

**Core Business Logic:**
4. **Services/ImageDetector.cs** - The heart of the AI detection (complex!)
5. **Services/FileScanner.cs** - File discovery logic
6. **Config.cs** - All configuration constants (easy to modify)

**Data Models:**
7. **Models/DetectionResult.cs** - Understanding this is crucial
8. **Models/UserSettings.cs** - User preferences structure

### Code Flow: Performing a Scan

Let's trace what happens when a user clicks "Start Scan":

```
1. User clicks "Start Scan" button
   ↓
2. MainPage.OnStartScanClicked() handler triggered
   ↓
3. StartScanAsync() method called
   ↓
4. Phase 1: File Discovery
   - FileScanner.FindImagesAsync()
   - Recursively walks directory tree
   - Filters by extension, size, hidden status
   - Returns List<string> of image paths
   ↓
5. Phase 2: Image Analysis
   - ImageDetector.BatchAnalyzeAsync()
   - For each image path:
     a. Load image with SkiaSharp
     b. Preprocess to 320x320 tensor
     c. Run ONNX inference
     d. Post-process outputs (NMS, filtering)
     e. Create DetectionResult
     f. Report progress to UI
   - Returns List<DetectionResult>
   ↓
6. Results stored in _lastScanResults
   ↓
7. UI updated: "View Results" button enabled
   ↓
8. User clicks "View Results"
   ↓
9. Navigate to ResultsPage with results
   ↓
10. ResultsPage displays flagged images
```

### Important Concepts

#### ONNX Model Inference

**Input:** 320x320x3 RGB image (tensor format: NCHW)
**Output:** Bounding boxes + class probabilities
**Post-processing:** NMS to remove duplicates

**Key Code:**
```csharp
// Services/ImageDetector.cs:PreprocessImage()
var inputArray = new float[1 * 3 * 320 * 320];
// ... populate with normalized RGB values
var tensor = new DenseTensor<float>(inputArray, new[] { 1, 3, 320, 320 });
```

#### Non-Maximum Suppression (NMS)

Removes overlapping detections of the same object:

```csharp
// Services/ImageDetector.cs:ApplyNMS()
// 1. Sort by confidence
// 2. For each detection, suppress overlapping lower-confidence detections
// 3. Return filtered list
```

#### Progress Reporting

Uses `IProgress<T>` pattern for thread-safe UI updates:

```csharp
var progress = new Progress<ScanProgress>(p => {
    MainThread.BeginInvokeOnMainThread(() => {
        ProgressBar.Progress = p.ProgressPercentage / 100.0;
    });
});
```

---

## Your First Week

### Day 1: Environment Setup and Exploration

**Morning:**
- ✅ Complete development environment setup
- ✅ Successfully build and run the application
- ✅ Download the ONNX model (test first-run experience)

**Afternoon:**
- ✅ Read this new joiner guide completely
- ✅ Skim the system architecture document
- ✅ Explore the codebase (open key files, read comments)

**Homework:**
- Run a scan on your own Pictures folder
- Observe the UI flow (add folders → scan → view results)

### Day 2: Understanding the Core Services

**Tasks:**
1. Read `Services/FileScanner.cs` thoroughly
   - Understand the filtering logic
   - Trace through `ScanDirectoryAsync()` recursion
2. Read `Services/ModelDownloader.cs`
   - Simple service, good starting point
3. Start reading `Services/ImageDetector.cs`
   - Focus on public API first
   - Don't worry about ONNX details yet

**Exercise:**
- Add a debug log statement to `FileScanner.FindImagesAsync()` that prints the total file count
- Build, run, and verify you see the log output

### Day 3: Data Models and Configuration

**Tasks:**
1. Study `Models/DetectionResult.cs`
   - Understand Detection vs DetectionResult
   - Note how IsFlagged is determined
2. Study `Models/UserSettings.cs`
   - See how settings are serialized/deserialized
3. Study `Config.cs`
   - Memorize common constants (you'll use these often)

**Exercise:**
- Add a new configuration constant to `Config.cs` (e.g., `MaxConcurrentScans`)
- Reference it somewhere in the code
- Build and verify

### Day 4: UI Layer - MainPage

**Tasks:**
1. Read `Views/MainPage.xaml.cs` completely
   - Trace the scan lifecycle
   - Understand `EnsureModelLoadedAsync()`
   - Study progress reporting mechanism
2. Skim `Views/MainPage.xaml`
   - Don't worry about mastering XAML yet

**Exercise:**
- Add a new Label to MainPage.xaml that displays "Developer Mode: ON"
- Build and run - you should see your label

### Day 5: First Code Contribution

**Tasks:**
1. Pick a "good first issue" from GitHub Issues
   - Look for labels: `good-first-issue`, `documentation`, `enhancement`
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Suggested First Issues:**
- Add a new color to `Resources/Colors.xaml`
- Improve a comment in `ImageDetector.cs`
- Add a configuration option to `Config.cs`

---

## Development Workflow

### Branching Strategy

We use **Git Flow** (simplified):

```
main (production-ready)
  ├── develop (integration branch)
       ├── feature/your-feature-name
       ├── bugfix/issue-123
       └── hotfix/critical-fix
```

**Creating a Feature Branch:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-export-functionality
```

**Committing Changes:**
```bash
git add .
git commit -m "feat: Add CSV export functionality to ResultsPage"
```

**Pushing and Creating PR:**
```bash
git push origin feature/add-export-functionality
# Then create Pull Request on GitHub
```

### Commit Message Convention

We follow **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance (dependencies, build config)

**Examples:**
```
feat(scanner): Add support for HEIC image format

Implemented HEIC image decoding using ImageSharp.
Updated FileScanner to recognize .heic extension.

Closes #45
```

```
fix(detector): Correct NMS IoU threshold calculation

Previous implementation used wrong axis for intersection.
Updated to properly calculate overlap area.

Fixes #78
```

### Code Review Process

1. **Self-Review:** Before submitting PR, review your own changes
2. **Automated Checks:** CI/CD runs build and tests (if configured)
3. **Peer Review:** At least one team member must approve
4. **Address Feedback:** Make requested changes
5. **Merge:** Squash and merge into develop

### Release Process

1. **Feature Freeze:** Stop adding new features
2. **Testing:** QA testing on release branch
3. **Bug Fixes:** Fix critical issues only
4. **Tag Release:** `git tag v3.1.0`
5. **Build Release:** Create self-contained Windows build
6. **Publish:** Upload to GitHub Releases
7. **Merge to Main:** Merge release branch to main

---

## Common Tasks

### Adding a New UI Page

1. **Create XAML file:**
   ```xml
   <!-- Views/NewPage.xaml -->
   <ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
                x:Class="Inntinnsic.Views.NewPage">
       <Label Text="New Page" />
   </ContentPage>
   ```

2. **Create code-behind:**
   ```csharp
   // Views/NewPage.xaml.cs
   namespace Inntinnsic.Views;

   public partial class NewPage : ContentPage
   {
       public NewPage()
       {
           InitializeComponent();
       }
   }
   ```

3. **Add navigation:**
   ```csharp
   // MainPage.xaml.cs
   await Navigation.PushAsync(new NewPage());
   ```

### Adding a New Configuration Option

1. **Add to Config.cs:**
   ```csharp
   public const int MaxConcurrentScans = 3;
   ```

2. **Use in code:**
   ```csharp
   var semaphore = new SemaphoreSlim(Config.MaxConcurrentScans);
   ```

### Adding a New Detection Category

1. **Update category map in ImageDetector.cs:**
   ```csharp
   private readonly Dictionary<int, string> _categoryMap = new()
   {
       // ... existing categories
       { 18, "NEW_CATEGORY_NAME" }
   };
   ```

2. **Add to Config.cs default categories (if should be flagged by default):**
   ```csharp
   public static HashSet<string> GetDefaultFlaggedCategories() => new()
   {
       // ... existing
       "NEW_CATEGORY_NAME"
   };
   ```

3. **Update SettingsPage.xaml to add checkbox:**
   ```xml
   <CheckBox x:Name="NewCategoryCheckbox" />
   <Label Text="New Category" />
   ```

### Debugging Tips

**Breakpoint Locations:**
- `MainPage.StartScanAsync()` - Start of scan process
- `ImageDetector.AnalyzeImageAsync()` - Per-image analysis
- `FileScanner.ScanDirectoryAsync()` - Directory traversal

**Debugging ONNX Inference:**
```csharp
// Add to ImageDetector.cs after inference
Debug.WriteLine($"Model outputs: {string.Join(", ", results.Select(r => $"{r.Name} [{string.Join(",", r.GetTensorDataAsSpan<float>().Length)}]"))}");
```

**View Debug Logs:**
- Location: `%LOCALAPPDATA%\Inntinnsic\detection_debug.log`
- Open in Notepad or VS Code

---

## Code Standards

### C# Style Guidelines

**Naming Conventions:**
```csharp
// Classes, Methods, Properties: PascalCase
public class ImageDetector { }
public void AnalyzeImage() { }
public string FilePath { get; set; }

// Local variables, parameters: camelCase
var imageCount = 10;
public void Process(string imagePath) { }

// Private fields: _camelCase (underscore prefix)
private int _totalScanned;
private ImageDetector _detector;

// Constants: PascalCase
public const int MaxFileSize = 50 * 1024 * 1024;
```

**Bracing Style:**
```csharp
// Always use braces, even for single-line if statements
if (condition)
{
    DoSomething();
}

// Opening brace on new line (Allman style)
public void Method()
{
    // code
}
```

**Null Handling:**
```csharp
// Use nullable reference types
public string? ErrorMessage { get; set; }

// Null-conditional operators
var length = imagePath?.Length ?? 0;

// Null-coalescing
var settings = LoadSettings() ?? new UserSettings();
```

**Async/Await:**
```csharp
// Always await async methods (don't use .Result or .Wait())
var results = await AnalyzeImageAsync(path);

// Use Async suffix for async methods
public async Task<DetectionResult> AnalyzeImageAsync(string path)
{
    // implementation
}
```

### XAML Style Guidelines

**Indentation:**
```xml
<Grid>
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto" />
    </Grid.RowDefinitions>
    <Label Text="Example" />
</Grid>
```

**Naming:**
```xml
<!-- Use x:Name for elements you reference in code-behind -->
<Button x:Name="StartScanButton" Text="Start" />
```

### Documentation Standards

**XML Comments for Public APIs:**
```csharp
/// <summary>
/// Analyzes an image file for potentially inappropriate content.
/// </summary>
/// <param name="imagePath">Absolute path to the image file.</param>
/// <returns>Detection result with flagged status and detections.</returns>
public async Task<DetectionResult> AnalyzeImageAsync(string imagePath)
{
    // implementation
}
```

**Inline Comments:**
```csharp
// Use comments to explain "why", not "what"

// BAD: Increment counter
count++;

// GOOD: Track total processed for progress reporting
count++;
```

---

## Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test:

1. **Build Verification:**
   - ✅ Clean build (`dotnet clean && dotnet build`)
   - ✅ No warnings or errors
   - ✅ Application runs

2. **Functional Testing:**
   - ✅ Model downloads successfully (delete and re-download)
   - ✅ Folder selection works
   - ✅ Quick Scan populates common folders
   - ✅ Scan progresses and completes
   - ✅ Results display correctly
   - ✅ Settings save and load
   - ✅ File deletion works (with confirmation)

3. **Edge Cases:**
   - ✅ Scan with 0 images (folder with no images)
   - ✅ Scan with huge image (> 50 MB, should be skipped)
   - ✅ Scan with inaccessible folder (access denied)
   - ✅ Stop scan mid-process (cancellation)

### Unit Testing (Future)

Currently, the project has no automated tests. We're planning to add:

**Priority 1:**
- Unit tests for `FileScanner` (filtering logic)
- Unit tests for `ModelDownloader` (mocking HTTP)

**Priority 2:**
- Integration tests for `ImageDetector` (requires test images)
- UI tests for `MainPage` (MAUI testing framework)

**How You Can Help:**
- Propose testing strategy
- Write first unit tests
- Set up CI/CD with test runner

---

## Getting Help

### Internal Resources

1. **Documentation:**
   - Technical Documentation (deep dive)
   - System Architecture (big picture)
   - This guide (getting started)

2. **Code Comments:**
   - Most complex functions have detailed comments
   - Check `ImageDetector.cs` for ONNX examples

3. **Team Communication:**
   - Daily standup (time TBD)
   - Slack/Discord channel (link TBD)
   - Weekly team sync (time TBD)

### External Resources

**MAUI Documentation:**
- Official Docs: [https://learn.microsoft.com/en-us/dotnet/maui/](https://learn.microsoft.com/en-us/dotnet/maui/)
- Samples: [https://github.com/dotnet/maui-samples](https://github.com/dotnet/maui-samples)

**ONNX Runtime:**
- Docs: [https://onnxruntime.ai/docs/](https://onnxruntime.ai/docs/)
- C# API: [https://onnxruntime.ai/docs/api/csharp/api/](https://onnxruntime.ai/docs/api/csharp/api/)

**SkiaSharp:**
- Docs: [https://learn.microsoft.com/en-us/xamarin/xamarin-forms/user-interface/graphics/skiasharp/](https://learn.microsoft.com/en-us/xamarin/xamarin-forms/user-interface/graphics/skiasharp/)

**NudeNet Model:**
- Repository: [https://github.com/vladmandic/nudenet](https://github.com/vladmandic/nudenet)

### Asking Questions

**Before Asking:**
1. Check documentation (this guide, technical docs)
2. Search codebase for examples (`Ctrl+Shift+F` in Visual Studio)
3. Read relevant source file comments

**When Asking:**
1. Provide context (what are you trying to do?)
2. Share what you've tried
3. Include error messages (full stack trace)
4. Mention your development environment (OS, VS version)

**Where to Ask:**
- Team chat for quick questions
- GitHub Issues for bugs/features
- PR comments for code-specific questions

---

## Next Steps

### End of Week 1

By the end of your first week, you should:
- ✅ Have a working development environment
- ✅ Understand the project structure
- ✅ Know where to find key files
- ✅ Have made your first code contribution (even if tiny)
- ✅ Feel comfortable asking questions

### Month 1 Goals

- Contribute to 2-3 features or bug fixes
- Review pull requests from teammates
- Understand the ONNX inference pipeline
- Propose improvements to the codebase

### Month 3 Goals

- Own a feature area (e.g., UI, file scanning, settings)
- Mentor new team members
- Contribute to architectural decisions
- Help with release planning

---

## Welcome to the Team!

We're excited to have you join us in building Inntinnsic. This project makes a real difference in helping families stay safe online. Your contributions matter!

**Remember:**
- Ask questions early and often
- No question is too small
- Code reviews are learning opportunities (both ways)
- We value quality over speed
- Work-life balance is important

Happy coding!

---

**Document Version:** 1.0
**Last Updated:** December 2024
**Maintained By:** Development Team
