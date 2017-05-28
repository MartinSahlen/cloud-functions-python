from cloudfn.flask_handler import handle_http_event
from flask import Flask, request
from flask.json import jsonify
app = Flask(__name__)


@app.route('/',  methods=['POST', 'GET'])
def hello():
    print request.args
    return jsonify(message='Hello world!', json=request.get_json()), 201


@app.route('/lol')
def helloLol():
    return 'Hello lol!'


handle_http_event(app)
