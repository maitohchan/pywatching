from pywatching.googlehome import GoogleHome
import json


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", type=str, default="./configs.json")
    args = parser.parse_args()

    with open(args.configs, 'r') as f:
        configs = json.load(f)

    for a in configs["googlehome"]["ip_addrs"]:
        gh = GoogleHome(ip_addr=a)
        gh.play(configs["googlehome"]["mp3_url"])
