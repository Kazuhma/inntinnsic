using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

namespace Inntinnsic.Services
{
    /// <summary>
    /// Service for downloading and managing the NudeNet ONNX model
    /// </summary>
    public class ModelDownloader
    {
        // NudeNet detector model from HuggingFace (vladmandic)
        // YOLOv8-based model with output format [1, 22, 2100] where 22 = 4 bbox + 18 classes
        private const string ModelUrl = "https://huggingface.co/vladmandic/nudenet/resolve/main/nudenet.onnx";

        private readonly HttpClient _httpClient;

        public ModelDownloader()
        {
            _httpClient = new HttpClient
            {
                Timeout = TimeSpan.FromMinutes(10)
            };
        }

        /// <summary>
        /// Check if the model is already downloaded
        /// </summary>
        public bool IsModelDownloaded()
        {
            return File.Exists(Config.ModelPath);
        }

        /// <summary>
        /// Download the NudeNet ONNX model
        /// </summary>
        public async Task<bool> DownloadModelAsync(IProgress<double>? progress = null)
        {
            try
            {
                // Ensure directory exists
                var modelDir = Path.GetDirectoryName(Config.ModelPath);
                if (!Directory.Exists(modelDir))
                {
                    Directory.CreateDirectory(modelDir!);
                }

                progress?.Report(0);

                // Download the model
                using var response = await _httpClient.GetAsync(ModelUrl, HttpCompletionOption.ResponseHeadersRead);
                response.EnsureSuccessStatusCode();

                var totalBytes = response.Content.Headers.ContentLength ?? -1;
                var canReportProgress = totalBytes != -1;

                using var contentStream = await response.Content.ReadAsStreamAsync();
                using var fileStream = new FileStream(Config.ModelPath, FileMode.Create, FileAccess.Write, FileShare.None, 8192, true);

                var buffer = new byte[8192];
                long totalBytesRead = 0;
                int bytesRead;

                while ((bytesRead = await contentStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                {
                    await fileStream.WriteAsync(buffer, 0, bytesRead);
                    totalBytesRead += bytesRead;

                    if (canReportProgress && progress != null)
                    {
                        var progressPercentage = (double)totalBytesRead / totalBytes * 100;
                        progress.Report(progressPercentage);
                    }
                }

                progress?.Report(100);
                return true;
            }
            catch (Exception)
            {
                // Clean up partial download
                if (File.Exists(Config.ModelPath))
                {
                    try { File.Delete(Config.ModelPath); } catch { }
                }
                return false;
            }
        }

        /// <summary>
        /// Get the model file size in MB
        /// </summary>
        public double GetModelSizeMB()
        {
            if (!File.Exists(Config.ModelPath))
                return 0;

            var fileInfo = new FileInfo(Config.ModelPath);
            return fileInfo.Length / (1024.0 * 1024.0);
        }
    }
}
