# -*- coding: UTF-8 -*-

import json
import time


class PackageFactory(object):

    def __init__(self):
        self.buffer = ""

    @staticmethod
    def get_instance():
        """
        get factory instance
        :return: factory instance
        """
        return iter(PackageFactory())

    @staticmethod
    def push(factory, value):
        """
        push a data to factory
        :param factory: factory
        :param value: data
        :return: a package , None for no new package
        """
        next(factory)
        return factory.send(value)

    @staticmethod
    def pop(factory):
        """
        get a new package from factory
        :param factory: factory
        :return: a package, None for no new package
        """
        return next(factory)

    def __iter__(self):
        is_end = True
        decoder = json.JSONDecoder()
        while True:
            if is_end:
                new_package = yield
                self.buffer += new_package
            is_end = True
            package = None
            try:
                res, index = decoder.raw_decode(self.buffer)
            except ValueError:
                yield package
                continue
            else:
                package = Package()
                package.load(res)
                yield package
                is_end = False
                self.buffer = self.buffer[index:]


class Package(object):

    def __init__(self, package_type=None, time_stamp=None, src=None, dest=None, data=None):
        super(Package, self).__init__()
        self.__data = {}
        self.package_type = package_type
        self.time = time_stamp if time_stamp is not None else float(time.time())
        self.src = src
        self.dest = dest
        self.data = data

    def pack(self):
        return json.dumps(self.__data)

    def load(self, value):
        self.__data = value

    @property
    def package_type(self):
        return self.__data['package_type'] if 'package_type' in self.__data else None

    @package_type.setter
    def package_type(self, value):
        if value is not None:
            self.__data['package_type'] = str(value)

    @property
    def time(self):
        return self.__data['time'] if 'time' in self.__data else None

    @time.setter
    def time(self, value):
        if value is not None:
            self.__data['time'] = float(value)

    @property
    def src(self):
        return self.__data['src'] if 'src' in self.__data else None

    @src.setter
    def src(self, value):
        if value is not None:
            self.__data['src'] = str(value)

    @property
    def dest(self):
        return self.__data['dest'] if 'dest' in self.__data else None

    @dest.setter
    def dest(self, value):
        if value is not None:
            self.__data['dest'] = str(value)

    @property
    def data(self):
        return self.__data['data'] if 'data' in self.__data else None

    @data.setter
    def data(self, value):
        if value is not None:
            self.__data['data'] = str(value)
