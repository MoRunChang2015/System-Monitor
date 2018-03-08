#!/usr/bin/python3

from core.api import collectApi

@collectApi("MEM", "Memory info", 5)
def mem_info():
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = int(var) * 1024.0
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    return mem['MemUsed']
