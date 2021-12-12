import os
import psycopg2
import psycopg2.extras
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET_NAME = "altair-janga"

GCS_PRIMARY_FOLDER_NAME = "data"

GCS_BACKUP_FOLDER_NAME = "backup"

POSTGRES = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME")
}

class _DB:
    def __init__(self):
        self._connect()

    def _connect(self):
        self.conn = psycopg2.connect(**POSTGRES)
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        self.conn.autocommit = True


_db = _DB()


ES_URI = f"https://elastic:{os.getenv('ES_PASSWORD')}@{os.getenv('ES_URI')}"

es = Elasticsearch([ES_URI])
