from flask import Flask, request
from functools import wraps
import json
import os
from logic import restart, get_info, custom_metric, bd_utils, dump
from logic.dump import dump_schema, get_last_dumps

# костыль
os.environ['API_KEY'] = "a768b1d2-0929-469f-bce9-ee6e2c5e6f77"
# жесткий костыль
api_key_storage = [
    "a768b1d2-0929-469f-bce9-ee6e2c5e6f77", "447de72-1373-4753-b395-d38878416fdf",
    "cc2d93f7-4596-43a9-b95d-a3ba59eae766", "a768b1d2-0929-469f-bce9-ee6e2c5e6f77",
    "c023957f-2a20-4d2c-b259-ec1fa405c17b", "bf0237dd-f108-4f55-ba29-c781a831fd6b",
    "87a63eeb-6485-4b77-a6dc-bfb1e599bee7", "8d353a28-03d9-43e5-a036-e6c099f53b23",
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
        if parameter is None:
            parameter = get_last_dumps()['name']
        dump_schema(parameter)
        return 'OK', 200
    if command == "restore":
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
    return json.dumps(result)


@app.route('/top_transactions')
@api_key_required
def get_longest_queries():
    result = custom_metric.get_longest_transaction()
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
