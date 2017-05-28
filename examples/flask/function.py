from cloudfn.flask_handler import handle_http_event
from flask import Flask, request
from flask.json import jsonify
from google.cloud import bigquery


app = Flask('the-function')
client = bigquery.Client()


@app.route('/',  methods=['POST', 'GET'])
def hello():
    print request.args
    return jsonify(message='Hello world!', json=request.get_json()), 201


@app.route('/lol')
def helloLol():
    return 'Hello lol!'


@app.route('/bigquery-datasets',  methods=['POST', 'GET'])
def bigquery():
    datasets = []
    for dataset in client.list_datasets():
        datasets.append(dataset.name)
    return jsonify(message='Hello world!', datasets={
        'datasets': datasets
    }), 201


handle_http_event(app)
