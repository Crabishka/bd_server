from flask import Flask, request
from functools import wraps
import json

import dump
import get_info
import os
import restart

from dump import dump_schema

# костыль
os.environ['API_KEY'] = "bc6eb18d-f242-4cb8-ad04-352fbb879616"
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


@app.route('/restart_db')
@api_key_required
def restart_db():
    restart.restart_db()
    return 'OK', 200


@app.route('/restore_db')
@api_key_required
def restore_db():
    path = request.get_json()['file']
    dump.restore_schema(path)
    return 'OK', 200


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
    return 'Nor found', 404


@app.route('/get_metrics')
@api_key_required
def get_metrics():
    result = get_info.get_info()
    json_data = json.dumps(result, default=float)
    return json_data


@app.route('/dumps')
@api_key_required
def get_dumps():
    return dump.get_dumps()


if __name__ == '__main__':
    app.run()
