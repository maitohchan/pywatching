import pytest
from pywatching.line import Line


class TestLine(object):
    LINE_API = "https://notify-api.line.me/api/notify"
    LINE_TOKEN = "apikey-xxx"

    @pytest.fixture()
    def motion(self):
        return Line(self.LINE_TOKEN)

    @pytest.mark.parametrize(("code", "expected"), [(200, True), (400, False)])
    def test_notify(self, motion, mocker, code, expected):
        resMock = mocker.Mock()
        resMock.status_code = code
        mocked_post = mocker.patch("requests.post")
        mocked_post.return_value = resMock

        message = "detected!"
        filename = None
        ret = motion.notify(message, filename)
        assert ret is expected
        mocked_post.assert_called_once_with(
            self.LINE_API,
            data={"message": message},
            headers={"Authorization": "Bearer " + self.LINE_TOKEN},
            files=None,
        )
