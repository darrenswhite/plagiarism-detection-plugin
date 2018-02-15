from flask import Flask

HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)


def start(debug=False):
    app.run(host=HOST, port=PORT, debug=debug)


@app.route('/')
def index():
    return 'Plagiarism Detection Server'
