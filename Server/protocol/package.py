# -*- coding: UTF-8 -*-

import json


class PackageFactory:

    def __init__(self):
        super().__init__()
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
                yield res
                is_end = False
                self.buffer = self.buffer[index:]

