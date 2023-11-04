from flask import Flask, request
from functools import wraps
import json

import custom_metric
import dump
import get_info
import os
import restart

from dump import dump_schema

# костыль
os.environ['API_KEY'] = "99388f74-a9e9-4461-8186-1cf6cd26deb2"
os.environ['PGHOSTNAME'] = "92.53.127.18"
os.environ['PGPORT'] = "5432"
os.environ['PGUSERNAME'] = "postgres"
os.environ['PGPASSWORD'] = "hCImjO&&k6N$"
os.environ['PGDATABASE'] = "postgres"
os.environ['PGBACKUPPATH'] = "./backup/"
os.environ['DBDOCKERNAME'] = 'full_db'
os.environ['DBDOCKERDBNAME'] = 'full_db'
os.environ['DBDOCKERLOCATION'] = '/var/lib/jenkins/workspace/backend/docker-compose.yml'
app = Flask(__name__)


def api_key_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        api_key = request.headers.get('X-Api-Key')
        if api_key != os.environ['API_KEY']:
            return 'Unauthorized', 401
        return f(**kwargs)

    return wrapped_view


# deprecated use execute() instead
@app.route('/restart_db')
@api_key_required
def restart_db():
    restart.restart_db()
    return 'OK', 200


# deprecated use execute() instead
@app.route('/restore_db')
@api_key_required
def restore_db():
    path = request.get_json()['file']
    dump.restore_schema(path)
    return 'OK', 200


# deprecated use execute() instead
@app.route('/dump_db')
@api_key_required
def dump_db():
    path = request.get_json()['file']
    dump_schema(path)
    return 'OK', 200


@app.route('/exec')
@api_key_required
def execute():
    command = request.args.get("command")
    parameter = request.args.get("parameter")
    if command == "backup":
        dump_schema(parameter)
        return 'OK', 200
    if command == "restore":
        dump.restore_schema(parameter)
        return 'OK', 200
    if command == "restart":
        restart.restart_db()
        return 'OK', 200
    if command == "connection":

        return 'OK', 200
    return 'Not found', 404


@app.route('/get_metrics')
@api_key_required
def get_metrics():
    result = get_info.get_info()
    json_data = json.dumps(result, default=float)
    return json_data


@app.route('/dumps')
@api_key_required
def get_dumps():
    result = dump.get_dumps()
    return json.dumps(result)


@app.route('/long_transactions')
@api_key_required
def get_current_longest_queries():
    result = custom_metric.get_current_long_transaction()
    return result


@app.route('/top_transactions')
@api_key_required
def get_longest_queries():
    result = custom_metric.get_longest_transaction()
    return result


if __name__ == '__main__':
    app.run()
