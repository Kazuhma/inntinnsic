# Inntinnsic System Architecture

## Document Overview

This document provides a comprehensive architectural overview of the Inntinnsic application, including high-level design decisions, component interactions, data flows, and system diagrams.

**Target Audience:** Software architects, senior developers, and technical stakeholders

---

## Table of Contents

1. [Architectural Overview](#architectural-overview)
2. [System Context](#system-context)
3. [High-Level Architecture](#high-level-architecture)
4. [Component Architecture](#component-architecture)
5. [Data Architecture](#data-architecture)
6. [Deployment Architecture](#deployment-architecture)
7. [Security Architecture](#security-architecture)
8. [Performance Architecture](#performance-architecture)
9. [Design Decisions](#design-decisions)
10. [Architecture Trade-offs](#architecture-trade-offs)

---

## Architectural Overview

### Architecture Style

Inntinnsic follows a **Layered Architecture** pattern with three primary layers:

```
┌─────────────────────────────────────┐
│     Presentation Layer              │  XAML Views + Code-Behind
├─────────────────────────────────────┤
│     Business Logic Layer            │  Services (ImageDetector, FileScanner)
├─────────────────────────────────────┤
│     Data Layer                      │  File System, JSON Persistence
└─────────────────────────────────────┘
```

### Architectural Principles

1. **Separation of Concerns:** Clear boundaries between UI, business logic, and data access
2. **Single Responsibility:** Each service has one well-defined purpose
3. **Offline-First:** No cloud dependencies after initial setup
4. **Privacy by Design:** All processing happens locally
5. **Fail-Safe:** Graceful degradation when errors occur
6. **User Control:** No automatic actions without user consent

### Technology Stack

**Platform:** .NET MAUI (Multi-platform App UI)
**Runtime:** .NET 8.0
**Language:** C# 12
**UI Framework:** XAML
**AI Engine:** ONNX Runtime 1.23.2
**Image Processing:** SkiaSharp 3.119.1

---

## System Context

### System Context Diagram

```
                           ┌─────────────────────┐
                           │   HuggingFace CDN   │
                           │  (Model Download)   │
                           └──────────┬──────────┘
                                      │ HTTPS (once)
                                      ▼
    ┌──────────────────────────────────────────────────────┐
    │                    Inntinnsic                        │
    │                                                      │
    │  ┌────────────┐  ┌──────────────┐  ┌──────────┐   │
    │  │   MAUI UI  │  │ ONNX Runtime │  │ SkiaSharp│   │
    │  └────────────┘  └──────────────┘  └──────────┘   │
    └────────┬──────────────────────────────────┬─────────┘
             │                                  │
             │ Read/Write                       │ Read/Delete
             ▼                                  ▼
    ┌────────────────────┐         ┌──────────────────────┐
    │   User AppData     │         │   File System        │
    │  %LOCALAPPDATA%    │         │  (User Folders)      │
    │  - settings.json   │         │  - Images to Scan    │
    │  - nudenet.onnx    │         │                      │
    │  - debug.log       │         │                      │
    └────────────────────┘         └──────────────────────┘
```

### External Dependencies

1. **HuggingFace Model Repository**
   - **Purpose:** One-time download of NudeNet ONNX model
   - **Protocol:** HTTPS
   - **Frequency:** Once per installation
   - **Fallback:** Manual download supported

2. **Windows File System**
   - **Purpose:** Read images for scanning, delete flagged files
   - **Access Level:** User permissions (no elevation required)
   - **Operations:** Read, enumerate, delete

3. **User AppData Directory**
   - **Purpose:** Store settings, model, logs
   - **Location:** `%LOCALAPPDATA%\Inntinnsic`
   - **Operations:** Read, write, create

---

## High-Level Architecture

### Logical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  MainPage  │  │ ResultsPage  │  │  SettingsPage    │    │
│  └─────┬──────┘  └──────┬───────┘  └────────┬─────────┘    │
└────────┼─────────────────┼──────────────────┼───────────────┘
         │                 │                  │
         │ Commands        │ Results          │ Settings
         ▼                 ▼                  ▼
┌────────────────────────────────────────────────────────────┐
│                    Business Logic                          │
│  ┌──────────────────┐  ┌─────────────┐  ┌──────────────┐ │
│  │ ImageDetector    │  │FileScanner  │  │ModelDownloader│ │
│  │                  │  │             │  │               │ │
│  │ - LoadModel()    │  │ - FindFiles │  │ - Download()  │ │
│  │ - Analyze()      │  │ - Filter    │  │ - Verify()    │ │
│  │ - BatchProcess() │  │ - Report    │  │               │ │
│  └────────┬─────────┘  └──────┬──────┘  └───────┬───────┘ │
└───────────┼────────────────────┼──────────────────┼─────────┘
            │                    │                  │
            │ ONNX Runtime       │ File System      │ HTTP Client
            ▼                    ▼                  ▼
┌────────────────────────────────────────────────────────────┐
│                     Infrastructure                         │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ ONNX Engine │  │ File System  │  │ Network (HTTPS) │  │
│  └─────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

**Presentation Layer:**
- User input handling
- Progress visualization
- Navigation between pages
- Displaying scan results

**Business Logic Layer:**
- Image analysis orchestration
- File discovery and filtering
- Model lifecycle management
- Settings persistence

**Infrastructure Layer:**
- ONNX model inference
- File system operations
- Network communication (model download)

---

## Component Architecture

### Core Components

#### 1. MainPage Component

**Responsibility:** Primary user interface for configuring and executing scans

**Key Operations:**
```
MainPage
├── EnsureModelLoadedAsync()
│   └─> ModelDownloader.IsModelDownloaded()
│   └─> ShowModelDownloadDialog()
├── OnAddFolderClicked()
│   └─> FolderPicker.PickAsync()
├── OnQuickScanClicked()
│   └─> Config.GetCommonLocations()
├── StartScanAsync()
│   └─> FileScanner.FindImagesAsync()
│   └─> ImageDetector.BatchAnalyzeAsync()
└── OnViewResultsClicked()
    └─> Navigate to ResultsPage
```

**State Management:**
- `_selectedFolders`: List of folder paths to scan
- `_lastScanResults`: DetectionResult collection from most recent scan
- `_cancellationTokenSource`: Cancellation control for ongoing scan
- `_detector`: ImageDetector instance (loaded once, reused)

**Dependencies:**
- ImageDetector (service)
- FileScanner (service)
- ModelDownloader (service)
- Config (static configuration)

#### 2. ImageDetector Service

**Responsibility:** AI-powered image analysis using ONNX model

**Component Diagram:**
```
ImageDetector
├── ONNX InferenceSession
│   ├── Model File (nudenet.onnx)
│   └── SessionOptions (CPU optimization)
├── Preprocessing Pipeline
│   ├── Image Loading (SkiaSharp)
│   ├── Resize to 320x320
│   └── Tensor Conversion (NCHW)
├── Inference Engine
│   └── Session.Run(inputs)
└── Post-processing Pipeline
    ├── Output Parsing (2 formats supported)
    ├── Confidence Filtering
    ├── Category Filtering
    └── Non-Maximum Suppression
```

**Key Algorithms:**

**Non-Maximum Suppression (NMS):**
```
Input: List of detections with bounding boxes
Output: Filtered list without duplicates

Algorithm:
1. Sort detections by confidence (descending)
2. For each detection D:
   a. Mark D as kept
   b. For each remaining detection R:
      i. Calculate IoU(D, R)
      ii. If IoU > threshold AND same category:
          - Suppress R (remove from output)
3. Return kept detections
```

**Intersection over Union (IoU):**
```
IoU(box1, box2) = Area(Intersection) / Area(Union)

Where:
  Intersection = overlap region between boxes
  Union = total area covered by both boxes
```

#### 3. FileScanner Service

**Responsibility:** Recursive file system traversal with intelligent filtering

**Filtering Pipeline:**
```
Directory Entry
    │
    ├─> Is Directory?
    │   ├─> In Skip List? → Skip
    │   ├─> Hidden & SkipHidden? → Skip
    │   └─> Recurse into directory
    │
    └─> Is File?
        ├─> Has valid extension? → Continue
        ├─> Size 0-50MB? → Continue
        ├─> Hidden & SkipHidden? → Skip
        └─> Add to results
```

**Performance Optimizations:**
1. **Early Termination:** Skip entire directories that match exclusion list
2. **Lazy Evaluation:** Use IEnumerable where possible
3. **Throttled Progress:** Report only every 100 files
4. **Exception Resilience:** Continue scan even if some folders are inaccessible

#### 4. ModelDownloader Service

**Responsibility:** Manage ONNX model lifecycle

**Download Flow:**
```
Check if Model Exists
    │
    ├─> Yes: Return immediately
    │
    └─> No: Initiate Download
        │
        ├─> Create AppData directory
        ├─> Send HTTP GET to HuggingFace
        ├─> Stream to file (report progress)
        ├─> Verify complete download
        └─> Return success
```

**Error Handling:**
- Cleanup partial downloads on failure
- Timeout after 10 minutes
- Retry logic (not implemented - user must retry manually)

---

## Data Architecture

### Data Flow Diagram

```
User Selects Folders
        │
        ▼
   FileScanner
        │
        ├─> Discover Image Files
        │   (Recursive Traversal)
        │
        ▼
   List<string> ImagePaths
        │
        ▼
   ImageDetector.BatchAnalyzeAsync()
        │
        ├─> For each image:
        │   ├─> Load Image (SkiaSharp)
        │   ├─> Preprocess to Tensor
        │   ├─> Run ONNX Inference
        │   ├─> Post-process Outputs
        │   └─> Create DetectionResult
        │
        ▼
   List<DetectionResult>
        │
        ├─> Filter to Flagged Only
        │
        ▼
   ResultsPage Display
        │
        └─> User Actions:
            ├─> Open Folder (read metadata)
            ├─> Delete (file system write)
            └─> Ignore (in-memory filter)
```

### Data Models

**DetectionResult:**
```csharp
DetectionResult {
    FilePath: string              // Absolute path
    IsFlagged: bool               // Any detection matches user categories
    Detections: List<Detection>   // All detected objects
    ScannedAt: DateTime           // Timestamp
    ErrorMessage: string          // Null if successful
}

Detection {
    Category: string              // e.g., "FEMALE_BREAST_EXPOSED"
    Confidence: float             // [0.0, 1.0]
    BoundingBox: float[4]         // [x, y, width, height]
}
```

**UserSettings:**
```csharp
UserSettings {
    DetectionSensitivity: float             // [0.3, 0.9]
    FlaggedCategories: HashSet<string>      // Active detection categories
    AutoExportResults: bool                 // Future feature flag
    SkipHiddenFiles: bool                   // Filter hidden files
    ConfirmFileDeletions: bool              // Safety prompt
}
```

### Data Persistence

**File-Based Storage:**

| Data Type | Location | Format | Lifecycle |
|-----------|----------|--------|-----------|
| User Settings | `%LOCALAPPDATA%\Inntinnsic\settings.json` | JSON | Persistent across sessions |
| ONNX Model | `%LOCALAPPDATA%\Inntinnsic\nudenet.onnx` | Binary | Persistent, downloaded once |
| Debug Logs | `%LOCALAPPDATA%\Inntinnsic\detection_debug.log` | Plain text | Append-only, never cleared |
| Scan Results | In-memory only | `List<DetectionResult>` | Cleared on new scan or app close |

**No Database:**
- Justification: Simple data model, no complex queries needed
- Trade-off: No scan history, no result export (planned for future)

---

## Deployment Architecture

### Deployment Model

**Distribution:** Self-contained Windows executable
**Installation:** Xcopy deployment (no installer required)
**Updates:** Manual download and replace

### Runtime Architecture

```
┌────────────────────────────────────────────┐
│         Windows 10/11 (x64)                │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │   Inntinnsic.exe Process             │ │
│  │                                      │ │
│  │  ┌────────────────────────────────┐ │ │
│  │  │  .NET 8.0 Runtime (bundled)    │ │ │
│  │  │                                │ │ │
│  │  │  ┌──────────────────────────┐ │ │ │
│  │  │  │  MAUI Framework          │ │ │ │
│  │  │  │  ┌────────────────────┐  │ │ │ │
│  │  │  │  │ Application Code   │  │ │ │ │
│  │  │  │  │ - Views            │  │ │ │ │
│  │  │  │  │ - Services         │  │ │ │ │
│  │  │  │  │ - Models           │  │ │ │ │
│  │  │  │  └────────────────────┘  │ │ │ │
│  │  │  └──────────────────────────┘ │ │ │
│  │  │                                │ │ │
│  │  │  ┌──────────────────────────┐ │ │ │
│  │  │  │  ONNX Runtime (native)   │ │ │ │
│  │  │  └──────────────────────────┘ │ │ │
│  │  │                                │ │ │
│  │  │  ┌──────────────────────────┐ │ │ │
│  │  │  │  SkiaSharp (native)      │ │ │ │
│  │  │  └──────────────────────────┘ │ │ │
│  │  └────────────────────────────────┘ │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

### Process Model

**Single Process:**
- Main UI thread for MAUI rendering
- Background threads for:
  - Model loading
  - Image preprocessing
  - ONNX inference
  - File system scanning

**Thread Model:**
```
Main Thread (UI)
    │
    ├─> Background Task: Model Loading
    │   └─> Returns ImageDetector instance
    │
    ├─> Background Task: File Scanning
    │   └─> Progress callbacks marshaled to UI thread
    │
    └─> Background Task: Image Analysis
        ├─> Processes images sequentially
        └─> Progress updates throttled to 200ms
```

### Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| Disk Space | 250 MB | 500 MB |
| RAM | 4 GB | 8 GB |
| CPU | Dual-core x64 | Quad-core x64 |
| OS | Windows 10 (19041) | Windows 11 |
| GPU | Not used | Not used |

**Performance Characteristics:**
- Inference Speed: ~100-300ms per image (CPU-dependent)
- Memory Usage: ~200-500 MB (depends on model and batch size)
- Disk I/O: Read-heavy during scanning, write-only for deletions

---

## Security Architecture

### Security Principles

1. **Least Privilege:** Runs as standard user, no elevation required
2. **Data Minimization:** No data collection beyond local processing
3. **Privacy by Design:** All processing local, no cloud communication
4. **User Consent:** Explicit actions required for destructive operations

### Threat Model

**In-Scope Threats:**
1. **Unintended File Deletion**
   - Mitigation: Confirmation dialog (configurable)
   - Residual Risk: User can disable confirmation

2. **Unauthorized File Access**
   - Mitigation: Relies on Windows file permissions
   - Residual Risk: If user has access, app has access

3. **False Negatives (Missing Content)**
   - Mitigation: Adjustable sensitivity
   - Residual Risk: AI is not 100% accurate

**Out-of-Scope Threats:**
1. **Network-based Attacks:** No network surface after model download
2. **Code Injection:** Trusted input (local files only)
3. **Privilege Escalation:** No admin features

### Data Privacy

**Data Classification:**

| Data Type | Sensitivity | Storage | Retention |
|-----------|-------------|---------|-----------|
| User Settings | Low | Persistent | Until user deletes |
| ONNX Model | Public | Persistent | Until user deletes |
| Scan Results | High | In-memory | Until app close |
| Debug Logs | Medium | Persistent | Manual cleanup |
| Scanned Images | High | Not copied | Original files untouched |

**Privacy Controls:**
- No telemetry or analytics
- No cloud sync
- No external API calls (except model download)
- Debug logs contain file paths but no image data

---

## Performance Architecture

### Performance Goals

| Metric | Target | Actual |
|--------|--------|--------|
| Scan Speed | 100 images/min | 100-300 images/min (CPU-dependent) |
| UI Responsiveness | < 100ms latency | Achieved via background threads |
| Model Load Time | < 5 seconds | 1-2 seconds typical |
| Memory Footprint | < 1 GB | 200-500 MB typical |

### Bottlenecks

1. **ONNX Inference (CPU-bound)**
   - Current: ~100-300ms per image on modern CPUs
   - Optimization: Add GPU support via DirectML/CUDA

2. **File System Traversal (I/O-bound)**
   - Current: ~1000 files/second metadata reads
   - Optimization: Parallel directory enumeration

3. **Image Decoding (Mixed)**
   - Current: ~20-50ms per image (SkiaSharp)
   - Optimization: Thumbnail generation for large images

### Optimization Strategies

**Implemented:**
- Background threading for long-running operations
- Throttled progress updates (200ms minimum interval)
- Smart directory filtering (skip system folders)
- File size limits (skip > 50 MB)

**Potential Future Optimizations:**
- Parallel image processing (batch N images concurrently)
- GPU acceleration for inference
- Image caching for repeat scans
- Incremental scanning (only new/modified files)

### Scalability Analysis

**Current Limits:**
- **File Count:** Tested up to 100,000+ images (works but slow)
- **Scan Duration:** ~6-8 hours for 100,000 images (CPU-dependent)
- **Memory:** Scan results stored in-memory (1 KB per flagged result)

**Scalability Concerns:**
- Large result sets (> 10,000 flagged images) may cause UI lag
- No pagination in ResultsPage (loads all results at once)

---

## Design Decisions

### Key Architectural Decisions

#### 1. Layered Architecture vs. MVVM

**Decision:** Use layered architecture with code-behind instead of full MVVM

**Rationale:**
- Simpler for small team
- Faster development iteration
- MAUI code-behind is sufficient for this application's complexity
- No need for two-way data binding complexity

**Trade-offs:**
- Less testable than MVVM (tight coupling to UI)
- Harder to reuse business logic in different UI contexts
- Acceptable given single-platform, single-UI focus

#### 2. File-Based Persistence vs. Database

**Decision:** Use JSON files for settings, in-memory for results

**Rationale:**
- Simple data model (no complex relationships)
- No query requirements (no searching, filtering, aggregation)
- Portable (no database installation)
- Privacy-focused (no persistent scan history)

**Trade-offs:**
- No scan history across sessions
- No export to CSV/JSON (planned for future)
- Acceptable given parental control use case (privacy > history)

#### 3. CPU-Only Inference vs. GPU Acceleration

**Decision:** CPU-only inference initially

**Rationale:**
- Wider hardware compatibility (all PCs have CPUs)
- Simpler deployment (no CUDA/DirectML drivers required)
- Acceptable performance for typical use cases

**Trade-offs:**
- Slower inference (~100-300ms vs ~10-30ms on GPU)
- Future enhancement: Add GPU support as optional feature

#### 4. Self-Contained vs. Framework-Dependent Deployment

**Decision:** Self-contained deployment (bundle .NET runtime)

**Rationale:**
- No .NET installation required for end users
- Guaranteed version compatibility
- Simpler user experience

**Trade-offs:**
- Larger download size (~150 MB vs ~10 MB)
- Acceptable given target audience (parents, not developers)

#### 5. Offline-First Architecture

**Decision:** All processing local, no cloud services

**Rationale:**
- Privacy-focused (parental control data is sensitive)
- No subscription/cloud costs
- Works without internet (after model download)

**Trade-offs:**
- No multi-device sync
- No cloud backup of settings
- No collaborative features
- Acceptable given privacy-first principle

#### 6. Single Window Application

**Decision:** Single window with page navigation (not multi-window)

**Rationale:**
- Simpler mental model for users
- Easier state management
- Consistent with mobile app patterns (MAUI heritage)

**Trade-offs:**
- Cannot view results and settings simultaneously
- Acceptable given sequential workflow (scan → review → act)

---

## Architecture Trade-offs

### Performance vs. Accuracy

**Current Balance:** Favor accuracy over speed

- Use full 320x320 model input (not downsampled)
- Apply NMS for duplicate removal (adds ~5-10ms)
- Sequential processing (simpler, no concurrency bugs)

**Future Adjustments:**
- Add "Fast Scan" mode (lower resolution, skip NMS)
- Parallel processing for high-end CPUs

### Privacy vs. Features

**Current Balance:** Favor privacy over features

- No cloud sync (feature sacrifice for privacy)
- No scan history (feature sacrifice for privacy)
- No telemetry (no usage analytics)

**Non-Negotiable:** Privacy principles will not be compromised

### Simplicity vs. Extensibility

**Current Balance:** Favor simplicity over extensibility

- Hard-coded model path (not pluggable architecture)
- Fixed ONNX format support (not generic inference engine)
- Direct service instantiation (not dependency injection)

**Future Adjustments:**
- Add plugin system for custom models (if requested)
- Refactor to DI container for better testability

### User Control vs. Automation

**Current Balance:** Favor user control over automation

- Manual scan initiation (no scheduled scans)
- Explicit deletion confirmation (no auto-quarantine)
- Configurable sensitivity (not auto-tuning)

**Rationale:** Trust and transparency with users

---

## Future Architecture Evolution

### Planned Enhancements

1. **GPU Acceleration Layer**
   - Add DirectML backend for Windows
   - Fallback to CPU if GPU unavailable
   - Expected: 5-10x speedup

2. **Plugin Architecture**
   - Support custom ONNX models
   - Configurable categories per model
   - Model marketplace (community models)

3. **Incremental Scanning**
   - File system watcher for real-time monitoring
   - Database for scan history
   - Only scan new/modified files

4. **Export Functionality**
   - CSV export of scan results
   - JSON export for automation
   - Report generation (PDF)

### Architecture Risks

1. **MAUI Framework Maturity**
   - Risk: MAUI is relatively new, bugs and limitations
   - Mitigation: Active community, Microsoft support
   - Contingency: Fallback to WPF if needed

2. **ONNX Model Evolution**
   - Risk: Model format changes, breaking compatibility
   - Mitigation: Version detection, format adapters
   - Contingency: Pin to specific model version

3. **Windows Platform Lock-in**
   - Risk: Hard to port to macOS/Linux later
   - Mitigation: MAUI is cross-platform by design
   - Contingency: Refactor platform-specific code to interfaces

---

## Conclusion

Inntinnsic's architecture prioritizes **privacy, simplicity, and user control** over advanced features and cloud integration. The layered architecture provides clear separation of concerns while remaining accessible to small development teams. Future enhancements will focus on performance (GPU acceleration) and extensibility (plugin models) while maintaining the core privacy-first principles.

---

**Document Version:** 1.0
**Last Updated:** December 2024
**Maintained By:** Architecture Team
