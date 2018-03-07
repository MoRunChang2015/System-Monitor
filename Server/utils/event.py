# -*- coding: utf-8 -*-

input_event = []
output_event = []
input_map = {}
output_map = {}


class Event(object):

    def __init__(self):
        super(Event, self).__init__()
        self.callback = lambda: None

    def set_callback(self, callback):
        self.callback = callback

    def done(self):
        self._done()

    def error(self):
        self._error()


class InputEvent(Event):

    def __init__(self, sock):
        super(InputEvent, self).__init__()
        if sock not in input_event:
            input_event.append(sock)
        if sock not in input_map:
            input_map[sock] = []
        input_map[sock].append(self)


class OutputEvent(Event):

    def __init__(self, sock):
        super(OutputEvent, self).__init__()
        if sock not in output_event:
            output_event.append(sock)
        if sock not in output_map:
            output_map[sock] = []
        output_map[sock].append(self)
