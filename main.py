from pywatching.line import Line
from pywatching.gmail import Gmail

import json
import sys


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", type=str, default="./configs.json")
    args = parser.parse_args()

    with open(args.configs, 'r') as f:
        configs = json.load(f)

    ln = Line(configs["line"]["token"])
    gm = Gmail()

    if not gm.connect(configs["gmail"]["credfile"]):
        print("Cannot connect Gmail.")
        sys.exit(1)

    for addr in configs["gmail"]["addrs"]:
        for m in gm.get_messages(addr):
            ret = ln.notify(message=m["msg"])
            log = "Success: " if ret else "Fail "
            log += addr + " (id = " + m["id"] + ")"
            print(log)

    sys.exit(0)
