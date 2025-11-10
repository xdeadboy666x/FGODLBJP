import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging
import sys  # move this up, clean import order

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
webhook_discord_url = os.environ['webhookDiscord']
device_info = os.environ.get('DEVICE_INFO_SECRET')
appCheck = os.environ.get('APP_CHECK_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/xdeadboy666x/FGO-JP-NA-VerCode-Extractor/master/jp.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)
    return response_data['verCode']


def get_latest_appver():
    endpoint = "https://raw.githubusercontent.com/xdeadboy666x/FGO-JP-NA-VerCode-Extractor/master/jp.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)
    return response_data['appVer']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()
        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(1)
                logger.info(f"\n {'=' * 40} \n [+] 登录账号 \n {'=' * 40} ")
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(0.5)
                instance.lq001()
                time.sleep(0.5)
                instance.Present()
                time.sleep(0.5)
                instance.lq002()
                time.sleep(2)
                instance.buyBlueApple()
                time.sleep(1)
                instance.lq003()
                time.sleep(1)
                instance.drawFP()
                time.sleep(1)
                instance.LTO_Gacha()

            except Exception as ex:
                logger.error(ex)


# === Cobro GitHub Trigger Integration ===
def log_entry(entry: str) -> None:
    """
    Triggers the Cobro workflow on GitHub Actions with the given entry string.
    Example: log_entry("jetta auto 10:30 12:40")
    """
    github_token = os.getenv("GH_TOKEN")  # store your PAT as a GitHub secret or local env var
    github_repo = "D-Ramirez/FGO"         # replace with your repo
    workflow = "cobro.yml"                # must match the workflow file name

    url = f"https://api.github.com/repos/{github_repo}/actions/workflows/{workflow}/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
    }

    payload = {
        "ref": "master",                  # or "main", depending on your default branch
        "inputs": {"entry": entry}
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        r.raise_for_status()
        print(f"✅ Cobro workflow triggered successfully for: {entry}")

        # Optional: send confirmation to Discord
        confirmation = {"content": f"✅ Log entry sent: `{entry}`"}
        requests.post(webhook_discord_url, json=confirmation)

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to trigger Cobro workflow: {e}")
        error_notice = {
            "content": f"⚠️ Could not trigger Cobro workflow for `{entry}`\nError: {e}"
        }
        requests.post(webhook_discord_url, json=error_notice)


if __name__ == "__main__":
    # If script is called without arguments → run FGO login manager
    if len(sys.argv) == 1:
        main()

    # If arguments are given → trigger Cobro workflow
    else:
        entry = " ".join(sys.argv[1:])
        log_entry(entry)