# Changelog

All notable changes to Inntinnsic will be documented in this file.

## [2.4.0] - 2024-12-14

### Fixed - Critical Scan & UI Improvements
- **Stop Scan functionality** - Stop Scan button now properly halts the scanning process
  - Implemented interrupt checking in scan progress callback
  - Raises InterruptedError when scan is stopped by user
  - Prevents overlapping scans from starting
- **Results list management** - Results now clear automatically when starting a new scan
  - Prevents memory buildup from multiple scans
  - Keeps results relevant to current scan only
- **Progress bar persistence** - Progress bar now maintains visibility when switching tabs during active scan
- **Bounding box labels on scaled images** - Detection labels now remain legible on scaled-down images
  - Draws bounding boxes after scaling image (not before)
  - Scales bbox coordinates by scale factor
  - Maintains fixed 16pt font size regardless of image scale
- **Modal window sizing** - Reduced generous margins in preview modal
  - Width padding: 40px → 20px (10px per side)
  - Height padding: 170px → 110px (tighter header/footer)

### Changed - UI Polish
- **Scanner title** - Changed "Ready to Scan" to "Scanner" for consistency
  - Increased font size from 16 to 18 to match "Scan Locations" title

### Technical
- Progress callback now checks `is_scanning` flag and raises InterruptedError to stop analysis
- Added `InterruptedError` exception handler in scan thread
- Results cleared at start of `start_scan()` method
- Progress bar visibility restored when recreating Scan tab during active scan
- Bounding box drawing refactored: scale image first, then draw boxes with scaled coordinates
- Modal sizing: `modal_width = display_width + 20`, `modal_height = display_height + 110`

---

## [2.3.3] - 2024-12-14

### Fixed - UX & Functionality Improvements
- **Stop Scan button** - Now properly stops the scan when clicked (was showing "scan already running" error)
- **Scan button persistence** - Button text now persists as "⏹️ Stop Scan" when switching tabs during active scan
- **Modal window sizing** - Preview modal now dynamically sizes to fit the image instead of fixed square dimensions
  - Calculates modal size based on image dimensions (max 1200px on long side)
  - Adds appropriate padding for header (80px), margins (40px), and text (50px)
  - Prevents image and text cropping
- **Export results flow** - Removed redundant success confirmation message after export

### Technical
- Implemented `start_or_stop_scan()` toggle method for scan button
- Added `stop_scan()` method that calls `scanner.stop()`
- Scan button command now uses toggle logic instead of direct start
- Added scan state check when recreating Scan tab to maintain button text
- Modal sizing: `modal_width = display_width + 40`, `modal_height = display_height + 170`

---

## [2.3.2] - 2024-12-14

### Changed - Final UI Refinements
- **Simplified image scaling** - Images larger than 1200px on longest side scale down to 1200px (clearer logic)
- **Removed tooltips** - Confidence badge tooltips removed (preview shows full details now)
- **Cleaner tab styling** - Removed border from active tabs, keeping only purple color and underline
- **Better resolution display** - Added "Size: " prefix and placed directly above file path (no gap)

### Technical
- Simplified scaling: `if max(width, height) > 1200: scale to 1200px on long side`
- Resolution and path now in same info container for tighter grouping
- Removed `create_tooltip()` calls on confidence badges
- Tab active state now only uses color and underline (no border)

---

## [2.3.1] - 2024-12-14

### Changed - UI Polish & Refinements
- **Icon sizes refined** - Scaled back from 20 to 18 for better balance across UI
- **Settings button** - Added "Settings" text next to gear icon (⚙️ → ⚙️ Settings)
- **Active tab styling** - Replaced bold text with purple underline and border for clearer active state
- **Button spacing** - Tightened action button spacing (padx: 2 → 1) for more compact layout
- **Image resolution display** - Added resolution (e.g., "800 x 600") above file path in viewer
- **Draggable viewer** - Modal window header is now draggable for repositioning
- **Smart image scaling** - Images below 1200px keep original size, only larger images scale down
- **Escape key fixed** - Pressing Escape now properly closes the viewer window

### Technical
- Modal window uses `focus_set()` for keyboard event handling
- Drag functionality implemented with Button-1 and B1-Motion event bindings
- Conditional scaling logic: only scale if width/height > 860/550
- Tab active state uses underline and purple border instead of bold font

---

## [2.3.0] - 2024-12-14

### Added - Image Viewer with Detection Visualization
- **Bounding boxes on preview** - View modal now draws red rectangles around detected areas
- **Detection labels** - Each bounding box shows category name and confidence percentage
- **True modal window** - Removed window decorations for cleaner, distraction-free viewing

### Changed - UI Polish
- **Larger icons** - All icons increased in size for better visibility:
  - Tab icons: 16 → 20
  - Settings gear: 24 → 28
  - Action buttons: 16 → 20 (with button size 36 → 40)
- **Cleaner delete flow** - Removed redundant success message after deletion

### Technical
- Uses PIL ImageDraw for bounding box rendering
- Draws rectangles with 4px red outline (#EF4444)
- Labels use Arial font (16pt) with red background
- Window uses `wm_overrideredirect(True)` for borderless modal

---

## [2.2.0] - 2024-12-14

### Added - Results Actions
- **View image modal** - Click eye icon 👁️ to view images in a modal dialog (press Escape or X to close)
- **Open folder button** - New folder icon 📁 opens Windows Explorer and highlights the file
- **Ignore button** - Remove items from results list without confirmation (checkmark icon ✓)
- **Delete functionality** - Delete button 🗑️ now works, removes file from disk
- **Confirm file deletions setting** - Optional confirmation dialog before deleting files (default: enabled)
- **Bigger action icons** - Increased icon size in results rows from default to size 16 (matching tab icons)

### Changed - Results UX
- All four action buttons now fully functional: View 👁️, Open Folder 📁, Delete 🗑️, Ignore ✓
- Results refresh automatically after ignore or delete actions
- Badge count updates in real-time
- File existence checked before viewing - automatically removed from list if missing

### Technical
- Image viewer uses CTkToplevel modal with proper grab_set() for modal behavior
- PIL/Pillow for image loading with automatic thumbnail scaling (max 860x550)
- Windows Explorer integration with `/select,` flag to highlight files
- Error handling for file operations with user-friendly messages
- Logging for delete operations

---

## [2.1.0] - 2024-12-14

### Added - Settings Implementation
- **Skip hidden files setting** - Now functional, filters out files starting with "."
- **Detection sensitivity setting** - Three levels implemented:
  - Low (strict): 80% threshold - only very confident detections
  - Medium (balanced): 60% threshold - balanced default
  - High (sensitive): 40% threshold - more detections, may include false positives
- **Auto-export results setting** - Automatically saves results to file after each scan if enabled
- **Bigger icons** - Increased font sizes for tab emojis and settings gear icon for better visibility

### Technical
- Updated `ImageDetector` to accept configurable threshold
- Updated `FileScanner` with `skip_hidden` property
- Scanner now respects skip hidden files setting
- Detector threshold updates dynamically based on sensitivity selection

---

## [2.0.2] - 2024-12-14

### Fixed - Tab Switching Bugs
- **Folders disappearing on tab switch** - Path chips now properly restore when returning to Scan tab
- **Scan button disabled on tab return** - Button state now properly updates when returning to Scan tab
- **Sticky tooltips** - Tooltips now properly clean up when switching tabs or hovering over different badges
- **Tooltip cleanup** - All active tooltips are now tracked and destroyed to prevent orphaned windows

---

## [2.0.1] - 2024-12-14

### Changed - UX Improvements
- **Removed "Select Drive" button** - folders can select drives too
- **Moved Settings to icon** - Cogwheel icon on right side of tab bar
- **Removed scan completion popup** - Now just plays system sound
- **Removed Quick Scan popup** - Silently adds locations
- **Removed thumbnail placeholders** - Avoids creating copies of inappropriate images
- **Fixed Clear Results bug** - Now properly clears the results list

### Added
- **Tooltips on confidence badges** - Hover to see detailed detection breakdown
- **Application icon** - Purple shield icon (icon.ico)
- **System sound** on scan completion (Windows beep)
- **Icon generator script** (create_icon.py)

### Fixed
- **Settings alignment** - Controls now properly aligned with descriptions
- **Clear results** - No longer creates duplicate empty states

---

## [2.0.0] - 2024-12-14

### Added - Modern UI Redesign
- **Complete UI overhaul** using CustomTkinter for Windows 11 Fluent Design aesthetics
- **Tab-based navigation** (Scan, Results, Settings)
- **Modern color scheme** with purple/violet branding (#7C3AED)
- **Path chips** with visual folder icons and remove buttons
- **Results badge** on Results tab showing count of flagged images
- **Empty states** with helpful messaging when no results exist
- **Result cards** with:
  - Image thumbnail placeholders
  - Confidence badges (color-coded: red 80%+, yellow 60-80%)
  - Action buttons (view, delete, mark as reviewed) - placeholders for future features
- **Settings page** with:
  - Detection sensitivity dropdown (Low/Medium/High)
  - Modern toggle switches for options
  - Clean two-column layout
- **Improved progress indication** with integrated progress bar
- **Status footer** showing current status and last scan time

### Changed
- Migrated from standard tkinter to CustomTkinter
- Improved visual hierarchy and spacing
- Better button styles with hover effects
- Rounded corners throughout the interface
- Modern typography (clearer font sizes and weights)
- Reorganized scan controls into logical sections

### Design Elements
- **Colors**: Purple primary (#7C3AED), danger red (#EF4444), warning orange (#F59E0B)
- **Typography**: Segoe UI font family (Windows default)
- **Spacing**: Consistent padding and margins
- **Components**: Modern buttons, switches, dropdowns
- **Layout**: Card-based design with rounded corners

### Technical
- Added `customtkinter` dependency
- Updated `build.spec` to include CustomTkinter
- Backed up old GUI to `gui_old.py`
- Bumped version to 2.0.0

### Placeholder Features (UI Ready, Functionality Coming Soon)
- View image button (shows preview/details)
- Delete image button (move to recycle bin)
- Mark as reviewed button (hide from results)
- Image thumbnails in results (currently showing emoji placeholder)

---

## [1.0.2] - 2024-12-14

### Fixed - Critical Detection Fix
- **Corrected NudeNet category names** to match actual v3.4+ output
- Updated from `EXPOSED_*` pattern to `*_EXPOSED` pattern
- Categories now: `ANUS_EXPOSED`, `BUTTOCKS_EXPOSED`, `FEMALE_BREAST_EXPOSED`, etc.

### Added
- PyInstaller hooks for NudeNet model bundling
- Build instructions documentation
- `hooks/hook-nudenet.py` for proper model inclusion

### Changed
- Reorganized documentation into `/docs/` directory
- Renamed docs to kebab-case format
- Updated all documentation with correct category names

---

## [1.0.1] - 2024-12-13

### Fixed
- Attempted category name fix (still incorrect - see 1.0.2)

---

## [1.0.0] - 2024-12-13

### Initial Release
- Core scanning functionality
- NudeNet AI integration
- Basic tkinter GUI
- File system scanner
- Results export
- Configuration system

---

## Versioning

- **Major version** (x.0.0): Breaking changes, major redesigns
- **Minor version** (0.x.0): New features, non-breaking changes
- **Patch version** (0.0.x): Bug fixes, documentation updates
