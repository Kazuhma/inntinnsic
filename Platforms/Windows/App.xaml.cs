using Microsoft.UI.Xaml;
using System;
using System.Runtime.InteropServices;
using System.Threading;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace Inntinnsic.WinUI
{
    /// <summary>
    /// Provides application-specific behavior to supplement the default Application class.
    /// </summary>
    public partial class App : MauiWinUIApplication
    {
        private static Mutex? _mutex;
        private const string MutexName = "InntinnsicSingleInstanceMutex";

        // Windows API imports for window manipulation
        [DllImport("user32.dll")]
        private static extern bool SetForegroundWindow(IntPtr hWnd);

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        [DllImport("user32.dll")]
        private static extern bool IsIconic(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern IntPtr FindWindow(string? lpClassName, string lpWindowName);

        private const int SW_RESTORE = 9;
        private const int SW_SHOW = 5;

        /// <summary>
        /// Initializes the singleton application object.  This is the first line of authored code
        /// executed, and as such is the logical equivalent of main() or WinMain().
        /// </summary>
        public App()
        {
            // Check if another instance is already running
            _mutex = new Mutex(true, MutexName, out bool createdNew);

            if (!createdNew)
            {
                // Another instance is running, try to bring it to foreground
                BringExistingInstanceToFront();

                // Exit this instance
                Environment.Exit(0);
                return;
            }

            this.InitializeComponent();
        }

        private void BringExistingInstanceToFront()
        {
            // Try to find the window by title
            // The window title is set in MainPage or the app name
            IntPtr hWnd = FindWindow(null, "Inntinnsic");

            if (hWnd == IntPtr.Zero)
            {
                // Try with the full title that might include version or other info
                hWnd = FindWindow(null, "Inntinnsic - Image Safety Checker");
            }

            if (hWnd != IntPtr.Zero)
            {
                // If window is minimized, restore it
                if (IsIconic(hWnd))
                {
                    ShowWindow(hWnd, SW_RESTORE);
                }
                else
                {
                    ShowWindow(hWnd, SW_SHOW);
                }

                // Bring window to foreground
                SetForegroundWindow(hWnd);
            }
        }

        protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
    }
}
