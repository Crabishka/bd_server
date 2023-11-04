import os

import psycopg2


def get_connection():
    connection = psycopg2.connect(
        user=os.environ['PGUSERNAME'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOSTNAME'],
        port=os.environ['PGPORT'],
        database=os.environ['PGDATABASE']
    )
