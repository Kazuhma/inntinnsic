using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Inntinnsic.Models;
using Microsoft.Maui.Controls;
using SkiaSharp;
using SkiaSharp.Views.Maui;
using SkiaSharp.Views.Maui.Controls;

namespace Inntinnsic.Views
{
    public class DetectionImageView : SKCanvasView
    {
        private SKBitmap? _bitmap;
        private List<Detection>? _detections;
        private UserSettings? _settings;

        public static readonly BindableProperty ImagePathProperty =
            BindableProperty.Create(
                nameof(ImagePath),
                typeof(string),
                typeof(DetectionImageView),
                null,
                propertyChanged: OnImagePathChanged);

        public static readonly BindableProperty DetectionsProperty =
            BindableProperty.Create(
                nameof(Detections),
                typeof(List<Detection>),
                typeof(DetectionImageView),
                null,
                propertyChanged: OnDetectionsChanged);

        public string? ImagePath
        {
            get => (string?)GetValue(ImagePathProperty);
            set => SetValue(ImagePathProperty, value);
        }

        public List<Detection>? Detections
        {
            get => (List<Detection>?)GetValue(DetectionsProperty);
            set => SetValue(DetectionsProperty, value);
        }

        public DetectionImageView()
        {
            PaintSurface += OnPaintSurface;
            _settings = UserSettings.Load();
        }

        private static void OnImagePathChanged(BindableObject bindable, object oldValue, object newValue)
        {
            if (bindable is DetectionImageView view)
            {
                view.LoadImage(newValue as string);
            }
        }

        private static void OnDetectionsChanged(BindableObject bindable, object oldValue, object newValue)
        {
            if (bindable is DetectionImageView view)
            {
                view._detections = newValue as List<Detection>;
                view.InvalidateSurface();
            }
        }

        private void LoadImage(string? imagePath)
        {
            _bitmap?.Dispose();
            _bitmap = null;

            if (!string.IsNullOrEmpty(imagePath) && File.Exists(imagePath))
            {
                try
                {
                    _bitmap = SKBitmap.Decode(imagePath);
                    InvalidateSurface();
                }
                catch
                {
                    // Failed to load image
                }
            }
        }

        private void OnPaintSurface(object? sender, SKPaintSurfaceEventArgs e)
        {
            var canvas = e.Surface.Canvas;
            canvas.Clear(SKColor.Parse("#0F172A")); // Match background color

            if (_bitmap == null)
                return;

            var info = e.Info;
            var surface = info.Rect;

            // Calculate scaling to fit image while maintaining aspect ratio
            float scale = Math.Min(
                surface.Width / (float)_bitmap.Width,
                surface.Height / (float)_bitmap.Height);

            float scaledWidth = _bitmap.Width * scale;
            float scaledHeight = _bitmap.Height * scale;

            // Center the image
            float left = (surface.Width - scaledWidth) / 2;
            float top = (surface.Height - scaledHeight) / 2;

            var destRect = new SKRect(left, top, left + scaledWidth, top + scaledHeight);

            // Draw the image
            canvas.DrawBitmap(_bitmap, destRect);

            // Draw bounding boxes if detections exist
            if (_detections != null && _detections.Count > 0)
            {
                DrawBoundingBoxes(canvas, destRect, scale);
            }
        }

        private void DrawBoundingBoxes(SKCanvas canvas, SKRect destRect, float scale)
        {
            if (_detections == null || _bitmap == null)
                return;

            // Create paint objects for drawing
            using var boxPaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                StrokeWidth = 3,
                IsAntialias = true
            };

            using var textBackgroundPaint = new SKPaint
            {
                Style = SKPaintStyle.Fill,
                IsAntialias = true
            };

            using var textPaint = new SKPaint
            {
                Color = SKColors.White,
                IsAntialias = true
            };

            using var textFont = new SKFont
            {
                Size = 14,
                Typeface = SKTypeface.FromFamilyName("Arial", SKFontStyle.Bold)
            };

            // Model input size (from ImageDetector.cs)
            const int ModelInputSize = 320;

            // Calculate separate scale factors for X and Y axes
            // (image is stretched to 320x320, not maintaining aspect ratio)
            float modelToOriginalScaleX = _bitmap.Width / (float)ModelInputSize;
            float modelToOriginalScaleY = _bitmap.Height / (float)ModelInputSize;

            foreach (var detection in _detections)
            {
                if (detection.BoundingBox == null || detection.BoundingBox.Length < 4)
                    continue;

                // Skip silently disabled categories
                if (Config.SilentlyDisabledCategories.Contains(detection.Category))
                    continue;

                // Only show bounding boxes for enabled categories
                if (_settings != null && !_settings.FlaggedCategories.Contains(detection.Category))
                    continue;

                // Get bounding box coordinates (in model input pixels - 320x320)
                // YOLO format: (centerX, centerY, width, height)
                float modelCenterX = detection.BoundingBox[0];
                float modelCenterY = detection.BoundingBox[1];
                float modelWidth = detection.BoundingBox[2];
                float modelHeight = detection.BoundingBox[3];

                // Convert from center coordinates to top-left coordinates
                float modelX = modelCenterX - (modelWidth / 2);
                float modelY = modelCenterY - (modelHeight / 2);

                // Convert from model coordinates to original image coordinates
                // Use separate scale factors for X and Y since image was stretched
                float origX = modelX * modelToOriginalScaleX;
                float origY = modelY * modelToOriginalScaleY;
                float origWidth = modelWidth * modelToOriginalScaleX;
                float origHeight = modelHeight * modelToOriginalScaleY;

                // Scale bounding box to match displayed image size
                float scaledX = destRect.Left + (origX * scale);
                float scaledY = destRect.Top + (origY * scale);
                float scaledWidth = origWidth * scale;
                float scaledHeight = origHeight * scale;

                // All shown boxes are for enabled (flagged) categories, so use red
                boxPaint.Color = SKColors.Red;

                // Draw bounding box rectangle
                var rect = new SKRect(scaledX, scaledY, scaledX + scaledWidth, scaledY + scaledHeight);
                canvas.DrawRect(rect, boxPaint);

                // Prepare label text
                string label = $"{detection.Category} {detection.Confidence:P0}";

                // Measure text for background
                float labelWidth = textFont.MeasureText(label) + 12;
                float labelHeight = textFont.Size + 8;

                // Position label above the box, or inside if too close to top
                float labelX = scaledX;
                float labelY = scaledY > labelHeight + 5 ? scaledY - 5 : scaledY + labelHeight;

                // Draw label background
                textBackgroundPaint.Color = boxPaint.Color.WithAlpha(220);
                var labelRect = new SKRect(labelX, labelY - labelHeight, labelX + labelWidth, labelY);
                canvas.DrawRect(labelRect, textBackgroundPaint);

                // Draw label text
                canvas.DrawText(label, labelX + 6, labelY - 4, textFont, textPaint);
            }
        }
    }
}
