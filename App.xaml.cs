using System.Reflection;

namespace Inntinnsic
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();
            // Set dark mode as default
            UserAppTheme = AppTheme.Dark;
        }

        public static string MauiVersion
        {
            get
            {
                var version = typeof(MauiApp).Assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()!.InformationalVersion;
                return $".NET MAUI ver. {version[..version.IndexOf('+')]}";
            }
        }
    }
}
