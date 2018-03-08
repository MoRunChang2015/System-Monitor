#!/usr/bin/python3


import logging
import json
import socket
import time
import copy
from utils import runner
from utils.co import coroutine
from socketFunc.func import accept, recv
from protocol.package import PackageFactory
from influxdb import InfluxDBClient

CONFIG_PATH = "./etc/config.json"

config = None
logger = None
client = None

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

def getUTCTime(timestamp=None):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))

def switchToDb(db_name):
    global client
    db_list = client.get_list_database()
    for item in db_list:
        if item['name'] == db_name:
            client.switch_database(db_name)
            return
    client.create_database(db_name)

def writePoints(points):
    global client, logger
    logger.info("Write {0} points into database...".format(len(points)))
    client.write_points(points)

@coroutine
def handle(connection):
    factory = PackageFactory.get_instance()
    global logger
    while True:
        data = yield recv(connection)
        if not data:
            break
        global logger
        logger.info("Receive data(len = {0} from {1}".format(len(data), connection.getpeername()))
        data = data.decode('utf-8')
        package = PackageFactory.push(factory, data)
        while package is not None:
            if 'Alert' in package:
                logger.error("Found Alert {3}, Alert Host: {0} at {1} msg: {2}".format(package['hostname'],
                                                                                       getUTCTime(package['timestamp']),
                                                                                       package['msg'],
                                                                                       package['Alert']))
            else:
                db_name = package['hostname']
                switchToDb(db_name)
                point = {
                    'measurement': "",
                    'tags': {"host": db_name},
                    "time": getUTCTime(package['timestamp']),
                    'fields': {
                        'value': None
                    }
                }
                points = []
                for item in package:
                    if item == "timestamp" or item == "hostname":
                        continue
                    if item == 'BEAT':
                        # TODO
                        continue
                    new_point = copy.deepcopy(point)
                    new_point['measurement'] = item
                    new_point['fields']['value'] = package[item]
                    points.append(new_point)
                writePoints(points)
            package = PackageFactory.pop(factory)


def initDBClinet():
    global config, client, logger
    client = InfluxDBClient(config['db']['host'], config['db']['port'],
                            config['db']['user'], config['db']['password'], 'example')
    logger.info("Connect to {0}:{1} with User: {2}".format(config['db']['host'],
                                                         config['db']['port'],
                                                         config['db']['user']))

@coroutine
def start(t_config):
    global config
    config = t_config
    initLogger()
    initDBClinet()
    global logger
    logger.info("Initialize server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind((config["ip"], config["port"]))
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
