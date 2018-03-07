# -*- coding: utf-8 -*-

from event import input_event, output_event, input_map, output_map
import select
import global_var
import time

tick = None
shutdown = None


def run():
    last_tick_time = float(time.time())
    while not global_var.g_isStop:
        readable, writeable, exceptional = select.select(input_event, output_event, input_event + output_event,
                                                         global_var.g_timeout)
        if tick is not None and abs(float(time.time()) - last_tick_time) >= global_var.g_timeout:
            tick()
            last_tick_time = time.time()
        if not (readable or writeable or exceptional):
            continue

        for s in readable:
            if s in input_event:
                if s in input_map:
                    event = input_map[s].pop(0)
                    event.done()
                    if len(input_map[s]) == 0:
                        del input_map[s]
                if s is not global_var.g_command_socket and s not in input_map:
                    input_event.remove(s)

        for s in writeable:
            if s in output_event:
                if s in output_map:
                    event = output_map[s].pop(0)
                    event.done()
                    if len(output_map[s]) == 0:
                        del output_map[s]
                if s not in output_map:
                    output_event.remove(s)

        for s in exceptional:
            if s in input_event:
                if s in input_map:
                    event = input_map[s].pop(0)
                    event.error()
                    if len(input_map[s]) == 0:
                        del input_map[s]
                if s is not global_var.g_command_socket and s not in input_map:
                    input_event.remove(s)
            if s in output_event:
                if s in output_map:
                    event = output_map[s].pop(0)
                    event.error()
                    if len(output_map[s]) == 0:
                        del output_map[s]
                if s not in output_map:
                    output_event.remove(s)
    if shutdown is not None:
        shutdown()