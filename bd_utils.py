import os

import psycopg2


def terminate_process(pid):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        result = cursor.execute(f'SELECT pg_terminate_backend({pid})')
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


def get_connection():
    return psycopg2.connect(
        user=os.environ['PGUSERNAME'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOSTNAME'],
        port=os.environ['PGPORT'],
        database=os.environ['PGDATABASE']
    )
