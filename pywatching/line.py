import requests


class Line(object):
    API = 'https://notify-api.line.me/api/notify'

    def __init__(self, token):
        self.token = token

    def notify(self, message, filename=None):
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + self.token}
        files = {'imageFile': open(filename, 'rb')} if filename else None
        res = requests.post(self.API, data=payload, headers=headers, files=files)
        return res.status_code == 200


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('token', help='LINE token')
    args = parser.parse_args()

    line = Line(args.token)
    line.notify(message='test')
