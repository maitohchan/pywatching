from __future__ import print_function
import pickle
import os
import datetime
from typing import List
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


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

    def __get_today(self) -> str:
        """
        """
        return self.__dt2str(datetime.date.today())

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

    def __get_query(self, address: str, date: datetime.date) -> str:
        """
        """
        from_date = self.__get_previous_date(date)
        to_date = self.__get_next_date(date)
        return "from:{} after:{} before:{}".format(address, from_date, to_date)

    def __load_ids(self, date: str) -> dict:
        """
        """
        if os.path.exists(self.__id_file):
            with open(self.__id_file, "rb") as f:
                ids = pickle.load(f)
            if ids["date"] != date:
                ids = {"date": date, "ids": list()}
        else:
            ids = {"date": date, "ids": list()}
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
        return date, subject

    def get_messages(self, address: str, date: str = None):
        """
        """
        retval = list()

        date = self.__get_today() if date is None else date
        msginfo = self.__msg_api.list(
            userId="me", maxResults=10, q=self.__get_query(address, self.__str2dt(date))
        ).execute()

        if msginfo["resultSizeEstimate"] == 0:
            return retval

        ids = self.__load_ids(date)

        for msg in msginfo["messages"]:
            mid = msg["id"]
            if mid in ids["ids"]:
                continue

            date, subject = self.__extract_date_and_subject(mid)
            retval.append(
                "Date: {}\nSubject: {}\n{}".format(date, subject, msg["snippet"])
            )
            ids["ids"].append(mid)

        ids["date"] = date
        self.__save_ids(ids)
        return retval


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("email", type=str)
    args = parser.parse_args()

    gmail = Gmail("credentials.json")
    ret = gmail.get_messages(args.email)
