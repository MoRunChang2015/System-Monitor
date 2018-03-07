#!/usr/bin/python3
# -*- coding: utf-8 -*-


import json
import logging
import socket
from utils import runner
from utils.co import coroutine
from socketFunc.func import accept, recv, send

CONFIG_PATH = "./etc/config.json"

logger = None
config = None

forward_server = {}

def initLogger():
    global logger
    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    fmt = "%(asctime)-12s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    data_fmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, data_fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@coroutine
def handle(socket):
    while True:
        data = yield recv(socket)
        if not data:
            break
        global logger
        logger.info("Receive data(len = {0} from {1}".format(len(data), socket.getpeername()))
        global config
        for server in config["forward_server"]:
            server_id = tuple(server["ip"], server["port"])
            global forward_server
            if server_id not in forward_server:
                new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                new_socket.settimeout(5)
                try:
                    new_socket.connect(server["ip"], server["port"])
                    logger.info("Connect to {0}:{1}".format(server["ip"], server["port"]))
                except:
                    logger.info("Can't connect to {0}:{1}".format(server["ip"], server["port"]))
                    continue
                forward_server[server_id] = new_socket
            yield send(forward_server[server_id], data)
            logger.info("Send data(len={0}) from {1} to {2}:{3}".format(len(data), socket.getpeername(), server["ip"], server["port"]))

@coroutine
def start(t_config):
    global config
    config = t_config
    initLogger()
    global logger
    logger.info("Initialize collector...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(config["ip"], config["port"])
    logger.info("listening {0}:{1}".format(config["ip"], config["port"]))
    server.listen(10)

    while True:
        connection = yield accept(server)
        if connection is None:
            break
        logger.info("New connection from {0}".format(connection.getpeername()))
        handle(connection)


def main():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        start(config)
        runner.timeout = config["timeout"]
        runner.run()
        return
    print("Open config file ({0}) fail!, exit...",format(CONFIG_PATH))

if __name__ == "__main__":
    main()
