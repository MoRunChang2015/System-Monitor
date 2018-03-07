# -*- coding: utf-8 -*-

from event import input_event, output_event, input_map, output_map
import select

timeout = 5;

def run():
    while True:
        readable, writeable, exceptional = select.select(input_event, output_event, input_event + output_event,
                                                         timeout)
        if not (readable or writeable or exceptional):
            continue

        for s in readable:
            if s in input_event:
                if s in input_map:
                    event = input_map[s].pop(0)
                    event.done()
                    if len(input_map[s]) == 0:
                        del input_map[s]
                if s not in input_map:
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
                if s not in input_map:
                    input_event.remove(s)
            if s in output_event:
                if s in output_map:
                    event = output_map[s].pop(0)
                    event.error()
                    if len(output_map[s]) == 0:
                        del output_map[s]
                if s not in output_map:
                    output_event.remove(s)
