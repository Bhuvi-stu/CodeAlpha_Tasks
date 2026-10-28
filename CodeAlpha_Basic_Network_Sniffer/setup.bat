@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
    echo Python was not found. Install Python 3.10 or newer from https://www.python.org/downloads/
    echo During installation, enable "Add Python to PATH", then try again.
    pause
    exit /b 1
)

py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
    echo Python 3.10 or newer is required. Install it, then run setup.bat again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating this project's private Python environment...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Could not create the Python environment.
        pause
        exit /b 1
    )
)

echo Installing project dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed. Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Setup complete. You can now double-click run.bat to start a short capture.
pause
