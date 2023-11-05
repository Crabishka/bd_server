from flask import Flask, request, Response, jsonify
from functools import wraps
import json
import os
from logic import restart, get_info, custom_metric, bd_utils, dump
from logic.dump import dump_schema, get_last_dumps

# костыль
os.environ['API_KEY'] = "a768b1d2-0929-469f-bce9-ee6e2c5e6f77"
# жесткий костыль
api_key_storage = [
    "4385d4c5-7e68-4732-9f0b-7875b03c5581", "99388f74-a9e9-4461-8186-1cf6cd26deb2",
    "005fabb3-8250-48a1-bee4-4eb241fe762d", "dbc3283c-aa39-4c6c-b964-f77b3fc177b4",
    "2bfeb30d-1ff0-4eee-95a3-5c3c274ef2da", "d28da03e-7f4d-4938-958b-d728864aebb0"
]
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
        if api_key not in api_key_storage:
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
        if parameter is None:
            parameter = get_last_dumps()['name']
        dump.restore_schema(parameter)
        return 'OK', 200
    if command == "restart":
        restart.restart_db()
        return 'OK', 200
    if command == "connection":
        bd_utils.terminate_process(parameter)
        return 'OK', 200
    return 'Not found', 404


@app.route('/get_metrics')
@api_key_required
def get_metrics():
    result = get_info.get_info()
    result = json.dumps(result, default=float)
    return Response(
        response=result,
        status=200,
        content_type='application/json'
    )


@app.route('/dumps')
@api_key_required
def get_dumps():
    result = dump.get_dumps()
    return jsonify(result)


@app.route('/long_transactions')
@api_key_required
def get_current_longest_queries():
    result = custom_metric.get_current_long_transaction()
    return jsonify(result)


@app.route('/top_transactions')
@api_key_required
def get_longest_queries():
    result = custom_metric.get_longest_transaction()
    return jsonify(result)


if __name__ == '__main__':
    app.run()
