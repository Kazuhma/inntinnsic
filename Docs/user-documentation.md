# Inntinnsic User Documentation

## Welcome to Inntinnsic

Inntinnsic is a powerful image safety checker designed to help parents monitor and protect their children from inappropriate content. Using advanced AI technology, Inntinnsic scans your computer's image files and identifies potentially concerning content with high accuracy.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installing Inntinnsic](#installing-inntinnsic)
3. [First-Time Setup](#first-time-setup)
4. [Performing Your First Scan](#performing-your-first-scan)
5. [Understanding Scan Results](#understanding-scan-results)
6. [Managing Flagged Images](#managing-flagged-images)
7. [Configuring Settings](#configuring-settings)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### System Requirements

Before installing Inntinnsic, ensure your computer meets these requirements:

- **Operating System:** Windows 10 (Version 2004 or later) or Windows 11
- **Processor:** 64-bit (x64) processor
- **Disk Space:** At least 250 MB of free space
- **Memory:** 4 GB RAM (minimum), 8 GB recommended
- **Internet Connection:** Required for initial setup only

### What Inntinnsic Does

Inntinnsic helps you:
- Scan folders and drives for image files
- Identify potentially inappropriate content using AI
- Review flagged images in a safe, organized interface
- Take action on concerning content (delete, ignore, or investigate)
- Configure sensitivity levels to match your family's needs

### Privacy and Security

Inntinnsic is designed with privacy in mind:
- **100% Local Processing:** All scanning happens on your computer
- **No Cloud Upload:** Your images never leave your device
- **No Internet After Setup:** Only required to download the AI model once
- **No Tracking:** We don't collect any data about you or your files

---

## Installing Inntinnsic

### Download and Setup

1. **Download** the latest version of Inntinnsic from the official release page
2. **Extract** the ZIP file to a location of your choice (e.g., `C:\Program Files\Inntinnsic`)
3. **Run** `Inntinnsic.exe` to launch the application

**Note:** Inntinnsic is portable - you can run it from any folder without installation.

### Portable Application

Inntinnsic doesn't require traditional installation:
- No registry modifications
- No administrator privileges needed
- Can be run from a USB drive
- Easy to uninstall (just delete the folder)

---

## First-Time Setup

### Initial Model Download

When you first launch Inntinnsic, it needs to download its AI detection model.

1. **Launch the Application:** Double-click `Inntinnsic.exe`
2. **Model Download Prompt:** You'll see a message that the detection model is missing
3. **Click "Download Model"** to begin the download
4. **Wait for Completion:** The model is approximately 40 MB and takes 1-5 minutes depending on your connection
5. **Progress Bar:** Track the download progress in real-time

**Important:** This download only happens once. After the model is downloaded, Inntinnsic works completely offline.

### Understanding the Interface

After setup, you'll see the main screen with four key sections:

1. **Action Buttons (Top):**
   - Add Folder: Select specific folders to scan
   - Quick Scan: Scan common locations automatically
   - Settings: Configure detection preferences

2. **Selected Folders:** View and manage folders you've chosen to scan

3. **Scan Status:** Monitor scan progress and view results

4. **Statistics Cards:** See real-time scanning statistics

---

## Performing Your First Scan

### Quick Scan (Recommended for Beginners)

The easiest way to start is with a Quick Scan:

1. **Click "Quick Scan"** button on the main screen
2. **Review Common Locations:** Inntinnsic automatically selects frequently used folders:
   - Downloads
   - Pictures
   - Documents
   - Desktop
   - Videos
   - Browser cache folders (Chrome, Edge, Firefox, etc.)
   - Temporary folders

3. **Click "Start Scan"** to begin
4. **Wait for Completion:** The scan time depends on how many images you have (typically 5-30 minutes)
5. **View Results:** Click "View Results" when the scan completes

### Custom Folder Scan

For more control, select specific folders:

1. **Click "Add Folder"** button
2. **Browse to a Folder:** Use the Windows folder picker to select a directory
3. **Add Multiple Folders:** Repeat to add more locations
4. **Remove Folders:** Click the X button next to any folder to remove it
5. **Clear All:** Use "Clear All" to start over
6. **Click "Start Scan"**

### Understanding Scan Progress

While scanning, you'll see:
- **Progress Bar:** Visual indicator of completion percentage
- **Images Scanned:** Total count of images processed
- **Flagged:** Number of images that triggered the detector
- **Current Status:** Which file is being scanned right now

### Stopping a Scan

You can stop a scan at any time:
- **Click "Stop Scan"** (red button that replaces "Start Scan")
- Results for already-scanned images will be preserved
- You can view partial results immediately

---

## Understanding Scan Results

### Results Overview

After a scan completes:

1. **Summary:** See total flagged images at the top
2. **Results List (Left Side):** Scrollable list of all flagged images
3. **Preview Area (Right Side):** View selected image and its details
4. **Confidence Score:** How certain the AI is about the detection (higher = more confident)

### Confidence Levels

Each flagged image shows a confidence percentage:

- **90-100%:** Very high confidence - likely requires attention
- **70-89%:** High confidence - worth reviewing
- **60-69%:** Moderate confidence - may include false positives
- **Below 60%:** Not flagged (filtered out by default)

**Note:** You can adjust the sensitivity threshold in Settings to change what gets flagged.

### Reviewing Flagged Images

To review a flagged image:

1. **Click on an Image** in the results list
2. **Preview Appears** on the right side
3. **Read Details:** Check the filename and confidence score
4. **Take Action:** Use the action buttons (explained below)

---

## Managing Flagged Images

### Available Actions

For each flagged image, you have three options:

#### 1. Open Folder
- **Purpose:** See where the file is located on your computer
- **How:** Click the "Open Folder" button
- **Result:** Windows File Explorer opens with the file highlighted
- **Use Case:** Investigate context (is this in an app cache? A downloads folder?)

#### 2. Delete File
- **Purpose:** Permanently remove the file from your computer
- **How:** Click the "Delete" button
- **Confirmation:** By default, you'll be asked to confirm (can be disabled in Settings)
- **Result:** File is permanently deleted (not sent to Recycle Bin)
- **Warning:** This action cannot be undone!

#### 3. Ignore
- **Purpose:** Remove from current results without deleting the file
- **How:** Click the "Ignore" button
- **Result:** Image disappears from results list but stays on your computer
- **Use Case:** False positives or acceptable content

### Best Practices

**Before Deleting:**
1. Always view the image first
2. Check the file location (Open Folder)
3. Consider if it's a legitimate file (medical images, art, etc.)
4. When in doubt, ignore rather than delete

**Handling False Positives:**
- The AI isn't perfect and may flag innocent images
- Art, medical images, or cartoon characters can sometimes trigger detection
- Use the "Ignore" button for these cases
- Adjust sensitivity in Settings if you're getting too many false positives

---

## Configuring Settings

Access settings by clicking the **Settings (⚙️)** button on the main screen.

### Detection Sensitivity

**What It Controls:** How strict the AI is when flagging images

**Slider Range:** Low (0.3) to High (0.9)

**Default:** 0.6 (Medium)

**Recommendations:**
- **High (0.7-0.9):** Fewer false positives, but might miss some content
- **Medium (0.5-0.7):** Balanced approach (recommended for most users)
- **Low (0.3-0.5):** Catches more content, but more false positives

**How to Adjust:**
1. Drag the slider to your desired level
2. Click "Save Settings"
3. Your next scan will use the new threshold

### Content Categories to Flag

Choose which types of content should trigger flagging:

**Available Categories:**
- Female Breast Exposed (checked by default)
- Female Genitalia Exposed (checked by default)
- Male Genitalia Exposed (checked by default)
- Anus Exposed (checked by default)
- Buttocks Exposed (checked by default)
- Belly Exposed
- (Additional categories available in the model)

**How to Configure:**
1. Check the boxes for categories you want to monitor
2. Uncheck categories you want to ignore
3. Click "Save Settings"

**Example Use Case:** If you only care about explicit genitalia exposure, uncheck "Buttocks Exposed" and "Belly Exposed" to reduce false positives.

### Content Blurring (🔞)

**What It Does:** Automatically blurs detected content regions in image previews

**Location:** Next to the "Content to Flag" section title (right side)

**Toggle States:**
- **Bright Icon (🔞):** Blur is enabled - detected content will be blurred in previews
- **Faded Icon (🔞):** Blur is disabled - detected content shown without blurring

**Default:** Enabled (blur active)

**How to Use:**
1. Tap the 🔞 icon to toggle blur on/off
2. The icon will brighten (enabled) or fade (disabled) to show current state
3. Hover over the icon to see the tooltip: "Blur Content (Tap to toggle)"
4. Click "Save Settings" to save your preference

**Why Use It:**
- Protects you from viewing explicit content while reviewing results
- Makes it easier to share your screen or review images in public
- Can be disabled if you need to examine details closely

**Technical Details:**
- Uses a 25-pixel Gaussian blur filter
- Only blurs regions above your detection sensitivity threshold
- Only blurs categories you've selected to flag
- Bounding boxes and labels remain visible for context

### Scan Options

**Auto Export Results:**
- Automatically save scan results to a file
- *Currently not implemented - planned for future version*

**Skip Hidden Files:**
- Ignore files with the "hidden" attribute
- **Recommended:** Keep checked to avoid scanning system files
- **Uncheck if:** You want to scan everything, including hidden files

**Confirm File Deletions:**
- Show a confirmation dialog before deleting files
- **Recommended:** Keep checked for safety
- **Uncheck if:** You trust your judgment and want faster deletion workflow

### Resetting to Defaults

If you want to restore original settings:
1. Click "Reset to Defaults" button
2. Settings revert to recommended values
3. Click "Save Settings" to apply (or navigate away to discard)

---

## Advanced Features

### Scanning Specific Drives

While Quick Scan covers common locations, you can scan entire drives:

1. Click "Add Folder"
2. Select the root of a drive (e.g., `C:\`, `D:\`)
3. Be aware: This can take a very long time (hours for large drives)
4. Certain system folders are automatically excluded for safety

### Excluded Directories

For performance and safety, these folders are always skipped:
- Windows system folders (`C:\Windows`, `C:\Program Files`)
- Recycle Bin
- System Volume Information
- Development folders (`node_modules`, `.git`, `.venv`)

### File Type Support

Inntinnsic scans these image formats:
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- BMP (`.bmp`)
- WebP (`.webp`)
- TIFF (`.tiff`, `.tif`)

**File Size Limits:**
- Maximum: 50 MB per image
- Files larger than 50 MB are skipped

### Debug Logging

For troubleshooting, Inntinnsic creates a debug log:
- **Location:** `%LOCALAPPDATA%\Inntinnsic\detection_debug.log`
- **Contents:** Scan details, detection counts, errors
- **Usage:** Helpful for reporting issues or understanding why something was flagged

**To Access:**
1. Press `Windows + R`
2. Type `%LOCALAPPDATA%\Inntinnsic`
3. Open `detection_debug.log` in Notepad

---

## Troubleshooting

### Common Issues and Solutions

#### Model Download Fails

**Problem:** "Failed to download model" error

**Solutions:**
1. Check your internet connection
2. Disable firewall/antivirus temporarily
3. Try again later (server might be busy)
4. Check if you have enough disk space (~50 MB required)

#### Scan Runs Very Slowly

**Problem:** Scanning takes many hours

**Solutions:**
1. Reduce the number of folders being scanned
2. Exclude large folders with many images
3. Close other resource-intensive applications
4. Typical speed: 100-300 images per minute (varies by CPU)

#### Too Many False Positives

**Problem:** Innocent images are being flagged

**Solutions:**
1. Increase detection sensitivity (Settings > 0.7 or higher)
2. Uncheck overly broad categories (like "Belly Exposed")
3. Use "Ignore" button liberally during review
4. Consider the AI isn't perfect with art, medical images, or cartoons

#### Application Won't Start

**Problem:** Double-clicking `Inntinnsic.exe` does nothing

**Solutions:**
1. Right-click > Run as Administrator
2. Check Windows Event Viewer for error details
3. Ensure you have .NET 8.0 runtime (included in self-contained build)
4. Try extracting files to a different location

#### Can't Delete Files

**Problem:** "Access Denied" when trying to delete

**Solutions:**
1. Close any applications that might have the file open
2. Check file permissions (right-click > Properties > Security)
3. Use "Open Folder" to manually delete via File Explorer
4. Run Inntinnsic as Administrator (not typically needed)

#### Results Not Appearing

**Problem:** Scan completes but "View Results" is disabled

**Solutions:**
1. This means no images were flagged (good news!)
2. Try lowering detection sensitivity if you expected results
3. Check that you scanned folders with actual images
4. Verify selected folders contain supported image formats

---

## Frequently Asked Questions

### General Questions

**Q: Is Inntinnsic free?**
A: Yes, Inntinnsic is completely free and open-source.

**Q: Does it work on Mac or Linux?**
A: Currently Windows only. macOS and Linux support may be added in the future.

**Q: Do I need to be online to use it?**
A: Only for the initial model download. After that, it works 100% offline.

**Q: Can it scan videos?**
A: No, currently only image files are supported. Video support may be added later.

### Privacy and Security

**Q: Are my images uploaded anywhere?**
A: Absolutely not. All processing happens locally on your computer.

**Q: Does Inntinnsic collect data about me?**
A: No. There is no telemetry, analytics, or data collection of any kind.

**Q: Can I use this on a work computer?**
A: Check your company's policies first. Inntinnsic is safe and privacy-focused, but some organizations restrict parental control software.

**Q: What happens to scan results?**
A: They're stored in memory only while viewing. When you close the app or start a new scan, previous results are cleared.

### Detection and Accuracy

**Q: How accurate is the AI?**
A: The model is trained on millions of images and is quite accurate, but not perfect. Expect some false positives (10-20% of flagged images may be innocent).

**Q: Can it detect text/conversations?**
A: No, it only analyzes visual content in images, not text.

**Q: Will it flag artistic nudity?**
A: Possibly. The AI detects exposed body parts but can't distinguish artistic intent. You'll need to review flagged results manually.

**Q: Can I train it to recognize specific people?**
A: No, this feature is not available and not planned (for privacy reasons).

### Technical Questions

**Q: Where are settings stored?**
A: In `%LOCALAPPDATA%\Inntinnsic\settings.json`

**Q: Can I run multiple scans at once?**
A: No, only one scan can run at a time.

**Q: How much disk space does it use?**
A: About 150 MB for the application and 40 MB for the AI model (~200 MB total).

**Q: Does it slow down my computer?**
A: While scanning, it uses significant CPU. Close other applications for best performance.

### Troubleshooting

**Q: What if I accidentally delete an important file?**
A: Deletions are permanent and cannot be undone by Inntinnsic. Use file recovery software like Recuva if needed.

**Q: Why is the folder picker not showing?**
A: This is a known Windows issue. Try running as Administrator or restarting the application.

**Q: Can I pause and resume a scan?**
A: No, you can only stop a scan completely. Partial results are preserved.

---

## Getting Help

### Support Resources

**Documentation:**
- User Guide (this document)
- Technical Documentation (for developers)
- Quick Reference Guide

**Community:**
- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and share experiences

**Contact:**
- For urgent issues, open a GitHub issue
- Include debug logs when reporting problems

---

## Tips for Effective Use

### Best Practices

1. **Start with Quick Scan:** Get familiar with the tool using preset locations
2. **Review Before Deleting:** Always view flagged images before taking action
3. **Adjust Sensitivity:** Fine-tune settings based on your first scan results
4. **Regular Scans:** Run weekly scans for ongoing monitoring
5. **Educate, Don't Just Monitor:** Use findings as conversation starters with children

### Recommended Workflow

**Weekly Monitoring Routine:**
1. **Monday:** Run Quick Scan before kids use the computer
2. **Review Results:** Spend 10-15 minutes reviewing flagged content
3. **Take Action:** Delete or ignore as appropriate
4. **Talk to Kids:** Discuss any concerning findings age-appropriately
5. **Adjust Settings:** Refine sensitivity based on results

### Balancing Privacy and Safety

**Respect Privacy:**
- Inform family members that monitoring is taking place
- Focus on safety, not spying
- Review results privately
- Don't overreact to false positives or age-appropriate content

**Maintain Trust:**
- Use Inntinnsic as one tool among many (not the only strategy)
- Combine with education about online safety
- Create an open dialogue about digital content
- Adjust monitoring as children mature

---

## Keyboard Shortcuts

Currently, Inntinnsic does not support keyboard shortcuts. Navigation is mouse/touch-based only.

---

## Accessibility

Inntinnsic aims to be accessible but has some limitations:
- **Screen Readers:** Limited support (MAUI framework constraint)
- **High Contrast:** Forced dark mode only
- **Font Sizing:** Not currently adjustable

Accessibility improvements are planned for future versions.

---

## Updates and Versioning

**Current Version:** 3.0.0

**Checking for Updates:**
- Manual check via GitHub releases page
- No automatic update mechanism currently

**Version History:**
- **3.0.0:** .NET MAUI rewrite, Windows desktop focus
- **2.x:** Python-based prototype (deprecated)
- **1.x:** Initial concept version

---

## Uninstalling Inntinnsic

To remove Inntinnsic from your computer:

1. **Delete Application Folder:** Remove the folder where you extracted Inntinnsic
2. **Delete User Data:** Navigate to `%LOCALAPPDATA%\Inntinnsic` and delete this folder
   - Contains: settings.json, nudenet.onnx, detection_debug.log
3. **No Registry Cleanup Needed:** Inntinnsic doesn't modify the Windows registry

That's it! Inntinnsic is completely removed.

---

## Legal and Ethical Use

### Intended Use

Inntinnsic is designed for:
- Parents monitoring their children's devices
- Personal use on your own computer
- Educational purposes

### Prohibited Use

Do NOT use Inntinnsic to:
- Monitor adults without their explicit consent
- Scan files you don't have permission to access
- Violate privacy laws in your jurisdiction
- Harass or stalk individuals

### Disclaimer

Inntinnsic is a tool to assist with parental control, not a replacement for active parenting, education, and open communication. The developers are not responsible for how you use this software.

---

## Credits and Acknowledgments

**AI Model:** NudeNet by Vladmandic (HuggingFace)
**Framework:** .NET MAUI by Microsoft
**ONNX Runtime:** Microsoft ML Team
**Image Processing:** SkiaSharp

---

## Conclusion

Thank you for using Inntinnsic! We hope this tool helps you create a safer digital environment for your family. Remember, technology is just one part of a comprehensive approach to digital safety - communication and education are equally important.

**Stay Safe, Stay Informed.**

---

**Document Version:** 1.0
**Last Updated:** December 2024
**For:** Inntinnsic v3.0.0
