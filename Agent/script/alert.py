#!/usr/bin/python3

from core.api import alertApi

@alertApi("LOAD_ALERT", "LOAD5")
def loadAlert(load5):
    return "Warning"
