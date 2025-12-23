# Inntinnsic

**Privacy-first local AI image content scanning for Windows**

[![.NET Version](https://img.shields.io/badge/.NET-8.0-blue)](https://dotnet.microsoft.com/)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-TBD-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/[organization]/inntinnsic/releases)

Inntinnsic is a free, open-source desktop application that scans image files for sensitive or inappropriate content using AI—entirely offline.

It is designed for creators, researchers, and families who need visibility into large or disorganized image collections without uploading data to the cloud. All processing happens locally on your machine. No accounts, no subscriptions, no telemetry.

---

## Features

- 🖥️ **Fully Local Processing**  
  All image analysis runs on your computer. Nothing is uploaded or shared, no data collection.
- 🧠 **AI-Powered Detection**  
  Uses a trained image classification model to identify exposed anatomy, potentially inappropriate content and other configurable content categories.
- 🎛️ **Configurable Sensitivity & Categories**  
  Adjust detection thresholds and choose exactly which content types should be flagged.
- 🖼️ **Visual Results & Confidence Scores**  
  Review flagged images with previews, bounding boxes, and probability estimates.
- 🔓 **Free & Open Source**  
  No paywalls. No locked features. Community contributions welcome.

---

## 🎯 Common Use Cases

### 🎨 AI Image Creators
Generative AI tools often produce unintended NSFW content, especially across multiple UIs and output folders.

Inntinnsic helps you:
- Locate unintended nudity in large output batches
- Audit images before publishing or sharing
- Manage chaotic folder structures from tools like WebUI, ComfyUI, or custom pipelines

---

### 🧠 Dataset Curators & ML Researchers
Maintaining clean and ethically sourced datasets is essential.

Inntinnsic can be used to:
- Audit image datasets before training or release
- Flag potentially sensitive content automatically
- Reduce manual review workload

---

### 👨‍👩‍👧 Families & Shared Computers
For parents and households who want local content awareness tools without cloud services.

Inntinnsic enables:
- Offline scanning of image folders
- Transparent, reviewable results
- No monitoring, tracking, or remote reporting

---

## Screenshots

![Main Interface](docs/screenshots/main-page.jpg)
*Main scanning interface with Quick Scan and custom folder selection*

![Results View](docs/screenshots/results-page.jpg)
*Review flagged images with confidence scores and action buttons*

![Settings](docs/screenshots/settings-page.jpg)
*Configure detection sensitivity and categories*

---

## ⚙️ How It Works

1. Select one or more folders to scan
2. Inntinnsic analyzes each image using a local AI model
3. Images matching configured criteria are flagged
4. Review results, preview images, and take action manually

The software does **not** delete or modify files automatically unless explicitly instructed.

---

## 🧩 Detection Categories

Depending on your configuration, Inntinnsic can flag:

- Female breast exposure
- Female genitalia exposure
- Male genitalia exposure
- Buttocks exposure
- Anus exposure
- (Additional categories may be added in future versions)

Each detection includes a confidence score to help guide review.

---

## 🧪 Model & Limitations

Inntinnsic uses the **NudeNet** image classification model for content detection.

Important notes:
- Detection is probabilistic and may produce false positives or false negatives
- Results should always be reviewed by a human
- The software provides signals—not judgments or enforcement
- Accuracy may vary based on image style, resolution, and context

This tool is intended for **assistance and awareness**, not automated decision-making.

---

## 🔐 Privacy & Security

- ✅ No internet connection required
- ✅ No cloud uploads
- ✅ No telemetry or analytics
- ✅ No accounts or logins

Your files never leave your computer.

---

## 🛠️ Development & Contributing

Inntinnsic is an open-source project and contributions are welcome.

You can help by:
- Reporting bugs
- Improving documentation
- Suggesting features

---

## 📄 License

This project is released under an open-source license.  
See the `LICENSE` file for details.

Third-party models and dependencies (including NudeNet) are subject to their respective licenses.

---

## ⚠️ Disclaimer

Inntinnsic is provided as-is, without warranty of any kind.  
The developers are not responsible for decisions made based on the software’s output.

Always verify results manually.

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
A: Not. Current version uses CPU-only inference.

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

## Project Status

**Current Version:** 3.0.0 (Stable)
**Development Status:** Active
**Last Updated:** December 2024

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/[organization]/inntinnsic)
[![Issues](https://img.shields.io/github/issues/[organization]/inntinnsic)](https://github.com/[organization]/inntinnsic/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/[organization]/inntinnsic)](https://github.com/[organization]/inntinnsic/pulls)

---

*Stay Safe. Stay Informed. Stay Connected.*