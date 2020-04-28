from pywatching.line import Line
from pywatching.gmail import Gmail

import json
import sys


def load_config(filename):
    with open(filename, 'r') as f:
        jsondata = json.load(f)
    return jsondata


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", type=str, default="./configs.json")
    args = parser.parse_args()

    configs = load_config(args.configs)
    ln = Line(configs["line"]["token"])
    gm = Gmail()

    if not gm.connect(configs["gmail"]["credfile"]):
        sys.exit(1)

    for addr in configs["gmail"]["addrs"]:
        for m in gm.get_messages(addr):
            ret = ln.notify(message=m["msg"])
            log = "Success: " if ret else "Fail "
            log += addr + "(" + m["id"] + ")"
            print(log)

    sys.exit(0)
