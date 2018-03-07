#!/usr/bin/python3

import json
from core import agent

CONFIG_PATH = './etc/config.json'

def main():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        agent.start(config)
        return
    print("Open {0} fail!, exit...".format(CONFIG_PATH))

if __name__ == "__main__":
    main()
