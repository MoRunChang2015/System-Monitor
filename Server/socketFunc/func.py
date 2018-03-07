# -*- coding: utf-8 -*-

from socketEvent import *
from utils.future import Future


def accept(sock):
    future = Future()
    event = AcceptEvent(sock)
    event.set_callback(lambda connect: future.done(connect))
    return future


def send(sock, data):
    future = Future()
    event = SendEvent(sock, data)
    event.set_callback(lambda: future.done())
    return future


def recv(sock):
    future = Future()
    event = ReceiveEvent(sock)
    event.set_callback(lambda data: future.done(data))
    return future
