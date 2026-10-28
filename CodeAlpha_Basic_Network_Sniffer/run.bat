@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo First run setup.bat to install the project's Python dependencies.
    pause
    exit /b 1
)

echo Capturing up to 10 packets for at most 15 seconds.
echo Only capture traffic on your own computer or an authorized network.
echo.
".venv\Scripts\python.exe" sniffer.py --count 10 --timeout 15
if errorlevel 1 (
    echo.
    echo Capture did not complete. Check that Npcap is installed and that the network adapter is available.
)
echo.
pause
