import os
import time
from datetime import date, datetime

import psycopg2 as psycopg2

from bd_utils import get_connection

sql_item = {
    'Alive': "select 1;",  # monitor survival
    'Cache hit ratio': "SELECT sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio FROM pg_statio_user_tables;",
    'Active_connections': "select count (*) from pg_stat_activity where state = 'active';",
    'Server_connections': "select count (*) from pg_stat_activity where backend_type = 'client backend'",
    'Idle_connections': "select count (*) from pg_stat_activity where state = 'idle'",
    'Idle_tx_connections': "select count (*) from pg_stat_activity where state = 'idle in transaction'",
    'Locks_waiting': "select count (*) from pg_stat_activity where backend_type = 'client backend' and wait_event_type like '% Lock%'",
    'Server_maxcon': "select setting :: int from pg_settings where name = 'max_connections'",
    'Tx_commited': "select sum (xact_commit) from pg_stat_database",
    'Tx_rollbacked': "select sum (xact_rollback) from pg_stat_database",
    'scan_full_tables': "select sum(tup_returned) from pg_stat_database",
    'scan_index_rows': "select sum(tup_fetched) from pg_stat_database",
    'tup_inserted': "select sum(tup_inserted) from pg_stat_database",
    'tup_updated': "select sum(tup_updated) from pg_stat_database",
    'tup_deleted': "select sum(tup_deleted) from pg_stat_database",
    'Deadlocks': "select sum (deadlocks) from pg_stat_database",
    'Rep_write_delay': "select pg_size_pretty (pg_wal_lsn_diff (pg_current_wal_lsn (), write_lsn)) from pg_stat_replication",
    'Rep_flush_delay': "select pg_size_pretty (pg_wal_lsn_diff (pg_current_wal_lsn (), flush_lsn)) from pg_stat_replication",
    'Rep_replay_delay': "select pg_size_pretty (pg_wal_lsn_diff (pg_current_wal_lsn (), replay_lsn)) from pg_stat_replication",
    'Idle_transaction_5': "select count (*) from pg_stat_activity where state = 'idle in transaction' and now () - state_change> interval '5 second'",
    'Long_query_5': "select count (*) from pg_stat_activity where state = 'active' and now () - query_start> interval '5 second'",
    'Long_transaction_5': "select count (*) from pg_stat_activity where now () - xact_start> interval '5 second'",
    'long_lock_waiting_5': "select count(*) from pg_stat_activity where wait_event_type is not null and now()-state_change > interval '5 second'",
    # 'pg_stat_activity': "SELECT * FROM pg_stat_activity"
}


def get_item(item_key):
    query = sql_item[item_key]
    connection = get_connection()
    cursor = None
    try:
        result = {}
        now = int(time.time())
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        result['timestamp'] = now
        result['name'] = item_key
        result['value'] = float(rows[0][0])
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


def get_info():
    result = []
    for key, value in sql_item.items():
        item = get_item(key)
        if item is not None:
            result.append(get_item(key))
    return result
