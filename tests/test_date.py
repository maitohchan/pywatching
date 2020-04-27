from pywatching.date import Date
import datetime


class TestDate(object):

    def test_initialize_with_date(self):
        date = "2020/05/04"
        assert Date(date).date == date

    def test_initialize_with_None(self):
        assert Date().date == datetime.date.today().strftime("%Y/%m/%d")

    def test_yesterday(self):
        assert Date().yesterday() == \
            (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y/%m/%d")

    def test_tomorrow(self):
        assert Date().tomorrow() == \
            (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")
