using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Inntinnsic.Models;
using Inntinnsic.Services;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Controls.Shapes;

namespace Inntinnsic.Views
{
    public partial class MainPage : ContentPage
    {
        private readonly ModelDownloader _modelDownloader;
        private readonly FileScanner _fileScanner;
        private ImageDetector? _imageDetector;
        private readonly List<string> _selectedFolders;
        private CancellationTokenSource? _cancellationTokenSource;
        private bool _isScanning;
        private DateTime _lastUiUpdate = DateTime.MinValue;
        private List<DetectionResult> _lastScanResults = new();

        public MainPage()
        {
            InitializeComponent();

            _modelDownloader = new ModelDownloader();
            _fileScanner = new FileScanner();
            _selectedFolders = new List<string>();

            // Initialize folder list with placeholder visible
            UpdateFolderList();
        }

        private async Task<bool> EnsureModelLoadedAsync()
        {
            // If detector already loaded, we're good
            if (_imageDetector != null)
                return true;

            // Check if model file exists
            if (!_modelDownloader.IsModelDownloaded())
            {
                var download = await DisplayAlert(
                    "Model Required",
                    "The NudeNet detection model needs to be downloaded (~40MB). Download now?",
                    "Download",
                    "Cancel");

                if (!download)
                    return false;

                await DownloadModelAsync();

                // Check if download succeeded
                if (_imageDetector == null)
                    return false;
            }
            else
            {
                // Model exists, try to load it
                try
                {
                    StatusMessageLabel.Text = "Loading model...";
                    _imageDetector = await ImageDetector.CreateAsync();
                    var modelSize = _modelDownloader.GetModelSizeMB();
                    StatusMessageLabel.Text = $"Model loaded ({modelSize:F1} MB). Ready to scan!";
                }
                catch (Exception ex)
                {
                    await DisplayAlert("Error", $"Failed to load model: {ex.Message}", "OK");
                    return false;
                }
            }

            return true;
        }

        private async Task DownloadModelAsync()
        {
            StatusTitleLabel.Text = "Downloading Model...";
            StatusMessageLabel.Text = "Please wait while the model is downloaded";
            ScanProgressBar.IsVisible = true;
            StartScanButton.IsEnabled = false;
            QuickScanButton.IsEnabled = false;
            AddFolderButton.IsEnabled = false;

            var progress = new Progress<double>(percent =>
            {
                MainThread.BeginInvokeOnMainThread(() =>
                {
                    ScanProgressBar.Progress = percent / 100.0;
                    StatusMessageLabel.Text = $"Downloading... {percent:F0}%";
                });
            });

            var success = await _modelDownloader.DownloadModelAsync(progress);

            ScanProgressBar.IsVisible = false;
            StartScanButton.IsEnabled = true;
            QuickScanButton.IsEnabled = true;
            AddFolderButton.IsEnabled = true;

            if (success)
            {
                try
                {
                    StatusMessageLabel.Text = "Loading model...";
                    _imageDetector = await ImageDetector.CreateAsync();
                    var modelSize = _modelDownloader.GetModelSizeMB();
                    StatusTitleLabel.Text = "Model Ready";
                    StatusMessageLabel.Text = $"Model downloaded successfully ({modelSize:F1} MB)";
                    await DisplayAlert("Success", "Model downloaded and loaded successfully!", "OK");
                }
                catch (Exception ex)
                {
                    await DisplayAlert("Error", $"Model downloaded but failed to load: {ex.Message}", "OK");
                }
            }
            else
            {
                StatusTitleLabel.Text = "Download Failed";
                StatusMessageLabel.Text = "Failed to download model. Please try again.";
                await DisplayAlert("Error", "Failed to download the model. Please check your internet connection and try again.", "OK");
            }
        }

        private async void OnAddFolderClicked(object sender, EventArgs e)
        {
            try
            {
                var folderPath = await PickFolderAsync();

                if (!string.IsNullOrWhiteSpace(folderPath))
                {
                    if (!_selectedFolders.Contains(folderPath))
                    {
                        _selectedFolders.Add(folderPath);
                        UpdateFolderList();
                        StatusMessageLabel.Text = $"Added: {folderPath} ({_selectedFolders.Count} folder(s) selected)";
                    }
                    else
                    {
                        await DisplayAlert("Already Added", "This folder has already been added to the scan list.", "OK");
                    }
                }
            }
            catch (Exception ex)
            {
                await DisplayAlert("Error", $"Failed to add folder: {ex.Message}", "OK");
            }
        }

        private async Task<string?> PickFolderAsync()
        {
#if WINDOWS
            var folderPicker = new Windows.Storage.Pickers.FolderPicker();

            // Get the window handle for the current window
            var window = Application.Current?.Windows[0].Handler?.PlatformView as Microsoft.UI.Xaml.Window;
            var hwnd = WinRT.Interop.WindowNative.GetWindowHandle(window);

            // Initialize the folder picker with the window handle
            WinRT.Interop.InitializeWithWindow.Initialize(folderPicker, hwnd);

            folderPicker.SuggestedStartLocation = Windows.Storage.Pickers.PickerLocationId.Desktop;
            folderPicker.FileTypeFilter.Add("*");

            var folder = await folderPicker.PickSingleFolderAsync();
            return folder?.Path;
#else
            await DisplayAlert("Not Supported", "Folder picker is only supported on Windows.", "OK");
            return null;
#endif
        }

        private async void OnQuickScanClicked(object sender, EventArgs e)
        {
            // Ensure model is loaded
            if (!await EnsureModelLoadedAsync())
                return;

            // Quick scan common locations
            _selectedFolders.Clear();
            var commonLocations = Config.GetCommonLocations();

            // Flatten the dictionary into a list of all paths
            foreach (var category in commonLocations.Values)
            {
                foreach (var location in category)
                {
                    if (System.IO.Directory.Exists(location) && !_selectedFolders.Contains(location))
                    {
                        _selectedFolders.Add(location);
                    }
                }
            }

            if (_selectedFolders.Count == 0)
            {
                await DisplayAlert("No Folders", "No common image folders found on this system.", "OK");
                return;
            }

            UpdateFolderList();
            StatusMessageLabel.Text = $"Quick scan: {_selectedFolders.Count} common location(s) selected";
            await StartScanAsync();
        }

        private async void OnStartScanClicked(object sender, EventArgs e)
        {
            if (_isScanning)
            {
                // Stop scan
                _cancellationTokenSource?.Cancel();
                return;
            }

            if (_selectedFolders.Count == 0)
            {
                await DisplayAlert("No Folders", "Please add folders to scan first.", "OK");
                return;
            }

            // Ensure model is loaded
            if (!await EnsureModelLoadedAsync())
                return;

            await StartScanAsync();
        }

        private async Task StartScanAsync()
        {
            if (_imageDetector == null) return;

            _isScanning = true;
            _cancellationTokenSource = new CancellationTokenSource();

            // Clear previous results and disable View Results button
            _lastScanResults.Clear();
            ViewResultsButton.IsEnabled = false;
            ViewResultsButton.BackgroundColor = Color.FromArgb("#1E293B"); // CardDark
            ViewResultsButton.TextColor = Color.FromArgb("#6B7280"); // TextMuted

            // Update UI for scanning state
            StartScanButton.Text = "⏹ Stop Scan";
            StartScanButton.BackgroundColor = Color.FromArgb("#EF4444"); // Red
            AddFolderButton.IsEnabled = false;
            QuickScanButton.IsEnabled = false;
            ScanProgressBar.IsVisible = true;
            ScanProgressBar.Progress = 0;
            ScannedCountLabel.Text = "0";
            FlaggedCountLabel.Text = "0";
            StatusLabel.Text = "Scanning";
            StatusTitleLabel.Text = "Scanning...";

            try
            {
                // Phase 1: Find images
                StatusMessageLabel.Text = "Searching for images...";

                var scanProgress = new Progress<string>(message =>
                {
                    MainThread.BeginInvokeOnMainThread(() =>
                    {
                        StatusMessageLabel.Text = message;
                    });
                });

                var imageFiles = await _fileScanner.FindImagesAsync(
                    _selectedFolders,
                    includeSystem: false,
                    scanProgress,
                    _cancellationTokenSource.Token);

                if (_cancellationTokenSource.Token.IsCancellationRequested)
                {
                    StatusTitleLabel.Text = "Scan Cancelled";
                    StatusMessageLabel.Text = "Scan was stopped by user";
                    return;
                }

                if (imageFiles.Count == 0)
                {
                    StatusTitleLabel.Text = "No Images Found";
                    StatusMessageLabel.Text = "No images found in selected folders";
                    await DisplayAlert("No Images", "No images were found in the selected folders.", "OK");
                    return;
                }

                // Phase 2: Analyze images
                StatusTitleLabel.Text = $"Analyzing {imageFiles.Count} Images...";

                var analysisProgress = new Progress<ScanProgress>(progress =>
                {
                    // Throttle UI updates to every 200ms to prevent overwhelming the UI thread
                    var now = DateTime.Now;
                    var isLastImage = progress.CurrentIndex >= progress.TotalFiles;
                    var shouldUpdate = isLastImage || (now - _lastUiUpdate).TotalMilliseconds >= 200;

                    if (shouldUpdate)
                    {
                        _lastUiUpdate = now;
                        MainThread.BeginInvokeOnMainThread(() =>
                        {
                            ScannedCountLabel.Text = progress.CurrentIndex.ToString();
                            FlaggedCountLabel.Text = progress.FlaggedCount.ToString();

                            var fileName = System.IO.Path.GetFileName(progress.CurrentFile);
                            StatusMessageLabel.Text = $"Analyzing: {fileName} ({progress.CurrentIndex}/{progress.TotalFiles})";

                            ScanProgressBar.Progress = (double)progress.CurrentIndex / progress.TotalFiles;
                        });
                    }
                });

                var results = await _imageDetector.BatchAnalyzeAsync(
                    imageFiles,
                    analysisProgress,
                    _cancellationTokenSource.Token);

                // Count flagged results
                var flaggedCount = results.Count(r => r.IsFlagged);

                // Store results and enable View Results button if flagged items exist
                _lastScanResults = results;

                if (flaggedCount > 0)
                {
                    ViewResultsButton.IsEnabled = true;
                    ViewResultsButton.BackgroundColor = Color.FromArgb("#3B82F6"); // Primary
                    ViewResultsButton.TextColor = Colors.White;
                }

                // Update status based on whether scan was cancelled
                if (_cancellationTokenSource.Token.IsCancellationRequested)
                {
                    StatusTitleLabel.Text = "Scan Cancelled";
                    StatusMessageLabel.Text = $"Scanned {results.Count} images before cancellation, {flaggedCount} flagged";
                    StatusLabel.Text = "Cancelled";
                }
                else
                {
                    StatusTitleLabel.Text = "Scan Complete";
                    StatusMessageLabel.Text = $"Scanned {results.Count} images, {flaggedCount} flagged";
                    StatusLabel.Text = "Complete";
                }
            }
            catch (Exception ex)
            {
                StatusTitleLabel.Text = "Error";
                StatusMessageLabel.Text = ex.Message;
                await DisplayAlert("Error", $"Scan failed: {ex.Message}", "OK");
            }
            finally
            {
                _isScanning = false;
                StartScanButton.Text = "▶ Start Scan";
                StartScanButton.BackgroundColor = Color.FromArgb("#3B82F6"); // Primary
                AddFolderButton.IsEnabled = true;
                QuickScanButton.IsEnabled = true;
                ScanProgressBar.IsVisible = false;
                StatusLabel.Text = "Ready";
            }
        }

        private async void OnSettingsClicked(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new SettingsPage());
        }

        private void UpdateFolderList()
        {
            FolderListStack.Children.Clear();

            // Show/hide placeholder based on folder count
            FolderPlaceholderLabel.IsVisible = _selectedFolders.Count == 0;

            foreach (var folder in _selectedFolders)
            {
                var border = new Border
                {
                    BackgroundColor = Color.FromArgb("#0F172A"),
                    Stroke = Color.FromArgb("#334155"),
                    StrokeThickness = 1,
                    Padding = new Thickness(12, 10),
                    Margin = new Thickness(0, 0)
                };
                border.StrokeShape = new RoundRectangle { CornerRadius = 8 };

                var grid = new Grid
                {
                    ColumnDefinitions =
                    {
                        new ColumnDefinition { Width = GridLength.Auto },
                        new ColumnDefinition { Width = GridLength.Star },
                        new ColumnDefinition { Width = GridLength.Auto }
                    }
                };

                // Folder icon
                var icon = new Label
                {
                    Text = "📁",
                    FontSize = 16,
                    VerticalOptions = LayoutOptions.Center,
                    Margin = new Thickness(0, 0, 10, 0)
                };

                // Path label
                var label = new Label
                {
                    Text = folder,
                    FontSize = 13,
                    TextColor = Color.FromArgb("#E2E8F0"),
                    VerticalOptions = LayoutOptions.Center,
                    LineBreakMode = LineBreakMode.MiddleTruncation
                };

                // Remove button
                var removeButton = new Button
                {
                    Text = "✕",
                    FontSize = 14,
                    WidthRequest = 32,
                    HeightRequest = 32,
                    CornerRadius = 4,
                    BackgroundColor = Colors.Transparent,
                    TextColor = Color.FromArgb("#EF4444"),
                    CommandParameter = folder
                };
                removeButton.Clicked += OnRemoveFolderClicked;

                grid.Add(icon, 0, 0);
                grid.Add(label, 1, 0);
                grid.Add(removeButton, 2, 0);
                border.Content = grid;

                FolderListStack.Children.Add(border);
            }
        }

        private void OnRemoveFolderClicked(object? sender, EventArgs e)
        {
            if (sender is Button button && button.CommandParameter is string folder)
            {
                _selectedFolders.Remove(folder);
                UpdateFolderList();
                StatusMessageLabel.Text = $"Removed: {folder} ({_selectedFolders.Count} folder(s) selected)";
            }
        }

        private void OnClearFoldersClicked(object sender, EventArgs e)
        {
            _selectedFolders.Clear();
            UpdateFolderList();
            StatusMessageLabel.Text = "All folders cleared";
        }

        private async void OnViewResultsClicked(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new ResultsPage(_lastScanResults));
        }
    }
}
