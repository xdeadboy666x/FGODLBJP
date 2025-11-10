import os
import re
import requests
from datetime import datetime, timedelta

# === Configuration ===
if os.path.exists("/sdcard"):
    LOG_DIR = "/sdcard/reg"
else:
    LOG_DIR = os.path.expanduser("~/reg")

LOG_FILE = os.path.join(LOG_DIR, "cobro.log")
DISCORD_WEBHOOK = os.getenv("webhookDiscord")

# === Ensure log directory exists ===
os.makedirs(LOG_DIR, exist_ok=True)

def append_entry(entry: str):
    """Append a new log entry with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {entry}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(f"✅ Logged: {line.strip()}")
    send_discord(f"📝 Nuevo registro: `{entry}`")

def parse_entry(entry: str):
    """
    Parse an entry like 'jetta auto 10:30 12:40'
    Returns (vehiculo, tipo, entry_time, exit_time)
    """
    pattern = r"^(\w+)\s+(\w+)\s+(\d{1,2}:\d{2})\s+(\d{1,2}:\d{2})$"
    match = re.match(pattern, entry.strip())
    if not match:
        raise ValueError(f"Invalid entry format: {entry}")
    return match.groups()

def calculate_price(vehicle_type: str, entry_time: str, exit_time: str):
    """Calculate price depending on vehicle type (10/h moto, 20/h auto)."""
    t1 = datetime.strptime(entry_time, "%H:%M")
    t2 = datetime.strptime(exit_time, "%H:%M")
    if t2 < t1:
        t2 += timedelta(days=1)

    hours = (t2 - t1).seconds / 3600
    rate = 10 if vehicle_type.lower() == "moto" else 20
    return round(hours * rate, 2)

def total_of_day():
    """Compute total price for all entries today."""
    if not os.path.exists(LOG_FILE):
        return 0.0

    today = datetime.now().strftime("%Y-%m-%d")
    total = 0.0
    with open(LOG_FILE, "r") as f:
        for line in f:
            if not line.startswith(today):
                continue
            parts = line.strip().split("|", 1)
            if len(parts) < 2:
                continue
            entry = parts[1].strip()
            try:
                _, tipo, e1, e2 = parse_entry(entry)
                total += calculate_price(tipo, e1, e2)
            except Exception:
                continue
    return total

def send_discord(content):
    """Send a message to your Discord webhook."""
    if not DISCORD_WEBHOOK:
        print("⚠️ No Discord webhook configured.")
        return
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": content})
    except Exception as e:
        print(f"⚠️ Discord error: {e}")

def main():
    entry = os.getenv("ENTRY")

    # If no entry is passed, assume it's a scheduled summary run
    if not entry:
        now = datetime.now()
        if now.hour == 18 and now.minute >= 45:
            total = total_of_day()
            msg = f"💰 Total del día ({datetime.now().date()}): ${total:.2f}"
            print(msg)
            send_discord(msg)
        else:
            print("ℹ️ No entry provided, and not time for summary.")
        return

    # Otherwise, log normal entry
    append_entry(entry)

    # Also send total automatically if it's 18:45+
    now = datetime.now()
    if now.hour == 18 and now.minute >= 45:
        total = total_of_day()
        msg = f"💰 Total del día ({datetime.now().date()}): ${total:.2f}"
        print(msg)
        send_discord(msg)

if __name__ == "__main__":
    main()