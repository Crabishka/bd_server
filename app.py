from flask import Flask, request
from functools import wraps

import get_info
import os

from dump import dump_schema

app = Flask(__name__)


# host = os.environ['PGHOSTNAME']
# port = os.environ['PGPORT']
# username = os.environ['PGUSERNAME']
# password = os.environ['PGPASSWORD']
# database = os.environ['PGDATABASE']
# path_to_backup = os.environ['PGBACKUPPATH']

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
    return result


if __name__ == '__main__':
    app.run(host='92.53.127.18', port=5000)
