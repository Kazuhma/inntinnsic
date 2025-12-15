# Inntinnsic Documentation

This directory contains detailed documentation for the Inntinnsic Image Safety Checker project.

## Documentation Files

### [quick-start.md](quick-start.md)
Fast-track guide to get up and running quickly.

**Contents:**
- Setup environment
- First run instructions
- Building standalone executable
- Quick usage guide
- Common scan scenarios
- Troubleshooting tips

**Best for:** Users who want to start using the app immediately.

---

### [project-summary.md](project-summary.md)
Comprehensive technical overview of the project architecture.

**Contents:**
- Project overview and features
- Technical architecture
- Module structure and responsibilities
- Build configuration
- Dependencies explained
- Configuration options
- Security and privacy features
- Deployment options
- Performance characteristics
- Future enhancement ideas
- Testing recommendations

**Best for:** Developers, contributors, and those wanting to understand how the application works internally.

---

### [category-fix.md](category-fix.md)
Important information about the NudeNet category name corrections.

**Contents:**
- Issue identification and resolution
- Correct vs incorrect category names
- NudeNet category reference
- Customization options for filtering
- Testing your configuration
- Impact and action required

**Best for:** Users experiencing detection issues or wanting to customize detection sensitivity.

---

### [build-instructions.md](build-instructions.md)
Comprehensive guide to building standalone executables with PyInstaller.

**Contents:**
- Build prerequisites and setup
- Quick build vs manual build
- Build configuration explained
- PyInstaller hooks for NudeNet
- Troubleshooting build issues
- Testing and distribution
- File size optimization

**Best for:** Developers building standalone executables or troubleshooting build errors.

---

## Quick Links

**Main Documentation:**
- [README.md](../README.md) - Main project documentation

**Source Code:**
- [config.py](../config.py) - Configuration settings
- [main.py](../main.py) - Application entry point
- [gui.py](../gui.py) - User interface
- [scanner.py](../scanner.py) - File scanning logic
- [detector.py](../detector.py) - AI detection logic

**Testing:**
- [test_setup.py](../test_setup.py) - Verify installation
- [test_categories.py](../test_categories.py) - Test category detection

**Build Scripts:**
- [build.bat](../build.bat) - Build standalone executable
- [run.bat](../run.bat) - Run from source
- [build.spec](../build.spec) - PyInstaller configuration

---

## Getting Help

1. **First time user?** → Start with [quick-start.md](quick-start.md)
2. **Want to understand the code?** → Read [project-summary.md](project-summary.md)
3. **Detection not working?** → Check [category-fix.md](category-fix.md)
4. **General questions?** → See main [README.md](../README.md)

---

## Contributing

If you'd like to contribute to the documentation:

1. Keep documentation clear and concise
2. Use examples where helpful
3. Update this index when adding new docs
4. Follow the lowercase-with-dashes.md naming convention
5. Include a table of contents for longer documents

---

**Version:** 1.0.1
**Last Updated:** 2024-12-13
