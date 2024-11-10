import requests
import json
import main

from mytime import GetTimeStamp


def GetGachaSubIdFP():
    response = requests.get(
        f"https://git.atlasacademy.io/atlasacademy/fgo-game-data/raw/branch/JP/master/mstGachaSub.json"
    )
    gachaList = json.loads(response.text)
    timeNow = GetTimeStamp()
    priority = 0
    goodGacha = {}

    for gacha in gachaList:
        openedAt = gacha["openedAt"]
        closedAt = gacha["closedAt"]

        # Fixing logical operators
        if openedAt <= timeNow and timeNow <= closedAt:
            p = int(gacha["priority"])
            if p > priority:
                priority = p
                goodGacha = gacha

    # Verify whether a suitable gacha has been found
    if not goodGacha:
        main.logger.info("No suitable gacha found")
        return None

    # Confirm the 'id' Key exists
    if "id" not in goodGacha:
        main.logger.info("Key 'id' not found in the selected gacha")
        return None

    return str(goodGacha["id"])
