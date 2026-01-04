using System.Collections.Generic;
using System.Text.Json;
using System.IO;

namespace Inntinnsic.Models
{
    /// <summary>
    /// User-configurable settings for Inntinnsic
    /// </summary>
    public class UserSettings
    {
        // Detection sensitivity (0.0 - 1.0, higher = more strict)
        public float DetectionSensitivity { get; set; } = Config.DetectionThreshold;

        // Categories to flag
        public HashSet<string> FlaggedCategories { get; set; } = new(Config.FlaggedCategories);

        // Auto export scan results to file
        public bool AutoExportResults { get; set; } = false;

        // Skip hidden files during scan
        public bool SkipHiddenFiles { get; set; } = true;

        // Confirm before deleting files
        public bool ConfirmFileDeletions { get; set; } = true;

        // Blur flagged content in image preview
        public bool BlurFlaggedContent { get; set; } = true;

        /// <summary>
        /// Path to user settings file
        /// </summary>
        private static string SettingsPath => Path.Combine(Config.AppDataPath, "settings.json");

        /// <summary>
        /// Load user settings from file, or create default if not exists
        /// </summary>
        public static UserSettings Load()
        {
            try
            {
                if (File.Exists(SettingsPath))
                {
                    var json = File.ReadAllText(SettingsPath);
                    var settings = JsonSerializer.Deserialize<UserSettings>(json);
                    return settings ?? new UserSettings();
                }
            }
            catch
            {
                // If loading fails, return default settings
            }

            return new UserSettings();
        }

        /// <summary>
        /// Save user settings to file
        /// </summary>
        public void Save()
        {
            try
            {
                // Ensure directory exists
                var dir = Path.GetDirectoryName(SettingsPath);
                if (!Directory.Exists(dir))
                {
                    Directory.CreateDirectory(dir!);
                }

                var json = JsonSerializer.Serialize(this, new JsonSerializerOptions
                {
                    WriteIndented = true
                });
                File.WriteAllText(SettingsPath, json);
            }
            catch
            {
                // Ignore save errors
            }
        }
    }
}
