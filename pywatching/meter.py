import requests
import json

SWITCH_BOT_URL = "https://api.switch-bot.com/v1.0/devices"


class SwitchBot(object):
    def __init__(self, token: str, device_name: str) -> None:
        self._header = {"Authorization": token}
        self._device_name = device_name

    def connect(self) -> bool:
        response = requests.get(SWITCH_BOT_URL, headers=self._header)
        devices = json.loads(response.text)
        if devices["statusCode"] != 100:
            return False

        device_ids = [
            device["deviceId"]
            for device in devices["body"]["deviceList"]
            if self._device_name in device["deviceName"]
        ]

        if len(device_ids) != 1:
            return False

        self._device_id = device_ids[0]
        return True

    def get(self) -> dict:
        response = requests.get(
            SWITCH_BOT_URL + "/" + self._device_id + "/status", headers=self._header
        )
        res = json.loads(response.text)

        if res["statusCode"] != 100:
            raise
        return {
            "temperature": res["body"]["temperature"],
            "humidity": res["body"]["humidity"],
        }


if __name__ == "__main__":
    TOKEN = ""
    DEVUCE_NAME = "Meter A3"
    s = SwitchBot(TOKEN, DEVUCE_NAME)
    if not s.connect():
        raise
    params = s.get()
    print(params["temperature"])
    print(params["humidity"])
