import requests
import json
import main
import user

# Dracula Color Palette
DRACULA_COLORS = {
    "purple": 0xBD93F9,
    "pink": 0xFF79C6,
    "cyan": 0x8BE9FD,
    "green": 0x50FA7B,
    "yellow": 0xF1FA8C,
    "orange": 0xFFB86C,
}

def send_discord_message(endpoint: str, payload: dict) -> None:
    """Send a POST request to the Discord webhook."""
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Message sent successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def top_login(data: list) -> None:
    """Handles top login data and sends results to Discord."""
    endpoint = main.webhook_discord_url
    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus = data[2]

    # Load user data from JSON
    with open("login.json", "r", encoding="utf-8") as f:
        login_data = json.load(f)
        user_info = login_data["cache"]["replaced"]["userGame"][0]
        name1 = user_info.get("name", "Unknown")
        fpids1 = user_info.get("friendCode", "N/A")

    # Prepare bonus message
    message_bonus = ""
    nl = "\n"
    if bonus != "No Bonus":
        message_bonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"
        if bonus.bonus_name:
            message_bonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

    # Build the Discord message payload
    payload = {
        "content": None,
        "embeds": [
            {
                "title": f"Fate/Grand Order Login Manager - {main.fate_region}",
                "description": f"Sign in success.\n\n{message_bonus}",
                "color": DRACULA_COLORS["pink"],
                "fields": [
                    {"name": "Master", "value": name1, "inline": True},
                    {"name": "Friend ID", "value": fpids1, "inline": True},
                    {"name": "Lvl.", "value": str(rewards.level), "inline": True},
                    {"name": "Summoning Tickets", "value": str(rewards.ticket), "inline": True},
                    {"name": "Saint Quartz", "value": str(rewards.stone), "inline": True},
                ],
                "thumbnail": {
                    "url": "https://static.atlasacademy.io/JP/External/FGOPoker/314.png"
                },
            }
        ],
    }

    send_discord_message(endpoint, payload)

def shop(item: str, quantity: int) -> None:
    """Logs shop activity to Discord."""
    endpoint = main.webhook_discord_url
    payload = {
        "content": None,
        "embeds": [
            {
                "title": f"Fate/Grand Order Shop Manager - {main.fate_region}",
                "description": "",
                "color": DRACULA_COLORS["cyan"],
                "fields": [
                    {
                        "name": "Da Vinci's Workshop",
                        "value": f"Used {40 * quantity} AP on x{quantity} {item}",
                        "inline": False,
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo3/images/commnet_chara10.png"
                },
            }
        ],
    }
    send_discord_message(endpoint, payload)

def drawFP(results: list) -> None:
    """Logs gacha results to Discord."""
    endpoint = main.webhook_discord_url
    payload = {
        "content": None,
        "embeds": [
            {
                "title": f"Fate/Grand Order Gacha Results - {main.fate_region}",
                "description": "Gacha draw complete.",
                "color": DRACULA_COLORS["green"],
                "fields": [
                    {"name": "Servants", "value": "\n".join(results["servants"]), "inline": False},
                    {"name": "Craft Essences", "value": "\n".join(results["craft_essences"]), "inline": False},
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/assets/img/contents/gacha.png"
                },
            }
        ],
    }
    send_discord_message(endpoint, payload)

def LTO_Gacha(results: list) -> None:
    """Logs limited-time gacha results to Discord."""
    endpoint = main.webhook_discord_url
    payload = {
        "content": None,
        "embeds": [
            {
                "title": f"Fate/Grand Order Limited-Time Gacha Results - {main.fate_region}",
                "description": "Limited-time gacha draw.",
                "color": DRACULA_COLORS["orange"],
                "fields": [
                    {"name": "Servants", "value": "\n".join(results["servants"]), "inline": False},
                    {"name": "Craft Essences", "value": "\n".join(results["craft_essences"]), "inline": False},
                    {"name": "Bonus", "value": results["bonus"], "inline": False},
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/assets/img/lto_gacha.png"
                },
            }
        ],
    }
    send_discord_message(endpoint, payload)

def Present(gifts: list) -> None:
    """Logs presents and items received to Discord."""
    endpoint = main.webhook_discord_url
    payload = {
        "content": None,
        "embeds": [
            {
                "title": f"Fate/Grand Order Present Box - {main.fate_region}",
                "description": "You have received gifts!",
                "color": DRACULA_COLORS["yellow"],
                "fields": [
                    {"name": "Gifts Received", "value": "\n".join(gifts), "inline": False},
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/assets/img/presents.png"
                },
            }
        ],
    }
    send_discord_message(endpoint, payload)

def handle_shop_activity(item: str, quantity: int) -> None:
    """Handle shop-related activities."""
    shop(item, quantity)
    print(f"Logged {quantity} {item} purchase.")

def handle_gacha_draw(servants: list, craft_essences: list) -> None:
    """Handle gacha draw activities."""
    results = {"servants": servants, "craft_essences": craft_essences}
    drawFP(results)

def handle_lto_gacha_draw(servants: list, craft_essences: list, bonus: str) -> None:
    """Handle limited-time gacha draw activities."""
    results = {"servants": servants, "craft_essences": craft_essences, "bonus": bonus}
    LTO_Gacha(results)

def handle_present_box(gifts: list) -> None:
    """Handle presents and gifts received."""
    Present(gifts)