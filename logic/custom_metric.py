import os
import time
from datetime import datetime, timedelta

import psycopg2

from bd_utils import get_connection


def get_current_long_transaction():
    result = get_custom_query(
        """
        select pid, query, datname, now() - query_start AS duration
        from pg_stat_activity
        where state = 'active'
        and now() - query_start > interval '5 second'
        ORDER BY now() - query_start DESC
        LIMIT 10;
        """,
        parse_fund=parse_curr_longest_transaction)
    return result


def get_longest_transaction():
    result = get_custom_query(
        "SELECT query, calls, total_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20",
        parse_fund=parse_longest_transaction)
    return result


def get_custom_query(query, parse_fund):
    connection = get_connection()
    cursor = connection.cursor()
    total = []
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        total = []
        for item in result:
            total.append(parse_fund(item))
        return total
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
    return total


def parse_curr_longest_transaction(item):
    longest_info = {
        "pid": item['pid'],
        "query": item['query'][:100],
        "datname": item['datname'],
        "duration": item['duration'].total_seconds(),
    }
    return longest_info


def parse_longest_transaction(item):
    longest_info = {
        "count": item['calls'],
        "query": item['query'][:100],
        "duration_sum": int(item['total_exec_time']),
    }
    return longest_info
