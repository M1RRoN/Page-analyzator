import os
import psycopg2
from datetime import date
from typing import NamedTuple
from psycopg2.extras import NamedTupleCursor


class Database:
    def __init__(self):
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(self.DATABASE_URL)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.conn.close()


class Urls(Database):
    def get_urls_data(self) -> NamedTuple:
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'SELECT DISTINCT ON (urls.id)'
                'urls.id, urls.name, url_checks.status_code, '
                'MAX(url_checks.created_at) as last_check '
                'FROM urls LEFT JOIN url_checks '
                'ON urls.id = url_checks.url_id '
                'GROUP BY urls.id, url_checks.status_code '
                'ORDER BY urls.id DESC;'
            )
            urls_data = curs.fetchall()

        return urls_data

    def find_url_by_id(self, url_id: int) -> NamedTuple:
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT * FROM urls WHERE id=(%s)', (url_id,))
            return curs.fetchone()

    def find_url_by_name(self, url_name: str) -> NamedTuple:
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT * FROM urls WHERE name=(%s)', (url_name,))
            return curs.fetchone()

    def create_url_entry(self, url_name: str) -> int:
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'INSERT INTO urls (name, created_at) '
                'VALUES (%s, %s) RETURNING id',
                (url_name, date.today())
            )
            self.conn.commit()
            url_id = curs.fetchone().id

            return url_id
