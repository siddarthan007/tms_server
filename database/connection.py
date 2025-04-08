import sqlite3
from contextlib import contextmanager
from config import Config

@contextmanager
def get_db():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()