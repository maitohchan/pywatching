import datetime


class Date(object):
    """Date Class

    if date is None, date is set to today.

    Args:
        date (str): YYYY/MM/DD
    Arguments:
        dt (datetime): coverted date to datetime
    """

    def __init__(self, date: str = None):
        self.__dt = self.__str2dt(date) if date else datetime.datetime.now()

    @property
    def date(self) -> str:

        """retun current date

        Returns:
            str: current date
        """
        return self.__dt.strftime("%Y/%m/%d")

    @property
    def time(self) -> str:
        """retun current time

        Returns:
            str: current time
        """
        return self.__dt.strftime("%H:%M:%S")

    @staticmethod
    def __str2dt(date: str) -> datetime:
        """convert string to datetime

        Args:
            date (str): string date
        Returns:
            datetime: coverted date to datetime
        """
        return datetime.datetime.strptime(date, "%Y/%m/%d")

    def yesterday(self) -> str:
        """return previous date

        Returns:
            datetime: previous date
        """
        return (self.__dt + datetime.timedelta(days=-1)).strftime("%Y/%m/%d")

    def tomorrow(self) -> str:
        """return next date

        Returns:
            datetime: next date
        """
        return (self.__dt + datetime.timedelta(days=1)).strftime("%Y/%m/%d")

    def today(self) -> str:
        """return today

        Returns:
            datetime: today
        """
        return self.__dt.strftime("%Y/%m/%d")
