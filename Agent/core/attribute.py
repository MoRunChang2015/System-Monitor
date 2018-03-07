#!/usr/bin/python3

import logging
import time


class Attribute:

    def __init__(self, name, description, interval, collectFunc):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__interval = interval
        self.__func = collectFunc;

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name;


    def getDescription(self):
        return self.__description

    def setDescription(self, description):
        self.__description = description

    def getInterval(self):
        return self.__interval

    def setInterval(self, interval):
        self.__interval = interval

    def update(self, time):
        if time % self.__interval == 0:
            return self.__func()
        else:
            return None


class AttributeManager:

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("default")
        self.__attrList = []
        self.__attrValueCache = {}

    def appendAttribute(self, attribute):
        self.__attrList.append(attribute)


    def removeAttribute(self, attribute):
        self.__attrList.remove(attribute)

    def update(self):
        count = 0
        ret = {}
        timeStamp = time.time();
        for attr in self.__attrList:
            res = attr.update(int(timeStamp))
            if res is not None:
                ret[attr.getName()] = res
                self.__attrValueCache[attr.getName()] = res
                count += 1
        ret["timestamp"] = timeStamp
        return count, ret

    def getAttrValueFromCache(self, name):
        if name in self.__attrValueCache:
            return self.__attrValueCache[name]
        else:
            return None
