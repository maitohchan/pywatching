from pywatching.ghome import GoogleHomeMini
import json


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", type=str, default="./configs.json")
    args = parser.parse_args()

    with open(args.configs, 'r') as f:
        configs = json.load(f)

    for a in configs["ghome"]["ip_addrs"]:
        ghm = GoogleHomeMini(ip_addr=a)
        ghm.play(configs["ghome"]["mp3_url"])
