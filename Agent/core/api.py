#!/usr/bin/python3


from .attribute import Attribute
from .alert import AlertItem
from .globalVar import attributeManager, alertManager

def collectApi(name, description, interval=5):
    def wraps(func):
        attr = Attribute(name, description, interval, func)
        attributeManager.appendAttribute(attr)
        return func
    return wraps

def alertApi(name, *args):
    def wraps(func):
        item = AlertItem(name, args, func)
        alertManager.append(item)
        return func
    return wraps
