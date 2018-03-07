#!/usr/bin/python3


import logging
import time
import json
from . import globalVar
from .attribute import AttributeManager
from .alert import AlertManager
from .reporter import Reporter

def initLogger():
    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    fmt = "%(asctime)-12s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    data_fmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, data_fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def start(config):
    initLogger()
    globalVar.hostname = config["hostname"]
    globalVar.attributeManager = AttributeManager()
    globalVar.alertManager = AlertManager()
    globalVar.reporter = Reporter(config["hostname"], config["urls"])
    while True:
        time.sleep(1)
        tick()

def tick():
    count, ret = globalVar.attributeManager.update()
    if count != 0:
        ret["hostname"] = globalVar["hostname"]
        globalVar.reporter.appendMessage(json.dumps(ret))

    count, ret = globalVar.alertManager.update()
    if count != 0:
        for itemName in ret:
            msg = {"Alert": itemName, "msg": ret[itemName],
                   "hostname": globalVar.hostname,
                   "timestamp": ret["timestamp"]}
            globalVar.reporter.appendMessage(json.dumps(msg))
