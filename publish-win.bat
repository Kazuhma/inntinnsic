@echo off
echo Building and publishing Inntinnsic for Windows...
dotnet publish -c Release -f net8.0-windows10.0.19041.0

echo.
echo Creating release archive...
powershell -Command "Compress-Archive -Path bin\Release\net8.0-windows10.0.19041.0\win-x64\publish\* -DestinationPath Inntinnsic-v3.1-win-x64.zip -Force"

echo.
echo Done! Release package created: Inntinnsic-v3.1-win-x64.zip
pause
