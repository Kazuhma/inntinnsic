using System;
using Inntinnsic.Models;
using Microsoft.Maui.Controls;

namespace Inntinnsic.Views
{
    public partial class SettingsPage : ContentPage
    {
        private UserSettings _settings = new UserSettings();
        private bool _blurEnabled = true;

        public SettingsPage()
        {
            InitializeComponent();
            LoadSettings();
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
            if (e.Key == Windows.System.VirtualKey.Escape)
            {
                Navigation.PopAsync();
                e.Handled = true;
            }
        }
#endif

        private void LoadSettings()
        {
            _settings = UserSettings.Load();

            // Load detection sensitivity
            SensitivitySlider.Value = _settings.DetectionSensitivity;
            SensitivityValueLabel.Text = $"Current: {_settings.DetectionSensitivity:F2}";

            // Load flagged categories
            FemaleBreastExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("FEMALE_BREAST_EXPOSED");
            FemaleGenitaliaExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("FEMALE_GENITALIA_EXPOSED");
            MaleGenitaliaExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("MALE_GENITALIA_EXPOSED");
            AnusExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("ANUS_EXPOSED");
            ButtocksExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("BUTTOCKS_EXPOSED");
            BellyExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("BELLY_EXPOSED");

            // Load other settings
            AutoExportCheck.IsChecked = _settings.AutoExportResults;
            SkipHiddenCheck.IsChecked = _settings.SkipHiddenFiles;
            ConfirmDeletionsCheck.IsChecked = _settings.ConfirmFileDeletions;
            _blurEnabled = _settings.BlurFlaggedContent;
            UpdateBlurToggleAppearance();
        }

        private void OnSensitivityChanged(object sender, ValueChangedEventArgs e)
        {
            SensitivityValueLabel.Text = $"Current: {e.NewValue:F2}";
        }

        private void OnBlurToggleTapped(object sender, EventArgs e)
        {
            _blurEnabled = !_blurEnabled;
            UpdateBlurToggleAppearance();
        }

        private void UpdateBlurToggleAppearance()
        {
            if (_blurEnabled)
            {
                BlurToggle.TextColor = Color.FromArgb("#E2E8F0"); // Bright slate
                BlurToggle.Opacity = 1.0;
            }
            else
            {
                BlurToggle.TextColor = Color.FromArgb("#64748B"); // Grey
                BlurToggle.Opacity = 0.4;
            }
        }

        private async void OnSaveClicked(object sender, EventArgs e)
        {
            try
            {
                // Update settings from UI
                _settings.DetectionSensitivity = (float)SensitivitySlider.Value;

                // Update flagged categories
                _settings.FlaggedCategories.Clear();

                if (FemaleBreastExposedCheck.IsChecked)
                    _settings.FlaggedCategories.Add("FEMALE_BREAST_EXPOSED");
                if (FemaleGenitaliaExposedCheck.IsChecked)
                    _settings.FlaggedCategories.Add("FEMALE_GENITALIA_EXPOSED");
                if (MaleGenitaliaExposedCheck.IsChecked)
                    _settings.FlaggedCategories.Add("MALE_GENITALIA_EXPOSED");
                if (AnusExposedCheck.IsChecked)
                    _settings.FlaggedCategories.Add("ANUS_EXPOSED");
                if (ButtocksExposedCheck.IsChecked)
                    _settings.FlaggedCategories.Add("BUTTOCKS_EXPOSED");
                if (BellyExposedCheck.IsChecked)
                    _settings.FlaggedCategories.Add("BELLY_EXPOSED");

                // Update other settings
                _settings.AutoExportResults = AutoExportCheck.IsChecked;
                _settings.SkipHiddenFiles = SkipHiddenCheck.IsChecked;
                _settings.ConfirmFileDeletions = ConfirmDeletionsCheck.IsChecked;
                _settings.BlurFlaggedContent = _blurEnabled;

                // Save to file
                _settings.Save();

                await Navigation.PopAsync();
            }
            catch (Exception ex)
            {
                await DisplayAlert("Error", $"Failed to save settings: {ex.Message}", "OK");
            }
        }

        private void OnResetClicked(object sender, EventArgs e)
        {
            // Reset to default settings
            _settings = new UserSettings();

            // Update UI directly with defaults (don't load from file)
            SensitivitySlider.Value = _settings.DetectionSensitivity;
            SensitivityValueLabel.Text = $"Current: {_settings.DetectionSensitivity:F2}";

            FemaleBreastExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("FEMALE_BREAST_EXPOSED");
            FemaleGenitaliaExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("FEMALE_GENITALIA_EXPOSED");
            MaleGenitaliaExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("MALE_GENITALIA_EXPOSED");
            AnusExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("ANUS_EXPOSED");
            ButtocksExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("BUTTOCKS_EXPOSED");
            BellyExposedCheck.IsChecked = _settings.FlaggedCategories.Contains("BELLY_EXPOSED");

            AutoExportCheck.IsChecked = _settings.AutoExportResults;
            SkipHiddenCheck.IsChecked = _settings.SkipHiddenFiles;
            ConfirmDeletionsCheck.IsChecked = _settings.ConfirmFileDeletions;
            _blurEnabled = _settings.BlurFlaggedContent;
            UpdateBlurToggleAppearance();
        }
    }
}
