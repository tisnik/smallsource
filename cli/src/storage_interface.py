"""Interface to the main storage (sqlite3 in this version)."""

import sqlite3
from sqlite3 import Error


def create_connection(db_filename):
    """Create a database connection to the SQLite database specified by the db_filename."""
    assert db_filename is not None

    try:
        conn = sqlite3.connect(db_filename)
        return conn
    except Error as e:
        print(str(e))
    return None


def select_all_ecosystems(connection):
    """Select and return list of all ecosystems."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ecosystem")
    rows = cursor.fetchall()

    return rows
