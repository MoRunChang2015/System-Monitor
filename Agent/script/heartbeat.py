#!/usr/bin/python3

from core.api import collectApi

@collectApi("BEAT", "System Heart Beat", 5)
def heart_beat():
    return "Beat"
