import pytest
import numpy as np


@pytest.fixture
def db_connection():
    from in_memory_db import InMemoryDBLite
    db = InMemoryDBLite('test_db')
    db.connect()
    return db


def test_connection(db_connection):
    assert(db_connection.connected)


def test_disconection(db_connection):
    db_connection.disconnect()
    assert(not db_connection.connected)

    with pytest.raises(Exception):
        db_connection.disconnect()


def test_create_schema(db_connection):
    assert(db_connection.create_schema('key', 'value') != None)


def test_insertion(db_connection):
    db_connection.create_schema('key', 'value')
    db_connection.insert({'key': 'A', 'value': 'B'})

    assert(len(db_connection.db()) == 1)


def test_multiple_insertion(db_connection):
    db_connection.create_schema('key', 'value')
    db_connection.insert_multiple([
        {'key': 'A', 'value': 'B'},
        {'key': 'C', 'value': 'D'}
    ])

    assert(len(db_connection.db()) == 2)