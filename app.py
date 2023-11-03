from flask import Flask

import get_info

app = Flask(__name__)


@app.route('/get_metrics')
def get_metrics():  # put application's code here
    result = get_info.get_info()
    return result


if __name__ == '__main__':
    app.run()
