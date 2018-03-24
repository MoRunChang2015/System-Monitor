#!/usr/bin/python3

from core.api import alertApi

@alertApi("LOAD_ALERT", "LOAD5")
def loadAlert(load5):
    if load5 > 1.0:
        return "LOAD5 more than 1.0"
