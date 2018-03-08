#!/usr/bin/python3

import logging
import threading
import socket
import time

class Reporter:

    def __init__(self, hostname, urls):
        super().__init__()
        self.logger = logging.getLogger("default")
        self.__hostname = hostname
        self.__mutex = threading.Lock()
        self.__messageList = []
        self.__urls = urls
        t = threading.Thread(target=self.report)
        t.start()

    def getHostname(self):
        return self.__hostname

    def setHostname(self, hostname):
        self.__hostname = hostname

    def getUrlList(self):
        return self.__urls

    def setUrlList(self, urls):
        self.__urls = urls

    def appendMessage(self, message):
        with self.__mutex:
            self.__messageList.append(message)

    def popAllMessage(self):
        with self.__mutex:
            ret = "".join(self.__messageList)
            self.__messageList = []
            return ret

    def connectToCollector(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        isConnect = False
        for ip, port in self.__urls:
            try:
                s.connect((ip, port))
            except:
                continue
            isConnect = True
            break
        s.settimeout(None)
        if isConnect:
            return s
        else:
            return None

    def report(self):
        self.logger.info("#Reporter: Reporter Start...")
        s = self.connectToCollector()
        if s is None:
            self.logger.warn("#Reporter: Can't not connect to collector")
        else:
            self.logger.info("#Reporter: Connect to {0}".format(s.getpeername()))
        while True:
            time.sleep(1)
            message = self.popAllMessage()
            if message == "":
                continue
            message = message.encode("utf-8")
            tryTime = 0
            while tryTime <= len(self.__urls):
                try:
                    s.sendall(message)
                except Exception as e:
                    print(e)
                    s = self.connectToCollector()
                    if s is None:
                        self.logger.warn("#Reporter: Can't not connect to collector")
                        break
                    self.logger.info("#Reporter: Connect to {0}".format(s.getpeername()))
                    tryTime += 1
                    continue
                self.logger.info("#Reporter: Send data(len={0}) to {1}".format(len(message), s.getpeername()))
                break
