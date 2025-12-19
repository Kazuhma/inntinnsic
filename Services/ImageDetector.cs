using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using Inntinnsic.Models;
using SkiaSharp;

namespace Inntinnsic.Services
{
    /// <summary>
    /// Image detection service using ONNX Runtime and NudeNet model
    /// </summary>
    public class ImageDetector : IDisposable
    {
        private readonly InferenceSession _session;
        private readonly float _threshold;
        private readonly string _inputName;
        private bool _disposed;

        // NudeNet model input dimensions
        private const int InputWidth = 320;
        private const int InputHeight = 320;
        private const int InputChannels = 3;

        // NudeNet category labels (must match model output order)
        private static readonly string[] CategoryLabels = new[]
        {
            "FEMALE_GENITALIA_COVERED",
            "FACE_FEMALE",
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "FEET_EXPOSED",
            "BELLY_COVERED",
            "FEET_COVERED",
            "ARMPITS_COVERED",
            "ARMPITS_EXPOSED",
            "FACE_MALE",
            "BELLY_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_COVERED",
            "FEMALE_BREAST_COVERED",
            "BUTTOCKS_COVERED"
        };

        private ImageDetector(InferenceSession session, float threshold, string inputName)
        {
            _session = session;
            _threshold = threshold;
            _inputName = inputName;
        }

        /// <summary>
        /// Create and initialize ImageDetector asynchronously (loads model on background thread)
        /// </summary>
        public static async Task<ImageDetector> CreateAsync(float threshold = Config.DetectionThreshold)
        {
            // Ensure model directory exists
            var modelDir = Path.GetDirectoryName(Config.ModelPath);
            if (!Directory.Exists(modelDir))
            {
                Directory.CreateDirectory(modelDir!);
            }

            // Check if model exists
            if (!File.Exists(Config.ModelPath))
            {
                throw new FileNotFoundException(
                    $"ONNX model not found at {Config.ModelPath}. " +
                    "Please download the NudeNet model first.");
            }

            // Load ONNX model on background thread to avoid blocking UI
            var (session, inputName) = await Task.Run(() =>
            {
                var sessionOptions = new SessionOptions
                {
                    GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL
                };

                var sess = new InferenceSession(Config.ModelPath, sessionOptions);

                // Get the actual input name from model metadata
                var inputMeta = sess.InputMetadata.First();
                var actualInputName = inputMeta.Key;

                System.Diagnostics.Debug.WriteLine($"Model input name: {actualInputName}");
                System.Diagnostics.Debug.WriteLine($"Model inputs: {string.Join(", ", sess.InputMetadata.Keys)}");
                System.Diagnostics.Debug.WriteLine($"Model outputs: {string.Join(", ", sess.OutputMetadata.Keys)}");

                return (sess, actualInputName);
            });

            return new ImageDetector(session, threshold, inputName);
        }

        /// <summary>
        /// Analyze a single image for inappropriate content
        /// </summary>
        public async Task<DetectionResult> AnalyzeImageAsync(string imagePath)
        {
            var result = new DetectionResult
            {
                FilePath = imagePath
            };

            try
            {
                // Validate file exists
                if (!File.Exists(imagePath))
                {
                    result.ErrorMessage = "File not found";
                    return result;
                }

                // Load and preprocess image
                using var bitmap = SKBitmap.Decode(imagePath);
                if (bitmap == null)
                {
                    result.ErrorMessage = "Invalid image file";
                    return result;
                }

                // Run inference
                var tensor = PreprocessImage(bitmap);
                var outputs = await Task.Run(() => RunInference(tensor));

                // Post-process results
                result.Detections = PostprocessOutputs(outputs);
                result.IsFlagged = result.Detections.Any(d =>
                    Config.FlaggedCategories.Contains(d.Category) &&
                    d.Confidence >= _threshold);

                // Debug: Log flagged images
                if (result.IsFlagged)
                {
                    var flaggedDetections = result.Detections
                        .Where(d => Config.FlaggedCategories.Contains(d.Category) && d.Confidence >= _threshold)
                        .Select(d => $"{d.Category}({d.Confidence:F3})");
                    var flaggedMsg = $"FLAGGED: {imagePath} - {string.Join(", ", flaggedDetections)}";
                    System.Diagnostics.Debug.WriteLine(flaggedMsg);
                    LogToFile(flaggedMsg);
                }
            }
            catch (Exception ex)
            {
                result.ErrorMessage = ex.Message;
                System.Diagnostics.Debug.WriteLine($"ERROR analyzing {imagePath}: {ex.Message}");
                LogToFile($"ERROR analyzing {imagePath}: {ex.Message}");
            }

            return result;
        }

        /// <summary>
        /// Analyze multiple images with progress updates
        /// </summary>
        public async Task<List<DetectionResult>> BatchAnalyzeAsync(
            List<string> imagePaths,
            IProgress<ScanProgress>? progress = null,
            CancellationToken cancellationToken = default)
        {
            var results = new List<DetectionResult>();
            var total = imagePaths.Count;
            var flaggedCount = 0;

            for (int i = 0; i < imagePaths.Count; i++)
            {
                if (cancellationToken.IsCancellationRequested)
                    break;

                var result = await AnalyzeImageAsync(imagePaths[i]);
                results.Add(result);

                if (result.IsFlagged)
                    flaggedCount++;

                progress?.Report(new ScanProgress
                {
                    CurrentIndex = i + 1,
                    TotalFiles = total,
                    CurrentFile = imagePaths[i],
                    FlaggedCount = flaggedCount
                });
            }

            return results;
        }

        /// <summary>
        /// Preprocess image for model input
        /// </summary>
        private DenseTensor<float> PreprocessImage(SKBitmap original)
        {
            // Resize to model input size
            using var resized = original.Resize(
                new SKImageInfo(InputWidth, InputHeight),
                SKSamplingOptions.Default);

            // Create tensor [1, 3, 320, 320] (NCHW format)
            var tensor = new DenseTensor<float>(
                new[] { 1, InputChannels, InputHeight, InputWidth });

            // Normalize pixels to [0, 1] and convert to NCHW format
            for (int y = 0; y < InputHeight; y++)
            {
                for (int x = 0; x < InputWidth; x++)
                {
                    var pixel = resized.GetPixel(x, y);

                    // Convert RGB to float [0, 1]
                    tensor[0, 0, y, x] = pixel.Red / 255f;   // R channel
                    tensor[0, 1, y, x] = pixel.Green / 255f; // G channel
                    tensor[0, 2, y, x] = pixel.Blue / 255f;  // B channel
                }
            }

            return tensor;
        }

        /// <summary>
        /// Run ONNX inference
        /// </summary>
        private IDisposableReadOnlyCollection<DisposableNamedOnnxValue> RunInference(
            DenseTensor<float> inputTensor)
        {
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor(_inputName, inputTensor)
            };

            return _session.Run(inputs);
        }

        /// <summary>
        /// Post-process model outputs
        /// </summary>
        private List<Detection> PostprocessOutputs(
            IDisposableReadOnlyCollection<DisposableNamedOnnxValue> outputs)
        {
            var detections = new List<Detection>();

            // Debug: Log output tensor names and shapes
            var outputInfo = string.Join(", ", outputs.Select(o =>
            {
                try
                {
                    var tensor = o.AsTensor<float>();
                    var dims = string.Join(",", tensor.Dimensions.ToArray());
                    return $"{o.Name}[{dims}]";
                }
                catch
                {
                    return $"{o.Name}[unknown]";
                }
            }));
            System.Diagnostics.Debug.WriteLine($"Model outputs: {outputInfo}");
            LogToFile($"Model outputs: {outputInfo}");

            // NudeNet detector model outputs:
            // - boxes: [N, 4] - bounding boxes
            // - scores: [N] - confidence scores
            // - labels: [N] - class labels

            // Try the expected format first (separate tensors)
            var boxes = outputs.FirstOrDefault(o => o.Name == "boxes")?.AsEnumerable<float>().ToArray();
            var scores = outputs.FirstOrDefault(o => o.Name == "scores")?.AsEnumerable<float>().ToArray();
            var labels = outputs.FirstOrDefault(o => o.Name == "labels")?.AsEnumerable<long>().ToArray();

            // If not found, try the HuggingFace format (single combined tensor)
            if (boxes == null || scores == null || labels == null)
            {
                LogToFile("Using HuggingFace YOLOv8 model format (single output tensor)");

                // Get the single output tensor
                var output = outputs.FirstOrDefault();
                if (output == null)
                {
                    LogToFile("ERROR: No outputs found at all!");
                    return detections;
                }

                try
                {
                    var tensor = output.AsTensor<float>();
                    var dims = tensor.Dimensions.ToArray();
                    LogToFile($"Processing YOLOv8 tensor shape: [{string.Join(", ", dims)}]");

                    // YOLOv8 format: [1, 22, 2100]
                    // - dim[0] = batch (1)
                    // - dim[1] = 22 values (4 bbox coords + 18 class probabilities)
                    // - dim[2] = 2100 anchor points/predictions

                    if (dims.Length != 3 || dims[0] != 1 || dims[1] != 22)
                    {
                        LogToFile($"ERROR: Unexpected tensor shape. Expected [1, 22, N], got [{string.Join(", ", dims)}]");
                        return detections;
                    }

                    int numPredictions = dims[2]; // 2100
                    LogToFile($"Processing {numPredictions} YOLOv8 predictions");

                    // Parse each prediction
                    for (int i = 0; i < numPredictions; i++)
                    {
                        // Extract bounding box coordinates (indices 0-3)
                        float x = tensor[0, 0, i];
                        float y = tensor[0, 1, i];
                        float w = tensor[0, 2, i];
                        float h = tensor[0, 3, i];

                        // Extract class probabilities (indices 4-21 = 18 classes)
                        float maxClassProb = 0f;
                        int maxClassIndex = -1;

                        for (int classIdx = 0; classIdx < 18; classIdx++)
                        {
                            float classProb = tensor[0, 4 + classIdx, i];
                            if (classProb > maxClassProb)
                            {
                                maxClassProb = classProb;
                                maxClassIndex = classIdx;
                            }
                        }

                        // Apply confidence threshold (lower for initial detection)
                        if (maxClassProb < _threshold * 0.3f)
                            continue;

                        // Get category name
                        string category = maxClassIndex >= 0 && maxClassIndex < CategoryLabels.Length
                            ? CategoryLabels[maxClassIndex]
                            : $"UNKNOWN_{maxClassIndex}";

                        // Create detection with bounding box
                        var bbox = new float[] { x, y, w, h };

                        detections.Add(new Detection
                        {
                            Category = category,
                            Confidence = maxClassProb,
                            BoundingBox = bbox
                        });
                    }

                    LogToFile($"Found {detections.Count} detections above threshold {_threshold * 0.3f:F3}");

                    // Apply Non-Maximum Suppression to remove duplicate detections
                    detections = ApplyNMS(detections, iouThreshold: 0.45f);
                    LogToFile($"After NMS: {detections.Count} detections remaining");

                    // Debug: Log top detections
                    var topDetections = detections
                        .OrderByDescending(d => d.Confidence)
                        .Take(10)
                        .Select(d => $"{d.Category}({d.Confidence:F3})");
                    LogToFile($"Top detections: {string.Join(", ", topDetections)}");

                    return detections;
                }
                catch (Exception ex)
                {
                    LogToFile($"ERROR parsing YOLOv8 format: {ex.Message}");
                    return detections;
                }
            }

            int numDetections = scores.Length;
            System.Diagnostics.Debug.WriteLine($"Processing {numDetections} raw detections from model");
            LogToFile($"Processing {numDetections} raw detections from model");

            for (int i = 0; i < numDetections; i++)
            {
                var score = scores[i];
                var labelIndex = (int)labels[i];

                // Skip low confidence detections
                if (score < _threshold * 0.5f) // Lower threshold for initial detection
                    continue;

                // Get category name
                string category = labelIndex >= 0 && labelIndex < CategoryLabels.Length
                    ? CategoryLabels[labelIndex]
                    : $"UNKNOWN_{labelIndex}";

                // Extract bounding box [x, y, width, height]
                var bbox = new float[4];
                Array.Copy(boxes, i * 4, bbox, 0, 4);

                detections.Add(new Detection
                {
                    Category = category,
                    Confidence = score,
                    BoundingBox = bbox
                });

                // Debug: Log first 5 detections
                if (i < 5)
                {
                    System.Diagnostics.Debug.WriteLine($"  Detection {i}: {category} ({score:F3}) at [{bbox[0]:F1}, {bbox[1]:F1}, {bbox[2]:F1}, {bbox[3]:F1}]");
                }
            }

            System.Diagnostics.Debug.WriteLine($"Returned {detections.Count} detections after filtering");
            return detections;
        }

        /// <summary>
        /// Apply Non-Maximum Suppression to remove duplicate detections
        /// </summary>
        private List<Detection> ApplyNMS(List<Detection> detections, float iouThreshold)
        {
            if (detections.Count == 0)
                return detections;

            // Sort by confidence (highest first)
            var sorted = detections.OrderByDescending(d => d.Confidence).ToList();
            var keep = new List<Detection>();

            while (sorted.Count > 0)
            {
                // Take the detection with highest confidence
                var current = sorted[0];
                keep.Add(current);
                sorted.RemoveAt(0);

                // Remove all detections that overlap significantly with current
                sorted.RemoveAll(d =>
                    current.BoundingBox != null &&
                    d.BoundingBox != null &&
                    CalculateIoU(current.BoundingBox, d.BoundingBox) > iouThreshold);
            }

            return keep;
        }

        /// <summary>
        /// Calculate Intersection over Union (IoU) between two bounding boxes
        /// </summary>
        private float CalculateIoU(float[] box1, float[] box2)
        {
            // boxes are in format [x, y, width, height]
            float x1 = box1[0];
            float y1 = box1[1];
            float w1 = box1[2];
            float h1 = box1[3];

            float x2 = box2[0];
            float y2 = box2[1];
            float w2 = box2[2];
            float h2 = box2[3];

            // Calculate intersection
            float xLeft = Math.Max(x1, x2);
            float yTop = Math.Max(y1, y2);
            float xRight = Math.Min(x1 + w1, x2 + w2);
            float yBottom = Math.Min(y1 + h1, y2 + h2);

            if (xRight < xLeft || yBottom < yTop)
                return 0f; // No intersection

            float intersectionArea = (xRight - xLeft) * (yBottom - yTop);

            // Calculate union
            float box1Area = w1 * h1;
            float box2Area = w2 * h2;
            float unionArea = box1Area + box2Area - intersectionArea;

            if (unionArea == 0)
                return 0f;

            return intersectionArea / unionArea;
        }

        public void Dispose()
        {
            if (!_disposed)
            {
                _session?.Dispose();
                _disposed = true;
            }
        }

        /// <summary>
        /// Helper method to write diagnostic logs to file
        /// </summary>
        private void LogToFile(string message)
        {
            try
            {
                var logPath = Path.Combine(Config.AppDataPath, "detection_debug.log");
                File.AppendAllText(logPath, $"{DateTime.Now:HH:mm:ss.fff} - {message}\n");
            }
            catch
            {
                // Ignore logging errors
            }
        }
    }
}
