from flask import Flask, request
from functools import wraps
import get_info
import os

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
def get_metrics():  # put application's code here
    return 'hello'


@app.route('/restore_db')
@api_key_required
def get_metrics():  # put application's code here
    return 'hello'


@app.route('/dump_db')
@api_key_required
def get_metrics():  # put application's code here
    return 'hello'


@app.route('/get_metrics')
@api_key_required
def get_metrics():  # put application's code here
    result = get_info.get_info()
    return result


if __name__ == '__main__':
    app.run()
