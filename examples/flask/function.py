from cloudfn.flask_handler import handle_http_event
from cloudfn.google_account import get_credentials
from flask import Flask, request
from flask.json import jsonify
from google.cloud import bigquery

app = Flask('the-function')
biquery_client = bigquery.Client(credentials=get_credentials())


@app.route('/',  methods=['POST', 'GET'])
def hello():
    print request.headers
    return jsonify(message='Hello world!', json=request.get_json()), 201


@app.route('/lol')
def helloLol():
    return 'Hello lol!'


@app.route('/bigquery-datasets',  methods=['POST', 'GET'])
def bigquery():
    datasets = []
    for dataset in biquery_client.list_datasets():
        datasets.append(dataset.name)
    return jsonify(message='Hello world!', datasets={
        'datasets': datasets
    }), 201


handle_http_event(app)
