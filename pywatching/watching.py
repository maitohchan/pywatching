from pywatching.googlehome import GoogleHome
from pywatching.line import Line
from pywatching.gmail import Gmail

import json
import os


def alarm(configs):
    for a in configs["googlehome"]["ip_addrs"]:
        gh = GoogleHome(ip_addr=a)
        gh.play(configs["googlehome"]["mp3_url"])
    return True


def notify(configs):
    ln = Line(configs["line"]["token"])
    gm = Gmail()

    if not gm.connect(configs["gmail"]["credfile"]):
        print("Cannot connect Gmail.")
        return False

    for addr in configs["gmail"]["addrs"]:
        print(addr)
        for m in gm.get_messages(addr):
            ret = ln.notify(message=m["msg"])
            log = "Success: " if ret else "Fail "
            log += addr + " (id = " + m["id"] + ")"
            print(log)

    return True


def main():
    import argparse

    default_config_path = os.path.join(os.getcwd(), "configs.json")
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["alarm", "notify"])
    parser.add_argument("--configs", type=str, default=default_config_path)
    args = parser.parse_args()

    with open(args.configs, 'r') as f:
        configs = json.load(f)

    func = {
        "alarm": alarm,
        "notify": notify
    }

    func[args.type](configs)


if __name__ == '__main__':
    main()
