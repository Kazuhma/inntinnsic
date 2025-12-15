@echo off
REM Build script for Inntinnsic using PyInstaller

echo Building Inntinnsic standalone executable...
echo.

REM Activate pipenv environment and build
pipenv run pyinstaller build.spec --clean

echo.
echo Build complete!
echo Executable located in: dist\Inntinnsic\Inntinnsic.exe
echo.
pause
