import logging

from in_memory_db import InMemoryDB
from pydblite.pydblite import Base


logging.basicConfig(level=logging.DEBUG,
                    format="(%(threadName)s) %(message)s",)
logger = logging.getLogger("InMemoryDBLite")


class InMemoryDBLite(InMemoryDB):
    """Class that implements all steps from Dextra's programming challange.

    Uses pydblite in-memory engine.
    """

    def __init__(self, name: str):
        logger.debug('Initializing DB.')
        self.connected = False
        self.name = name
        self.db = Base(name, save_to_file=False)

    def connect(self):
        logger.debug(f'Connecting to [{self.name}].')
        # When using pydblite in-memory engine, is unnecessary
        # connect to a db, so we just set the flag to true
        self.connected = True

    def disconnect(self):
        logger.debug(f'Disconnecting from [{self.name}].')
        if not self.connected:
            raise Exception('Not connected to db.')
        else:
            # When using pydblite in-memory engine, is unnecessary
            # disconnect from a db, so we just set the flag to false
            self.connected = False

    def create_schema(self, *args):
        logger.debug(f'Crating schema into [{self.name}].')
        if not self.connected:
            raise Exception('Not connected to db.')
        else:
            r = self.db.create(*args, mode='override')
            self.db.commit()
            return r

    def insert(self, item: dict):
        logger.debug(f'Inserting item into [{self.name}].')
        if not self.connected:
            raise Exception('Not connected to db.')
        else:
            r = self.db.insert(**item)
            self.db.commit()
            return r

    def insert_multiple(self, items: list):
        logger.debug(f'Inserting multiple items into [{self.name}].')
        if not self.connected:
            raise Exception('Not connected to db.')
        else:
            for item in items:
                r = self.db.insert(**item)
            self.db.commit()
            return r
