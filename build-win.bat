@echo off
echo Building inntinnsic for Windows (Release)...
echo.

dotnet build -f net8.0-windows10.0.19041.0 -c Release

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build completed successfully!
) else (
    echo.
    echo Build failed with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
