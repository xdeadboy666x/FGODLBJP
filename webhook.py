import main
import requests
import user
import json

# Define Dracula color palette
dracula_colors = {
    "purple": 0xBD93F9,
    "pink": 0xFF79C6,
    "cyan": 0x8BE9FD,
    "green": 0x50FA7B,
    "yellow": 0xF1FA8C,
    "orange": 0xFFB86C,
}

def topLogin(data: list) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]
    with open("login.json", "r", encoding="utf-8") as f:
        data22 = json.load(f)

        name1 = data22["cache"]["replaced"]["userGame"][0]["name"]
        fpids1 = data22["cache"]["replaced"]["userGame"][0]["friendCode"]

    messageBonus = ""
    nl = "\n"

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name is not None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "Fate/Grand Order Login Manager - " + main.fate_region,
                "description": f"Sign in success.\n\n{messageBonus}",
                "color": dracula_colors["pink"],
                "fields": [
                    {"name": "Master", "value": f"{name1}", "inline": True},
                    {"name": "Friend ID", "value": f"{fpids1}", "inline": True},
                    {"name": "Lvl.", "value": f"{rewards.level}", "inline": True},
                    {"name": "Summoning Tickets", "value": f"{rewards.ticket}", "inline": True},
                    {"name": "Saint Quartz", "value": f"{rewards.stone}", "inline": True},
                    {"name": "Saint Quartz Fragments", "value": f"{rewards.sqf01}", "inline": True},
                    {"name": "Golden Fruits", "value": f"{rewards.goldenfruit}", "inline": True},
                    {"name": "Silver Fruits", "value": f"{rewards.silverfruit}", "inline": True},
                    {"name": "Bronze Fruits", "value": f"{rewards.bronzefruit}", "inline": True},
                    {"name": "Bronzed Cobalt Fruits", "value": f"{rewards.bluebronzefruit}", "inline": True},
                    {"name": "Bronze Saplings", "value": f"{rewards.bluebronzesapling}", "inline": True},
                    {"name": "Daily Login Streak", "value": f"{login.login_days}", "inline": True},
                    {"name": "Total Days Played", "value": f"{login.total_days}", "inline": True},
                    {"name": "Pure Prisms", "value": f"{rewards.pureprism}", "inline": True},
                    {"name": "FP", "value": f"{login.total_fp}", "inline": True},
                    {"name": "Gained FP", "value": f"+{login.add_fp}", "inline": True},
                    {"name": "Current AP", "value": f"{login.remaining_ap}", "inline": True},
                    {"name": "Holy Grails", "value": f"{rewards.holygrail}", "inline": True},
                ],
                "thumbnail": {
                    "url": "https://static.atlasacademy.io/JP/External/FGOPoker/314.png"
                },
            }
        ],
        "attachments": [],
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=jsonData, headers=headers)
        response.raise_for_status()
        print("topLogin response:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def shop(item: str, quantity: str) -> None:
    endpoint = main.webhook_discord_url

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "Fate/Grand Order Shop Manager - " + main.fate_region,
                "description": f"",
                "color": dracula_colors["cyan"],
                "fields": [
                    {
                        "name": f"Da Vinci's Workshop",
                        "value": f"Used {40 * quantity} AP on x{quantity} {item}",
                        "inline": False,
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo3/images/commnet_chara10.png"
                },
            }
        ],
        "attachments": [],
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=jsonData, headers=headers)
        response.raise_for_status()
        print("shop response:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def drawFP(servants, missions) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""

    if len(servants) > 0:
        servants_atlas = requests.get(
            "https://api.atlasacademy.io/export/JP/basic_svt_lang_en.json"
        ).json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            objectId = servant.objectId
            if objectId in svt_dict:
                svt = svt_dict[objectId]
                message_servant += f"`{svt['name']}` "
            else:
                continue

    if len(missions) > 0:
        for mission in missions:
            message_mission += (
                f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"
            )

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "Fate/Grand Order FP Summon Manager - " + main.fate_region,
                "description": f"FP Summoning done. Gacha results. \n\n{message_mission}",
                "color": dracula_colors["green"],
                "fields": [
                    {"name": "FP Gacha", "value": f"{message_servant}", "inline": False}
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara02_rv.png"
                },
            }
        ],
        "attachments": [],
    }

    headers = {"Content-Type": "application/json"}

    requests.post(endpoint, json=jsonData, headers=headers)


def LTO_Gacha(servants) -> None:
    endpoint = main.webhook_discord_url

    message_servant = ""

    if len(servants) > 0:
        servants_atlas = requests.get(
            "https://api.atlasacademy.io/export/JP/basic_svt_lang_en.json"
        ).json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            objectId = servant.objectId
            if objectId in svt_dict:
                svt = svt_dict[objectId]
                message_servant += f"`{svt['name']}` "
            else:
                continue

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Limited Summoning - " + main.fate_region,
                "description": f"Gacha results.",
                "color": dracula_colors["green"],
                "fields": [
                    {"name": "Gacha", "value": f"{message_servant}", "inline": False}
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara02_rv.png"
                },
            }
        ],
        "attachments": [],
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=jsonData, headers=headers)
        response.raise_for_status()
        print("LTO_gacha response:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def Present(name, namegift, object_id_count) -> None:
    endpoint = main.webhook_discord_url

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Exchange System - JP",
                "description": "Exchange done.",
                "color": dracula_colors["orange"],
                "fields": [
                    {
                        "name": f"{name}",
                        "value": f"{namegift} x{object_id_count}",
                        "inline": False,
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo2/images/commnet_chara06.png"
                },
            }
        ],
        "attachments": [],
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
    	response = requests.post(endpoint, json=jsonData, headers=headers)
        response.raise_for_status()
        print("Present response:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
