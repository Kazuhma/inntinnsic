# Inntinnsic

**AI-Powered Image Safety Checker for Parental Control**

[![.NET Version](https://img.shields.io/badge/.NET-8.0-blue)](https://dotnet.microsoft.com/)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-TBD-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/[organization]/inntinnsic/releases)

Inntinnsic is a free, privacy-focused desktop application that helps parents protect their children from inappropriate content by scanning image files using AI-powered detection. All processing happens locally on your computer—no cloud uploads, no subscriptions, no data collection.

---

## Features

- **AI-Powered Detection:** Uses the NudeNet ONNX model to identify potentially inappropriate content with high accuracy
- **100% Local Processing:** All scanning happens on your device—your images never leave your computer
- **Privacy-First:** No telemetry, no cloud sync, no data collection
- **Easy to Use:** Simple interface with Quick Scan and custom folder selection
- **Configurable:** Adjust sensitivity levels and choose which categories to monitor
- **Free and Open Source:** No subscriptions, no hidden costs

---

## Screenshots

![Main Interface](docs/screenshots/main-page.png)
*Main scanning interface with Quick Scan and custom folder selection*

![Results View](docs/screenshots/results-page.png)
*Review flagged images with confidence scores and action buttons*

![Settings](docs/screenshots/settings-page.png)
*Configure detection sensitivity and categories*

---

## Quick Start

### System Requirements

- **OS:** Windows 10 (Version 2004/build 19041) or Windows 11
- **Processor:** 64-bit (x64) processor
- **Memory:** 4 GB RAM (minimum), 8 GB recommended
- **Disk Space:** 250 MB free space
- **Internet:** Required for initial setup only (model download)

### Installation

1. **Download** the latest release from the [Releases page](https://github.com/[organization]/inntinnsic/releases)
2. **Extract** the ZIP file to your desired location (e.g., `C:\Program Files\Inntinnsic`)
3. **Run** `Inntinnsic.exe`
4. **Download Model** when prompted (one-time, ~40 MB download)
5. **Start Scanning!**

No traditional installation required—Inntinnsic is portable and can run from any folder.

### Usage

**Quick Scan (Recommended for First-Time Users):**
```
1. Click "Quick Scan" button
2. Click "Start Scan"
3. Wait for scan to complete
4. Click "View Results" to review flagged images
```

**Custom Folder Scan:**
```
1. Click "Add Folder" to select specific directories
2. Add multiple folders as needed
3. Click "Start Scan"
4. Review results when complete
```

For detailed usage instructions, see the [User Documentation](Docs/user-documentation.md).

---

## How It Works

Inntinnsic uses a three-phase approach to analyze images:

1. **File Discovery:** Recursively scans selected folders for image files (JPEG, PNG, GIF, BMP, WebP, TIFF)
2. **AI Analysis:** Each image is processed through the NudeNet ONNX model to detect potentially inappropriate content
3. **Results Review:** Flagged images are presented with confidence scores for user review and action

**Privacy Note:** All processing happens locally using ONNX Runtime. Images are analyzed in memory and never uploaded anywhere.

---

## Technology Stack

- **Framework:** [.NET MAUI](https://dotnet.microsoft.com/apps/maui) (Multi-platform App UI)
- **Runtime:** .NET 8.0
- **Language:** C# 12
- **AI Engine:** [ONNX Runtime](https://onnxruntime.ai/) 1.23.2
- **AI Model:** [NudeNet](https://github.com/vladmandic/nudenet) (YOLOv8-based, 18 content categories)
- **Image Processing:** [SkiaSharp](https://github.com/mono/SkiaSharp) 3.119.1
- **Platform:** Windows Desktop (x64)

---

## Documentation

Comprehensive documentation is available in the `/Docs` folder:

- **[User Documentation](Docs/user-documentation.md)** - Complete guide for end users
- **[Quick Reference](Docs/quick-reference.md)** - Cheat sheet for common tasks
- **[Technical Documentation](Docs/technical-documentation.md)** - Deep dive for developers
- **[System Architecture](Docs/system-architecture.md)** - Architectural overview and design decisions
- **[New Joiner Guide](Docs/new-joiner-guide.md)** - Onboarding guide for new developers

---

## Building from Source

### Prerequisites

- Windows 10/11 (x64)
- [Visual Studio 2022](https://visualstudio.microsoft.com/) (17.8 or later)
- Workloads:
  - .NET Multi-platform App UI development
  - .NET desktop development

### Build Steps

```bash
# Clone the repository
git clone https://github.com/[organization]/inntinnsic.git
cd inntinnsic

# Restore NuGet packages
dotnet restore

# Build the project
dotnet build -c Release

# Run the application
dotnet run
```

For detailed development setup, see the [New Joiner Guide](Docs/new-joiner-guide.md).

---

## Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs:** Open an issue on GitHub with detailed reproduction steps
2. **Suggest Features:** Share your ideas in GitHub Discussions
3. **Submit Pull Requests:** Fix bugs or implement features
4. **Improve Documentation:** Help make our docs clearer and more comprehensive
5. **Spread the Word:** Tell other parents about Inntinnsic

### Contribution Guidelines

- Follow the [code standards](Docs/new-joiner-guide.md#code-standards) in the New Joiner Guide
- Write clear commit messages using [Conventional Commits](https://www.conventionalcommits.org/)
- Test your changes thoroughly before submitting
- Update documentation as needed

See the [New Joiner Guide](Docs/new-joiner-guide.md) for detailed development workflow.

---

## Roadmap

### Version 3.x (Current)
- ✅ .NET MAUI desktop application
- ✅ ONNX-based AI detection
- ✅ Configurable sensitivity and categories
- ✅ File management (delete, ignore)
- ✅ Comprehensive documentation

### Version 4.0 (Planned)
- ⏳ GPU acceleration (DirectML/CUDA)
- ⏳ Parallel image processing
- ⏳ Export results to CSV/JSON
- ⏳ Scheduled automated scans
- ⏳ Real-time monitoring (file system watcher)

### Future Considerations
- 💡 Support for additional image formats
- 💡 Video frame analysis
- 💡 Plugin system for custom models
- 💡 macOS and Linux support

See [GitHub Issues](https://github.com/[organization]/inntinnsic/issues) for detailed feature requests and bugs.

---

## FAQ

### General

**Q: Is Inntinnsic really free?**
A: Yes, completely free and open source. No subscriptions, no hidden costs.

**Q: Does it work offline?**
A: Yes, after the initial model download, Inntinnsic works 100% offline.

**Q: What operating systems are supported?**
A: Currently Windows 10/11 (x64 only). macOS and Linux support may be added in the future.

### Privacy and Security

**Q: Are my images uploaded anywhere?**
A: No. All processing happens locally on your computer. Your images never leave your device.

**Q: Does Inntinnsic collect any data about me?**
A: No. There is no telemetry, analytics, or data collection of any kind.

**Q: Where is scan data stored?**
A: Scan results are stored in memory only and cleared when you close the app or start a new scan.

### Technical

**Q: How accurate is the AI detection?**
A: The NudeNet model is quite accurate, but not perfect. Expect some false positives (10-20% of flagged images may be innocent). Always review results manually.

**Q: Can I use my own AI model?**
A: Not currently, but plugin support for custom models is planned for a future version.

**Q: Does it support GPU acceleration?**
A: Not yet. Current version uses CPU-only inference. GPU support is planned for version 4.0.

For more questions, see the [User Documentation FAQ](Docs/user-documentation.md#frequently-asked-questions).

---

## Known Limitations

- **Windows Only:** No macOS or Linux support currently
- **CPU-Only Inference:** ~100-300ms per image (GPU support coming in v4.0)
- **No Scan History:** Results not saved between sessions (privacy by design)
- **No Video Analysis:** Images only, no video frame extraction
- **Fixed Model:** Cannot swap ONNX models without code changes

See [Technical Documentation](Docs/technical-documentation.md#known-limitations) for complete list.

---

## License

[License to be determined - suggest MIT or GPLv3]

This project uses the following third-party components:
- **NudeNet Model:** [MIT License](https://github.com/vladmandic/nudenet)
- **ONNX Runtime:** [MIT License](https://github.com/microsoft/onnxruntime)
- **SkiaSharp:** [MIT License](https://github.com/mono/SkiaSharp)
- **.NET MAUI:** [MIT License](https://github.com/dotnet/maui)

---

## Acknowledgments

- **NudeNet Model:** Thanks to [Vladmandic](https://github.com/vladmandic) for the excellent ONNX conversion
- **Microsoft:** For .NET MAUI, ONNX Runtime, and Windows platform
- **Community:** All contributors and users who help improve Inntinnsic

---

## Support

**Need Help?**
- Check the [User Documentation](Docs/user-documentation.md)
- Read the [Quick Reference](Docs/quick-reference.md)
- Search [GitHub Issues](https://github.com/[organization]/inntinnsic/issues)
- Ask in [GitHub Discussions](https://github.com/[organization]/inntinnsic/discussions)

**Found a Bug?**
- Open an [issue](https://github.com/[organization]/inntinnsic/issues/new) with detailed steps to reproduce

**Want a Feature?**
- Share your idea in [Discussions](https://github.com/[organization]/inntinnsic/discussions)

---

## Disclaimer

Inntinnsic is a tool to assist with parental control, not a replacement for active parenting, education, and open communication. The AI model is not 100% accurate and may produce false positives or false negatives. Users are responsible for reviewing results and making informed decisions. The developers are not liable for how this software is used.

**Legal Notice:** This software is intended for use by parents monitoring their own children's devices. Using this software to monitor adults without their explicit consent may violate privacy laws in your jurisdiction. Always use responsibly and legally.

---

## Project Status

**Current Version:** 3.0.0 (Stable)
**Development Status:** Active
**Last Updated:** December 2024

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/[organization]/inntinnsic)
[![Issues](https://img.shields.io/github/issues/[organization]/inntinnsic)](https://github.com/[organization]/inntinnsic/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/[organization]/inntinnsic)](https://github.com/[organization]/inntinnsic/pulls)

---

## Contact

**Project Maintainer:** [Name/Email to be added]
**GitHub:** [https://github.com/[organization]/inntinnsic](https://github.com/[organization]/inntinnsic)
**Issues:** [https://github.com/[organization]/inntinnsic/issues](https://github.com/[organization]/inntinnsic/issues)

---

**Made with ❤️ for families who want to keep their children safe online.**

*Stay Safe. Stay Informed. Stay Connected.*
