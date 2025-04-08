from database.connection import get_db

def init_db():
    with open("database/schema.sql", "r") as f:
        sql = f.read()
    with get_db() as conn:
        conn.executescript(sql)
        conn.commit()