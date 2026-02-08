@echo off
echo Building and publishing Inntinnsic for Windows...
dotnet publish -c Release -f net8.0-windows10.0.19041.0

:: Extract version from .csproj
for /f "tokens=*" %%v in ('powershell -NoProfile -Command "[xml]$x = Get-Content 'Inntinnsic.csproj'; $x.Project.PropertyGroup.ApplicationDisplayVersion"') do set APP_VERSION=%%v

echo.
echo Building installer for v%APP_VERSION%...
if not exist Publish mkdir Publish
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DAppVersion=%APP_VERSION% Inntinnsic.iss

echo.
echo Done! Installer created: Publish\Inntinnsic-v%APP_VERSION%-win-x64-Setup.exe
pause
