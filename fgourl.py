import json
import binascii
import requests
import main
import CatAndMouseGame
import os

requests.urllib3.disable_warnings()
session = requests.Session()
session.verify = False

# ===== Game's parameters =====
app_ver_ = ''
data_ver_ = 0
date_ver_ = 0
ver_code_ = ''
asset_bundle_folder_ = ''
data_server_folder_crc_ = 0
server_addr_ = 'https://game.fate-go.jp'
github_token_ = ''
github_name_ = ''


# ==== User Info ====
def set_latest_assets():
    global app_ver_, data_ver_, date_ver_, asset_bundle_folder_, data_server_folder_crc_, ver_code_, server_addr_

    region = main.fate_region

    # Set Game Server Depends of region

    if region == "NA":
        server_addr_ = "https://game.fate-go.us"