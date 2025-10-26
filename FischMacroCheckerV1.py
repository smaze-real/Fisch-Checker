import time
import io
from datetime import datetime
from PIL import ImageGrab
import requests
import signal
import sys

# 🔗 Your Discord webhook
WEBHOOK = "https://discord.com/api/webhooks/1431859428428222589/38XggO8FgUUaaYFeeokXAj7CO-acZEWl--PH_Cer6GwBSQTvuXAnjMQUj1oYClaDTckR"

# ⏱ Screenshot interval in seconds
INTERVAL = 60

running = True

def send_screenshot():
    """Take a screenshot and send it to Discord."""
    try:
        img = ImageGrab.grab()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        files = {"file": ("screenshot.png", buf, "image/png")}
        data = {"content": f"📷 screenshot at {datetime.now():%Y-%m-%d %H:%M:%S}"}

        r = requests.post(WEBHOOK, data=data, files=files)

        if r.ok:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Screenshot sent.")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed: {r.status_code} {r.text}")

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")

def send_exit_message():
    """Send a message to Discord when the client is closing."""
    try:
        data = {"content": "⚠️ client closed FischMacroCheckerV1"}
        requests.post(WEBHOOK, data=data)
    except:
        pass  # Fail silently

def handle_exit(sig, frame):
    global running
    print("\nStopping automatic screenshots...")
    send_exit_message()
    running = False

# Bind Ctrl+C to stop
signal.signal(signal.SIGINT, handle_exit)

print("Starting automatic screenshots every 1 minute. Press Ctrl+C to stop.")

while running:
    send_screenshot()
    for _ in range(INTERVAL):
        if not running:
            break
        time.sleep(1)

print("Exited cleanly.")
