import os
import re
from datetime import datetime, timedelta

# === Configuration ===
LOG_DIR = "/sdcard/reg"
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

def calculate_price(entry_time, exit_time):
    """
    Example price calculation: 10 pesos per hour (rounded up)
    Modify this logic as needed.
    """
    t1 = datetime.strptime(entry_time, "%H:%M")
    t2 = datetime.strptime(exit_time, "%H:%M")
    if t2 < t1:
        t2 += timedelta(days=1)  # handle overnight entries
    hours = (t2 - t1).seconds / 3600
    price = round(hours * 10, 2)
    return price

def total_of_day():
    """Compute total price for all entries today."""
    if not os.path.exists(LOG_FILE):
        return 0.0

    today = datetime.now().strftime("%Y-%m-%d")
    total = 0.0
    with open(LOG_FILE, "r") as f:
        for line in f:
            if line.startswith(today):
                parts = line.strip().split("|", 1)
                if len(parts) < 2:
                    continue
                entry = parts[1].strip()
                try:
                    _, _, e1, e2 = parse_entry(entry)
                    total += calculate_price(e1, e2)
                except Exception:
                    continue
    return total

def send_discord(content):
    """Send a message to your Discord webhook."""
    if not DISCORD_WEBHOOK:
        return
    import requests
    requests.post(DISCORD_WEBHOOK, json={"content": content})

def main():
    entry = os.getenv("ENTRY")
    if not entry:
        print("⚠️ No entry provided (ENTRY env var missing).")
        return

    append_entry(entry)

    # Check if time is 18:45
    now = datetime.now().strftime("%H:%M")
    if now == "18:45":
        total = total_of_day()
        msg = f"💰 Total del día ({datetime.now().date()}): {total:.2f}"
        print(msg)
        send_discord(msg)

if __name__ == "__main__":
    main()