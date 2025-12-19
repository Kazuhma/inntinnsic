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

        public ResultsPage(List<DetectionResult> results)
        {
            InitializeComponent();
            _results = results;
            LoadResults();
        }

        private void LoadResults()
        {
            var flaggedResults = _results.Where(r => r.IsFlagged).ToList();

            SummaryLabel.Text = $"Found {flaggedResults.Count} flagged image(s)";

            ResultsListStack.Children.Clear();

            foreach (var result in flaggedResults)
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

                // Score pill
                var score = result.Detections
                    .Where(d => Config.FlaggedCategories.Contains(d.Category))
                    .Max(d => d.Confidence);

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
            if (flaggedResults.Count > 0)
            {
                SelectResult(flaggedResults[0]);
            }
        }

        private void SelectResult(DetectionResult result)
        {
            _selectedResult = result;
            _selectedResultFilePath = result.FilePath;

            // Update preview
            var filename = System.IO.Path.GetFileName(result.FilePath);
            PreviewFilenameLabel.Text = filename;

            // Load and display image
            try
            {
                if (File.Exists(result.FilePath))
                {
                    PreviewImage.Source = ImageSource.FromFile(result.FilePath);
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

                        await DisplayAlert("Success", "File deleted successfully.", "OK");
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
