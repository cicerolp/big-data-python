import abc


class InMemoryDB(metaclass=abc.ABCMeta):
    """Interface to In-Memory Database Engines.
    """
    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create_schema(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def insert(self, item: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def insert_multiple(self, items: list):
        raise NotImplementedError
