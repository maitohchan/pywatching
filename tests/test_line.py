import pytest
from pywatching.line import Line


class TestLine(object):
    LINE_API = "https://notify-api.line.me/api/notify"
    LINE_TOKEN = "apikey-xxx"

    @pytest.fixture()
    def motion(self):
        return Line(self.LINE_TOKEN)

    @pytest.mark.parametrize(
        ("code", "filename", "expected"),
        [(200, None, True), (200, "image.jpeg", True), (400, None, False)],
    )
    def test_notify(self, motion, mocker, code, filename, expected):
        resMock = mocker.Mock()
        resMock.status_code = code
        mocked_post = mocker.patch("requests.post")
        mocked_post.return_value = resMock

        message = "detected!"
        if filename is not None:
            mocked_open = mocker.patch("builtins.open")
            mocked_open.return_value = "file_data"

        ret = motion.notify(message, filename)
        assert ret is expected
        mocked_post.assert_called_once_with(
            self.LINE_API,
            data={"message": message},
            headers={"Authorization": "Bearer " + self.LINE_TOKEN},
            files=None if filename is None else {"imageFile": "file_data"},
        )
