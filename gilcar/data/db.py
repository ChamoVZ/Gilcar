import oracledb
from contextlib import contextmanager
from gilcar.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SERVICE

@contextmanager
def get_connection():
    conn = None
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            service_name=DB_SERVICE
        )
        yield conn
    finally:
        if conn:
            conn.close()
