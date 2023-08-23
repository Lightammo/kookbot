from abc import ABCMeta, abstractmethod


class Driver(metaclass=ABCMeta):
    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def setup(self):
        ...

    @abstractmethod
    def teardown(self):
        ...
