from __future__ import print_function
import pickle
import os
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from line import Line


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

    def __init__(self, credentials: str = "credentials.json", tmp_dir: str = "tmp"):
        service = self.__connect(credentials)
        self.__msg_api = service.users().messages()
        self.__id_file = os.path.join(tmp_dir, "gmail_ids.pkl")

    def __connect(self, credentials: str):
        """

        """
        creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, self.SCOPES
                )
                creds = flow.run_local_server()

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build("gmail", "v1", credentials=creds)

    @staticmethod
    def __str2dt(date: str) -> datetime.date:
        """
        """
        return datetime.datetime.strptime(date, "%Y/%m/%d")

    @staticmethod
    def __dt2str(dt: datetime.date) -> str:
        """
        """
        return dt.strftime("%Y/%m/%d")

    @staticmethod
    def __get_today() -> datetime.date:
        """
        """
        return datetime.date.today()

    @staticmethod
    def __get_previous_date(dt: datetime.date) -> datetime.date:
        """
        """
        return dt + datetime.timedelta(days=-1)

    @staticmethod
    def __get_next_date(dt: datetime.date) -> datetime.date:
        """
        """
        return dt + datetime.timedelta(days=1)

    def __get_query(self, address: str, date: str = None) -> str:
        """
        """
        today = self.__get_today() if date is None else self.__str2dt(date)
        from_date = self.__get_previous_date(today)
        to_date = self.__get_next_date(today)
        return "from:{} after:{} before:{}".format(
            address, self.__dt2str(from_date), self.__dt2str(to_date)
        )

    def __load_ids(self) -> list:
        """
        """
        if os.path.exists(self.__id_file):
            with open(self.__id_file, "rb") as f:
                ids = pickle.load(f)
        else:
            ids = list()
        return ids

    def __save_ids(self):
        """
        """
        with open(self.__id_file, "wb") as f:
            pickle.dump(self.__id_list, f)

    def __extract_date_and_subject(self, mid):
        """
        """
        info = self.__msg_api.get(userId="me", id=mid).execute()

        has_date = False
        has_subject = False
        for header in info["payload"]["headers"]:
            if header["name"] == "Date":
                date = header["value"]
                has_date = True
            elif header["name"] == "Subject":
                subject = header["value"]
                has_subject = True
            if has_date and has_subject:
                break
        return date, subject

    def get_message_list(self, address: str, date: str = None):
        """
        """
        retval = list()
        msginfo = self.__msg_api.list(
            userId="me", maxResults=10, q=self.__get_query(address, date)
        ).execute()

        if msginfo["resultSizeEstimate"] == 0:
            return retval

        ids = self.__load_ids()

        for msg in msginfo["messages"]:
            mid = msg["id"]
            if mid in ids:
                continue

            date, subject = self.__extract_date_and_subject(mid)
            retval.append(
                "Date: {}\nSubject: {}\n{}".format(date, subject, msg["snippet"])
            )
            ids.append(mid)

        self.__save_ids()
        return retval


def main():
    import config
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("email", type=str)
    args = parser.parse_args()

    line = Line(config.LINE_TOKEN)
    gmail = Gmail("credentials.json")
    ret = gmail.get_message_list(args.email)
    for r in ret:
        line.notify(message=r)


if __name__ == "__main__":
    main()
