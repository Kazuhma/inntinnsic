using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Inntinnsic.Services
{
    /// <summary>
    /// File system scanning service for finding image files
    /// </summary>
    public class FileScanner
    {
        private CancellationTokenSource? _cancellationTokenSource;
        private int _scannedCount;
        private int _foundCount;

        public bool SkipHidden { get; set; } = true;

        /// <summary>
        /// Stop the current scan
        /// </summary>
        public void Stop()
        {
            _cancellationTokenSource?.Cancel();
        }

        /// <summary>
        /// Check if a directory should be skipped
        /// </summary>
        private bool ShouldSkipDirectory(DirectoryInfo directory)
        {
            var dirName = directory.Name;

            // Skip hidden directories
            if (dirName.StartsWith("."))
                return true;

            // Skip directories in the skip list
            if (Config.SkipDirectories.Contains(dirName))
                return true;

            // Check if path contains any skip directory
            var pathParts = directory.FullName.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            return pathParts.Any(part => Config.SkipDirectories.Contains(part));
        }

        /// <summary>
        /// Check if file is a valid image to process
        /// </summary>
        private bool IsValidImage(FileInfo file)
        {
            try
            {
                // Skip hidden files if enabled
                if (SkipHidden && file.Name.StartsWith("."))
                    return false;

                // Check extension
                if (!Config.ImageExtensions.Contains(file.Extension))
                    return false;

                // Check file size
                if (file.Length == 0 || file.Length > Config.MaxFileSize)
                    return false;

                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        /// <summary>
        /// Recursively find all image files in given paths
        /// </summary>
        public async Task<List<string>> FindImagesAsync(
            List<string> paths,
            bool includeSystem = false,
            IProgress<string>? progress = null,
            CancellationToken cancellationToken = default)
        {
            var imageFiles = new List<string>();
            _cancellationTokenSource = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            _scannedCount = 0;
            _foundCount = 0;

            foreach (var pathStr in paths)
            {
                if (_cancellationTokenSource.Token.IsCancellationRequested)
                    break;

                try
                {
                    var path = new DirectoryInfo(pathStr);

                    // Validate path exists
                    if (!path.Exists)
                    {
                        if (File.Exists(pathStr))
                        {
                            // It's a file
                            var file = new FileInfo(pathStr);
                            if (IsValidImage(file))
                            {
                                imageFiles.Add(file.FullName);
                                _foundCount++;
                                progress?.Report($"Found: {_foundCount} images");
                            }
                        }
                        else
                        {
                            progress?.Report($"⚠️ Path not found: {pathStr}");
                        }
                        continue;
                    }

                    // Scan directory
                    await ScanDirectoryAsync(
                        path,
                        imageFiles,
                        includeSystem,
                        progress,
                        _cancellationTokenSource.Token);
                }
                catch (UnauthorizedAccessException)
                {
                    progress?.Report($"⚠️ Access denied: {pathStr}");
                }
                catch (Exception ex)
                {
                    progress?.Report($"⚠️ Error scanning {pathStr}: {ex.Message}");
                }
            }

            return imageFiles;
        }

        /// <summary>
        /// Recursively scan a directory for images
        /// </summary>
        private async Task ScanDirectoryAsync(
            DirectoryInfo directory,
            List<string> imageFiles,
            bool includeSystem,
            IProgress<string>? progress,
            CancellationToken cancellationToken)
        {
            if (cancellationToken.IsCancellationRequested)
                return;

            try
            {
                // Process files in current directory
                var files = directory.EnumerateFiles();
                foreach (var file in files)
                {
                    if (cancellationToken.IsCancellationRequested)
                        return;

                    _scannedCount++;

                    // Update progress every 100 files
                    if (_scannedCount % 100 == 0)
                    {
                        progress?.Report(
                            $"Scanning... Found: {_foundCount} images (checked {_scannedCount} files)");
                    }

                    try
                    {
                        if (IsValidImage(file))
                        {
                            imageFiles.Add(file.FullName);
                            _foundCount++;
                        }
                    }
                    catch
                    {
                        // Skip inaccessible files
                    }
                }

                // Process subdirectories
                var subdirectories = directory.EnumerateDirectories();
                foreach (var subdir in subdirectories)
                {
                    if (cancellationToken.IsCancellationRequested)
                        return;

                    try
                    {
                        // Filter directories to skip
                        if (!includeSystem && ShouldSkipDirectory(subdir))
                            continue;

                        // Even with system scan, skip hidden directories
                        if (includeSystem && subdir.Name.StartsWith("."))
                            continue;

                        await ScanDirectoryAsync(
                            subdir,
                            imageFiles,
                            includeSystem,
                            progress,
                            cancellationToken);
                    }
                    catch (UnauthorizedAccessException)
                    {
                        // Skip inaccessible directories
                    }
                    catch
                    {
                        // Skip problematic directories
                    }
                }
            }
            catch (UnauthorizedAccessException)
            {
                progress?.Report($"⚠️ Access denied: {directory.FullName}");
            }
        }

        /// <summary>
        /// Get list of available drives on Windows
        /// </summary>
        public List<string> GetAvailableDrives()
        {
            return DriveInfo.GetDrives()
                .Where(d => d.IsReady && d.DriveType == DriveType.Fixed)
                .Select(d => d.Name)
                .ToList();
        }
    }
}
