#!/usr/bin/python3


import logging
import time
from . import globalVar

class AlertItem:

    def __init__(self, name, args, alertFunc):
        super().__init__()
        self.__args = args
        self.__name = name
        self.__func = alertFunc

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def test(self):
        argsList = []
        for item in self.__args:
            res = globalVar.attributeManager.getAttrValueFromCache(item)
            if res is None:
                return None
            argsList.append(res)
        return self.__func(*argsList)


class AlertManager:

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("default")
        self.__alertItemList = []

    def appendAlertItem(self, alertItem):
        self.logger.info("Register Alert {0}".format(alertItem.getName()))
        self.__alertItemList.append(alertItem)

    def remvoeAlertItem(self, alertItem):
        self.logger.info("Remove Alert {0}".format(alertItem.getName()))
        self.__alertItemList.remove(alertItem)

    def update(self):
        count = 0
        ret = {}
        for item in self.__alertItemList:
            res = item.test()
            if res is not None:
                count += 1
                self.logger.error("{0}, msg:{1}".format(item.getName(), res))
                ret[item.getName()] = res
        if count != 0:
            ret["timestamp"] = time.time()
            return count, ret
        else:
            return count, None
