import psycopg2
from psycopg2.extras import RealDictCursor

class DB:
    def __init__(self, host, port, dbname, user, password):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password
        }

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def fetch_query(self, query, params=None):
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params or ())
                return cur.fetchall()

    def execute_query(self, query, params=None):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                conn.commit()
