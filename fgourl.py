import json
import binascii
import requests
import os
import main
import CatAndMouseGame

# Constants
NA_SERVER = "https://game.fate-go.us"
JP_SERVER = "https://game.fate-go.jp"

# Initialize session
session = requests.Session()
session.verify = False
requests.urllib3.disable_warnings()

# ==== Game Info ====
app_ver = ""
data_ver = 0
date_ver = 0
ver_code = ""
asset_bundle_folder = ""
data_server_folder_crc = 0

# ==== Headers ====
user_agent_2 = os.getenv("USER_AGENT_SECRET_2")
if not user_agent_2:
    raise ValueError("USER_AGENT_SECRET_2 environment variable not set")

httpheader = {
    "User-Agent": user_agent_2,
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Unity-Version": "2022.3.28f1",
}


def set_latest_assets():
    """
    Fetch the latest game version details and set game assets info.
    """
    global app_ver, data_ver, date_ver, asset_bundle_folder, data_server_folder_crc, ver_code

    server_addr = JP_SERVER if main.fate_region != "NA" else NA_SERVER

    version_str = main.get_latest_appver()
    response = session.get(f"{server_addr}/gamedata/top?appVer={version_str}")
    response_data = response.json()["response"][0]["success"]

    # Set version details
    app_ver = version_str
    data_ver = response_data["dataVer"]
    date_ver = response_data["dateVer"]
    ver_code = main.get_latest_verCode()

    # Extract folder data
    assetbundle = CatAndMouseGame.getAssetBundle(response_data["assetbundle"])
    get_folder_data(assetbundle)


def get_folder_data(assetbundle):
    """
    Extract folder data and compute its CRC32.
    """
    global asset_bundle_folder, data_server_folder_crc

    asset_bundle_folder = assetbundle["folderName"]
    data_server_folder_crc = binascii.crc32(asset_bundle_folder.encode("utf8"))


def post_request(session, url, data):
    """
    Send a POST request and return the response.

    Args:
        session: The requests session to use.
        url: The endpoint to send the request.
        data: The data to include in the POST request.

    Returns:
        dict: JSON response if successful.

    Raises:
        Exception: If the response contains an error code.
    """
    try:
        res = session.post(url, data=data, headers=httpheader, verify=False)
        res.raise_for_status()
        res_json = res.json()

        res_code = res_json["response"][0]["resCode"]
        if res_code != "00":
            detail = res_json["response"][0]["fail"]["detail"]
            raise Exception(f"[ErrorCode: {res_code}] {detail}")

        return res_json

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        rais
