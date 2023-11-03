from flask import Flask, request
from functools import wraps
import json
import get_info
import os

from dump import dump_schema

os.environ['API_KEY'] = "1234567890"
os.environ['PGHOSTNAME'] = "92.53.127.18"
os.environ['PGPORT'] = "5432"
os.environ['PGUSERNAME'] = "postgres"
os.environ['PGPASSWORD'] = "hCImjO&&k6N$"
os.environ['PGDATABASE'] = "postgres"
os.environ['PGBACKUPPATH'] = "/backup"
os.environ['DBDOCKERNAME'] = ''
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
    return 'hello'


@app.route('/restore_db')
@api_key_required
def restore_db():
    return 'hello'


@app.route('/dump_db')
@api_key_required
def dump_db():
    path = request.get_json()['file']
    dump_schema(path)


@app.route('/get_metrics')
@api_key_required
def get_metrics():
    result = get_info.get_info()
    json_data = json.dumps(result, default=str)
    return json_data


if __name__ == '__main__':
    # костыль
    app.run()
