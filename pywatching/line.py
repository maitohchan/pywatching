import requests


class Line(object):
    """LINE class to notify message and file data.

    https://notify-bot.line.me/ja/

    Args:
        token (str): LINE Token
    Attributes:
        token (str): LINE Token
    """

    API = "https://notify-api.line.me/api/notify"

    def __init__(self, token: str):
        self.token = token

    def notify(self, message: str, filename=None):
        """Notify message and file data.

        Args:
            message (str): LINE message
            filename (str): filename of data sent as imageFile
        Returns:
            bool: True if successful, False otherwise.
        """
        payload = {"message": message}
        headers = {"Authorization": "Bearer " + self.token}
        files = {"imageFile": open(filename, "rb")} if filename else None
        res = requests.post(self.API, data=payload, headers=headers, files=files)
        return res.status_code == 200


"""
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="LINE token")
    args = parser.parse_args()

    line = Line(args.token)
    line.notify(message="test")
"""
