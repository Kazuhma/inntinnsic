using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using Inntinnsic.Models;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Controls.Shapes;
using Microsoft.Maui.Graphics;

namespace Inntinnsic.Views
{
    public partial class ResultsPage : ContentPage
    {
        private List<DetectionResult> _results;
        private DetectionResult? _selectedResult;
        private string? _selectedResultFilePath;
        private UserSettings _settings;
        private List<DetectionResult> _flaggedResults = new();
        private int _selectedIndex = -1;

        public ResultsPage(List<DetectionResult> results)
        {
            InitializeComponent();
            _results = results;
            _settings = UserSettings.Load();
            LoadResults();
            SetupKeyboardHandling();
        }

        private void SetupKeyboardHandling()
        {
#if WINDOWS
            this.Loaded += OnLoaded;
#endif
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();
#if WINDOWS
            AttachKeyboardHandler();
#endif
        }

        protected override void OnDisappearing()
        {
            base.OnDisappearing();
#if WINDOWS
            DetachKeyboardHandler();
#endif
        }

#if WINDOWS
        private void OnLoaded(object? sender, EventArgs e)
        {
            AttachKeyboardHandler();
        }

        private void AttachKeyboardHandler()
        {
            try
            {
                var window = Application.Current?.Windows[0]?.Handler?.PlatformView as Microsoft.UI.Xaml.Window;
                if (window != null)
                {
                    window.Content.KeyDown -= OnWindowKeyDown;
                    window.Content.KeyDown += OnWindowKeyDown;
                }
            }
            catch { /* Ignore errors */ }
        }

        private void DetachKeyboardHandler()
        {
            try
            {
                var window = Application.Current?.Windows[0]?.Handler?.PlatformView as Microsoft.UI.Xaml.Window;
                if (window != null)
                {
                    window.Content.KeyDown -= OnWindowKeyDown;
                }
            }
            catch { /* Ignore errors */ }
        }

        private void OnWindowKeyDown(object sender, Microsoft.UI.Xaml.Input.KeyRoutedEventArgs e)
        {
            HandleKeyPress(e);
        }

        private void HandleKeyPress(Microsoft.UI.Xaml.Input.KeyRoutedEventArgs e)
        {
            switch (e.Key)
            {
                case Windows.System.VirtualKey.Up:
                case Windows.System.VirtualKey.Left:
                    NavigatePrevious();
                    e.Handled = true;
                    break;
                case Windows.System.VirtualKey.Down:
                case Windows.System.VirtualKey.Right:
                    NavigateNext();
                    e.Handled = true;
                    break;
                case Windows.System.VirtualKey.Escape:
                    Navigation.PopAsync();
                    e.Handled = true;
                    break;
            }
        }
#endif

        private void NavigatePrevious()
        {
            if (_flaggedResults.Count == 0) return;

            if (_selectedIndex > 0)
            {
                _selectedIndex--;
                SelectResult(_flaggedResults[_selectedIndex]);
            }
        }

        private void NavigateNext()
        {
            if (_flaggedResults.Count == 0) return;

            if (_selectedIndex < _flaggedResults.Count - 1)
            {
                _selectedIndex++;
                SelectResult(_flaggedResults[_selectedIndex]);
            }
        }

        private void LoadResults()
        {
            // Filter ALL results based on current settings (ignore scan-time IsFlagged)
            // This allows changing sensitivity after scan to show more or fewer results
            _flaggedResults = _results
                .Where(r => r.Detections.Any(d =>
                                !Config.SilentlyDisabledCategories.Contains(d.Category) &&
                                _settings.FlaggedCategories.Contains(d.Category) &&
                                d.Confidence >= _settings.DetectionSensitivity))
                .ToList();

            SummaryLabel.Text = $"Found {_flaggedResults.Count} flagged image(s)";

            ResultsListStack.Children.Clear();

            foreach (var result in _flaggedResults)
            {
                var border = new Border
                {
                    BackgroundColor = Color.FromArgb("#1F2937"),
                    Padding = new Thickness(15),
                    StrokeThickness = 0,
                    Margin = new Thickness(0, 0, 0, 0)
                };
                border.StrokeShape = new RoundRectangle { CornerRadius = 8 };

                var grid = new Grid
                {
                    ColumnDefinitions =
                    {
                        new ColumnDefinition { Width = GridLength.Star },
                        new ColumnDefinition { Width = GridLength.Auto }
                    }
                };

                // Filename
                var filename = System.IO.Path.GetFileName(result.FilePath);
                var filenameLabel = new Label
                {
                    Text = filename,
                    FontSize = 13,
                    FontAttributes = FontAttributes.Bold,
                    TextColor = Colors.White,
                    VerticalOptions = LayoutOptions.Center,
                    LineBreakMode = LineBreakMode.MiddleTruncation
                };
                grid.Add(filenameLabel, 0, 0);

                // Score pill - show highest confidence among enabled categories above threshold
                var qualifyingDetections = result.Detections
                    .Where(d => !Config.SilentlyDisabledCategories.Contains(d.Category) &&
                                _settings.FlaggedCategories.Contains(d.Category) &&
                                d.Confidence >= _settings.DetectionSensitivity)
                    .ToList();

                if (qualifyingDetections.Count == 0)
                    continue; // Skip if no qualifying detections (shouldn't happen due to outer filter)

                var score = qualifyingDetections.Max(d => d.Confidence);

                var scoreBorder = new Border
                {
                    BackgroundColor = Color.FromArgb("#EF4444"),
                    Padding = new Thickness(8, 4),
                    StrokeThickness = 0,
                    VerticalOptions = LayoutOptions.Center,
                    HorizontalOptions = LayoutOptions.End
                };
                scoreBorder.StrokeShape = new RoundRectangle { CornerRadius = 12 };

                var scoreLabel = new Label
                {
                    Text = $"{score:P0}",
                    FontSize = 11,
                    FontAttributes = FontAttributes.Bold,
                    TextColor = Colors.White
                };
                scoreBorder.Content = scoreLabel;
                grid.Add(scoreBorder, 1, 0);

                border.Content = grid;

                // Make the entire item clickable
                var tapGesture = new TapGestureRecognizer();
                tapGesture.Tapped += (s, e) => SelectResult(result);
                border.GestureRecognizers.Add(tapGesture);

                ResultsListStack.Children.Add(border);
            }

            // Auto-select first result
            if (_flaggedResults.Count > 0)
            {
                _selectedIndex = 0;
                SelectResult(_flaggedResults[0]);
            }
        }

        private void SelectResult(DetectionResult result)
        {
            _selectedResult = result;
            _selectedResultFilePath = result.FilePath;

            // Update selected index for keyboard navigation
            _selectedIndex = _flaggedResults.IndexOf(result);

            // Update preview
            var filename = System.IO.Path.GetFileName(result.FilePath);
            PreviewFilenameLabel.Text = filename;

            // Load and display image with bounding boxes
            try
            {
                if (File.Exists(result.FilePath))
                {
                    PreviewImage.ImagePath = result.FilePath;
                    PreviewImage.Detections = result.Detections;
                    PreviewImage.IsVisible = true;
                    PreviewPlaceholderLabel.IsVisible = false;

                    // Show action buttons
                    PreviewOpenFolderButton.IsVisible = true;
                    PreviewDeleteButton.IsVisible = true;
                    PreviewIgnoreButton.IsVisible = true;
                }
                else
                {
                    PreviewImage.IsVisible = false;
                    PreviewPlaceholderLabel.Text = "Image file not found";
                    PreviewPlaceholderLabel.IsVisible = true;
                }
            }
            catch (Exception ex)
            {
                PreviewImage.IsVisible = false;
                PreviewPlaceholderLabel.Text = $"Error loading image: {ex.Message}";
                PreviewPlaceholderLabel.IsVisible = true;
            }

            // Highlight selected item in list
            UpdateListSelection();

            // Auto-scroll to keep selected item in view (fire and forget)
            _ = ScrollToSelectedItem();
        }

        private void UpdateListSelection()
        {
            // Update background colors to show selection
            foreach (var child in ResultsListStack.Children)
            {
                if (child is Border border)
                {
                    var isSelected = false;
                    if (border.Content is Grid grid && grid.Children.Count > 0)
                    {
                        if (grid.Children[0] is Label label)
                        {
                            var filename = System.IO.Path.GetFileName(_selectedResultFilePath ?? "");
                            isSelected = label.Text == filename;
                        }
                    }

                    border.BackgroundColor = isSelected
                        ? Color.FromArgb("#2563EB")
                        : Color.FromArgb("#1F2937");
                }
            }
        }

        private async System.Threading.Tasks.Task ScrollToSelectedItem()
        {
            try
            {
                if (_selectedIndex < 0 || _selectedIndex >= ResultsListStack.Children.Count)
                    return;

                var selectedBorder = ResultsListStack.Children[_selectedIndex] as Border;
                if (selectedBorder != null)
                {
                    // Scroll to the selected item with animation
                    await ResultsScrollView.ScrollToAsync(selectedBorder, ScrollToPosition.MakeVisible, true);
                }
            }
            catch
            {
                // Ignore scroll errors
            }
        }

        private void OnPreviewOpenFolderClicked(object? sender, EventArgs e)
        {
            if (_selectedResultFilePath == null) return;

            try
            {
                var directory = System.IO.Path.GetDirectoryName(_selectedResultFilePath);
                if (directory != null && Directory.Exists(directory))
                {
#if WINDOWS
                    Process.Start("explorer.exe", $"/select,\"{_selectedResultFilePath}\"");
#endif
                }
            }
            catch (Exception ex)
            {
                DisplayAlert("Error", $"Failed to open folder: {ex.Message}", "OK");
            }
        }

        private async void OnPreviewDeleteClicked(object? sender, EventArgs e)
        {
            if (_selectedResultFilePath == null || _selectedResult == null) return;

            var filename = System.IO.Path.GetFileName(_selectedResultFilePath);
            var confirm = await DisplayAlert(
                "Confirm Delete",
                $"Are you sure you want to permanently delete this file?\n\n{filename}",
                "Delete",
                "Cancel");

            if (confirm)
            {
                try
                {
                    if (File.Exists(_selectedResultFilePath))
                    {
                        File.Delete(_selectedResultFilePath);

                        // Remove from results and refresh
                        _results.RemoveAll(r => r.FilePath == _selectedResultFilePath);
                        LoadResults();
                    }
                }
                catch (Exception ex)
                {
                    await DisplayAlert("Error", $"Failed to delete file: {ex.Message}", "OK");
                }
            }
        }

        private void OnPreviewIgnoreClicked(object? sender, EventArgs e)
        {
            if (_selectedResultFilePath == null) return;

            // Remove from results and refresh
            _results.RemoveAll(r => r.FilePath == _selectedResultFilePath);
            LoadResults();
        }
    }
}
