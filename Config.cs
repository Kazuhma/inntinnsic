using System.Collections.Generic;
using System.IO;

namespace Inntinnsic
{
    /// <summary>
    /// Configuration settings for Inntinnsic Image Safety Checker
    /// </summary>
    public static class Config
    {
        // Application metadata
        public const string AppName = "Inntinnsic";
        public const string AppVersion = "3.0.0";
        public const string AppDescription = "Image Safety Checker for Parental Control";

        // Supported image formats
        public static readonly HashSet<string> ImageExtensions = new(StringComparer.OrdinalIgnoreCase)
        {
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"
        };

        // Detection threshold (0.0 - 1.0, higher = more strict)
        // 0.6 is a balanced default - increase for fewer false positives
        public const float DetectionThreshold = 0.6f;

        // Categories that are silently disabled (not used for flagging or display)
        public static readonly HashSet<string> SilentlyDisabledCategories = new(StringComparer.OrdinalIgnoreCase)
        {
            "ARMPITS_EXPOSED",
            "BELLY_EXPOSED",
            "FACE_FEMALE",
            "FACE_MALE"
        };

        // Categories to flag (NudeNet provides these classifications)
        public static readonly HashSet<string> FlaggedCategories = new(StringComparer.OrdinalIgnoreCase)
        {
            "ANUS_EXPOSED",
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED"
        };

        // Optional: Stricter filtering categories (currently not used)
        public static readonly HashSet<string> StrictFilteringCategories = new(StringComparer.OrdinalIgnoreCase)
        {
            "ANUS_EXPOSED",
            "ANUS_COVERED",
            "BUTTOCKS_EXPOSED",
            "BUTTOCKS_COVERED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_BREAST_COVERED",
            "FEMALE_GENITALIA_EXPOSED",
            "FEMALE_GENITALIA_COVERED",
            "MALE_GENITALIA_EXPOSED",
            "MALE_BREAST_EXPOSED"
        };

        // Directories to skip (for performance and to avoid system issues)
        public static readonly HashSet<string> SkipDirectories = new(StringComparer.OrdinalIgnoreCase)
        {
            "$RECYCLE.BIN",
            "System Volume Information",
            "Windows",
            "Program Files",
            "Program Files (x86)",
            "ProgramData",
            "node_modules",
            ".git",
            ".venv",
            "venv"
        };

        // Maximum file size to process (in bytes) - skip very large files
        public const long MaxFileSize = 50 * 1024 * 1024; // 50 MB

        /// <summary>
        /// Returns commonly used directories that may contain images
        /// </summary>
        public static Dictionary<string, List<string>> GetCommonLocations()
        {
            var userHome = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            var localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            var tempPath = Path.GetTempPath();

            return new Dictionary<string, List<string>>
            {
                ["User Folders"] = new List<string>
                {
                    Path.Combine(userHome, "Downloads"),
                    Environment.GetFolderPath(Environment.SpecialFolder.MyPictures),
                    Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                    Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
                    Environment.GetFolderPath(Environment.SpecialFolder.MyVideos)
                },
                ["Browser Caches"] = new List<string>
                {
                    Path.Combine(localAppData, "Google", "Chrome", "User Data", "Default", "Cache"),
                    Path.Combine(localAppData, "Google", "Chrome", "User Data", "Default", "Cache", "Cache_Data"),
                    Path.Combine(localAppData, "Microsoft", "Edge", "User Data", "Default", "Cache"),
                    Path.Combine(localAppData, "Microsoft", "Edge", "User Data", "Default", "Cache", "Cache_Data"),
                    Path.Combine(userHome, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles"),
                    Path.Combine(localAppData, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"),
                    Path.Combine(localAppData, "Opera Software", "Opera Stable", "Cache")
                },
                ["System Temp"] = new List<string>
                {
                    tempPath,
                    @"C:\Windows\Temp"
                },
                ["Common App Locations"] = new List<string>
                {
                    Path.Combine(localAppData, "Packages"),
                    Path.Combine(localAppData, "Microsoft", "Windows", "INetCache")
                }
            };
        }

        /// <summary>
        /// Path to the ONNX model file
        /// </summary>
        public static string ModelPath => Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            AppName,
            "nudenet.onnx"
        );

        /// <summary>
        /// Directory for application data
        /// </summary>
        public static string AppDataPath => Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            AppName
        );

        /// <summary>
        /// Path to the log file
        /// </summary>
        public static string LogFilePath => Path.Combine(AppDataPath, "scan_log.txt");
    }
}
