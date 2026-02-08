@echo off
echo Building and publishing Inntinnsic for Windows...
dotnet publish -c Release -f net8.0-windows10.0.19041.0

:: Extract version from .csproj
for /f "tokens=*" %%v in ('powershell -NoProfile -Command "[xml]$x = Get-Content 'Inntinnsic.csproj'; $x.Project.PropertyGroup.ApplicationDisplayVersion"') do set APP_VERSION=%%v

echo.
echo Creating release archive for v%APP_VERSION%...
if not exist Publish mkdir Publish
powershell -NoProfile -Command "Compress-Archive -Path 'bin\Release\net8.0-windows10.0.19041.0\win-x64\publish\*' -DestinationPath 'Publish\Inntinnsic-v%APP_VERSION%-win-x64.zip' -Force"

echo.
echo Done! Release package created: Publish\Inntinnsic-v%APP_VERSION%-win-x64.zip
pause
