from __future__ import print_function
import pickle
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pywatching.date import Date


class Gmail(object):
    """

    https://developers.google.com/gmail/api/quickstart/python

    Args:
        credentials (str):

    Attributes:
        SCOPES (list of str):
        service :

    """

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self, tmp_dir: str = "tmp"):
        self.__msg_api = None
        self.__id_file = os.path.join(tmp_dir, "gmail_ids.pkl")

    def connect(self, credentials: str = 'credentials.json'):
        """

        """
        creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(credentials):
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, self.SCOPES
                )
                creds = flow.run_local_server()
            else:
                return False

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        try:
            service = build("gmail", "v1", credentials=creds)
        except:
            return False

        self.__msg_api = service.users().messages()
        return True

    def __get_query(self, address: str, date: Date) -> str:
        """
        """
        from_date = date.yesterday()
        to_date = date.tomorrow()
        print(to_date)
        query = "from:{} after:{} before:{}".format(address, from_date, to_date)
        print(query)
        return query

    def __load_ids(self, address :str, date: str) -> dict:
        """
        """
        ids = {address: {"date": date, "ids": list()}}
        if os.path.exists(self.__id_file):
            with open(self.__id_file, "rb") as f:
                loaded_ids = pickle.load(f)
            if loaded_ids[address]["date"] == date:
                ids = loaded_ids

        return ids

    def __save_ids(self, ids):
        """
        """
        with open(self.__id_file, "wb") as f:
            pickle.dump(ids, f)

    def __extract_date_and_subject(self, mid):
        """
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

    def get_messages(self, address: str, date: str = None):
        """
        """
        retval = list()

        if self.__msg_api is None or address is None:
            return retval

        d = Date(date)
        try:
            msginfo = self.__msg_api.list(
                userId="me", maxResults=10, q=self.__get_query(address, d)
            ).execute()
        except:
            print("ppp")
            return retval

        if msginfo["resultSizeEstimate"] == 0:
            return retval

        ids = self.__load_ids(address, d.date)
        print(ids)

        for msg in msginfo["messages"]:
            mid = msg["id"]
            if mid in ids[address]["ids"]:
                continue

            date, subject, snippet = self.__extract_date_and_subject(mid)
            retval.append(
                "Date: {}\nSubject: {}\n{}".format(date, subject, snippet)
            )
            ids[address]["ids"].append(mid)

        ids[address]["date"] = d.date
        self.__save_ids(ids)
        return retval


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--cred", type=str)
    parser.add_argument("--email", type=str)
    parser.add_argument("--date", type=str)
    args = parser.parse_args()

    gmail = Gmail()
    if gmail.connect():
        print(gmail.get_messages(args.email, args.date))
    else:
        print("Cannot connect.")
