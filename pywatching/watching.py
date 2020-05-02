from pywatching.googlehome import GoogleHome
from pywatching.line import Line
from pywatching.gmail import Gmail
from pywatching.logger import Logger

import argparse
import json
import os

lg = Logger(__name__)
lg.set_logfile(os.path.join(os.getcwd(), "watching_system.log"))
logger = lg.logger


def alarm(configs):
    for a in configs["googlehome"]["ip_addrs"]:
        gh = GoogleHome(ip_addr=a)
        gh.play(configs["googlehome"]["mp3_url"])
    return True


def notify(configs):
    ln = Line(configs["line"]["token"])
    gm = Gmail()

    if not gm.connect(configs["gmail"]["credfile"]):
        logger.debug("Cannot connect Gmail.")
        return False

    for addr in configs["gmail"]["addrs"]:
        logger.info(addr)
        for m in gm.get_messages(addr):
            ret = ln.notify(message=m["msg"])
            log = "Success: " if ret else "Fail "
            log += addr + " (id = " + m["id"] + ")"
            logger.info(log)

    return True


def main():
    logger.info("--- start logging ---")

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

    ret = func[args.type](configs)
    logger.info(args.type + " -> " + str(ret))
    logger.info("--- end logging ---")


if __name__ == '__main__':
    main()
