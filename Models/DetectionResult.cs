using System;
using System.Collections.Generic;

namespace Inntinnsic.Models
{
    /// <summary>
    /// Represents a single detection from the ONNX model
    /// </summary>
    public class Detection
    {
        public string Category { get; set; } = string.Empty;
        public float Confidence { get; set; }
        public float[]? BoundingBox { get; set; } // [x, y, width, height]
    }

    /// <summary>
    /// Result of analyzing an image
    /// </summary>
    public class DetectionResult
    {
        public string FilePath { get; set; } = string.Empty;
        public bool IsFlagged { get; set; }
        public List<Detection> Detections { get; set; } = new();
        public DateTime ScannedAt { get; set; } = DateTime.Now;
        public string? ErrorMessage { get; set; }
    }

    /// <summary>
    /// Progress information for batch scanning
    /// </summary>
    public class ScanProgress
    {
        public int CurrentIndex { get; set; }
        public int TotalFiles { get; set; }
        public string? CurrentFile { get; set; }
        public int FlaggedCount { get; set; }
        public double ProgressPercentage => TotalFiles > 0 ? (double)CurrentIndex / TotalFiles * 100 : 0;
    }
}
