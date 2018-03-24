#!/usr/bin/python3

from core.api import collectApi

@collectApi("LOAD5", "Cpu Avg Load 5", 5)
def cpu_load_5():
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    return float(con[1])

@collectApi("LOAD1", "Cpu Avg Load 1", 1)
def cpu_load_1():
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    return float(con[0])

@collectApi("LOAD15", "Cpu Avg Load 15", 15)
def cpu_load_15():
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    return float(con[2])
