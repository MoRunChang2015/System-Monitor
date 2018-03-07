# -*- coding: utf-8 -*-

from utils.event import InputEvent, OutputEvent


class ReceiveEvent(InputEvent):

    def __init__(self, sock):
        super(ReceiveEvent, self).__init__(sock)
        self.socket = sock

    def _done(self):
        try:
            data = self.socket.recv(1024)
        except Exception:
            data = ""
        self.callback(data)

    def _error(self):
        self.callback(None)


class SendEvent(OutputEvent):

    def __init__(self, sock, data):
        super(SendEvent, self).__init__(sock)
        self.socket = sock
        self.data = data

    def _done(self):
        self.socket.send(self.data)
        self.callback()

    def _error(self):
        self.callback(None)


class AcceptEvent(InputEvent):

    def __init__(self, sock):
        super(AcceptEvent, self).__init__(sock)
        self.socket = sock

    def _done(self):
        connection, address = self.socket.accept()
        self.callback(connection)

    def _error(self):
        self.callback(None)
