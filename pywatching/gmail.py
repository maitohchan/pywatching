from __future__ import print_function
import pickle
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import httplib2

from pywatching.date import Date


class Gmail(object):
    """Gmail class

    https://developers.google.com/gmail/api/quickstart/python

    Args:
        tmp_dir (str): temporary directory name

    Attributes:
        SCOPES (list of str): auth API
        msg_api (googleapiclient.discovery.Resource): message API
        id_file (str): Gmail IDs file
        token_file (str): token file
    """

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self, tmp_dir: str = "tmp"):
        self.__msg_api = None
        self.__id_file = os.path.join(tmp_dir, "gmail_ids.pkl")
        self.__token_file = os.path.join(tmp_dir, "token.pickle")

    def connect(self, credentials: str = "credentials.json") -> bool:
        """connect Gmail server.

        Args:
            credentials (str): credential file name
        Returns:
            bool: True if successful, False otherwise.
        """
        creds = None

        if os.path.exists(self.__token_file):
            with open(self.__token_file, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(credentials):
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            else:
                return False

            with open(self.__token_file, "wb") as token:
                pickle.dump(creds, token)

        try:
            service = build("gmail", "v1", credentials=creds)
        except httplib2.ServerNotFoundError:
            return False

        self.__msg_api = service.users().messages()
        return True

    def __create_query(self, address: str, date: Date) -> str:
        """create query.

        Args:
            address (str): email address
            date (Date): date
        Returns:
            str: query
        """
        return "from:{} after:{} before:{}".format(
            address, date.today(), date.tomorrow()
        )

    def __load_ids(self, address: str, date: str) -> dict:
        """load IDs from pickle file

        ret = {
            "date": date,
            "ids": {
                address1: [x,y,z,,,],
                address2: [a,b,c,,,]
            }
        }

        Args:
            address (str): email address
            date (Date): date
        Returns:
            dict: read data
        """
        ret = {"date": date, "ids": dict()}
        if os.path.exists(self.__id_file):
            with open(self.__id_file, "rb") as f:
                loaded_ids = pickle.load(f)
            if loaded_ids["date"] == date:
                ret = loaded_ids

        if address not in ret["ids"].keys():
            ret["ids"][address] = list()

        return ret

    def __save_ids(self, ids: dict):
        """save ID data in pickle file.

        Args:
            ids (dict): saved data
        """
        with open(self.__id_file, "wb") as f:
            pickle.dump(ids, f)

    def __extract_info(self, mid: str) -> tuple:
        """extract mail information, which are date, subject and snippet.

        Args:
            mid (str): message ID
        Returns:
            str, str, str: date, subject and snippet
        """
        info = self.__msg_api.get(userId="me", id=mid).execute()

        has_date = False
        has_subject = False
        for header in info["payload"]["headers"]:
            if not has_date and header["name"] == "Date":
                date = header["value"]
                has_date = True
            elif not has_subject and header["name"] == "Subject":
                subject = header["value"]
                has_subject = True
            if has_date and has_subject:
                break

        return date, subject, info["snippet"]

    def get_messages(self, address: str, date: str = None) -> list:
        """get messages.

        Args:
            address (str): email address
            date (str): date
        Returns:
            list: messages
        """
        retval = list()

        if self.__msg_api is None or address is None:
            return retval

        d = Date(date)
        try:
            msginfo = self.__msg_api.list(
                userId="me", maxResults=10, q=self.__create_query(address, d)
            ).execute()
        except httplib2.ServerNotFoundError:
            return retval

        if msginfo["resultSizeEstimate"] == 0:
            return retval

        ids = self.__load_ids(address, d.date)
        msgs = sorted(msginfo["messages"], key=lambda x: x["id"])

        for m in msgs:
            mid = m["id"]
            if mid in ids["ids"][address]:
                continue

            date, subject, snippet = self.__extract_info(mid)
            retval.append(
                {
                    "id": mid,
                    "msg": "Date: {}\nSubject: {}\n{}".format(date, subject, snippet),
                }
            )
            ids["ids"][address].append(mid)

        ids["date"] = d.date
        self.__save_ids(ids)
        return retval


if __name__ == "__main__":
    import sys
    import json

    with open("configs.json", "r") as f:
        configs = json.load(f)

    gm = Gmail()

    if not gm.connect(configs["gmail"]["credfile"]):
        print("Cannot connect Gmail.")
        sys.exit()

    for addr in configs["gmail"]["addrs"]:
        for m in gm.get_messages(addr):
            print(m["msg"])
