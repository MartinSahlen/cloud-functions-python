[![PyPI version](https://badge.fury.io/py/pycloudfn.svg)](https://badge.fury.io/py/pycloudfn)

# cloud-functions-python
`py-cloud-fn` is a CLI tool that allows you to write and deploy [Google cloud functions](https://cloud.google.com/functions/) in pure python. No javascript allowed!
The goal of this library is to be able to let developers write light weight functions
in idiomatic python without needing to worry about node.js. It works OOTB with [pip](https://pypi.python.org/pypi),
just include a file named `requirements.txt` that is structured like this:

```
pycloudfn==0.1.115
jsonpickle==0.9.4
```

as you normally would when building any python application. When building (for production), the library
will pick up this file and make sure to install the dependencies. It will do so while caching all dependencies
in a [virtual environment](https://virtualenv.pypa.io/en/stable/), to speed up subsequent builds.

Run `pip install pycloudfn` to get it.
You need to have [Google cloud SDK](https://cloud.google.com/sdk/downloads) installed, as well as
the [Cloud functions emulator](https://github.com/GoogleCloudPlatform/cloud-functions-emulator/).
Currently the emulator does not seem to work though :(

You also need **Docker** installed and running as well as the **gcloud** CLI. Docker is needed to build for the production environment, regardless of you local development environment. It's only tested on my mac and currently only for python 2.7. It should be not too difficult to make it work with python 3, pull requests welcome!

Currently, only `http`, `pubsub` and `bucket` events are supported.



# Usage

## CLI

```
usage: py-cloud-fn [-h] [-p] [-f FILE_NAME] [--python_version {2,3}]
                   function_name {http,pubsub,bucket}

Build a GCP Cloud Function in python.

positional arguments:
  function_name         the name of your cloud function
  {http,pubsub,bucket}  the trigger type of your cloud function

optional arguments:
  -h, --help            show this help message and exit
  -p, --production      Build function for production environment
  -f FILE_NAME, --file_name FILE_NAME
                        The file name of the file you wish to build
  --python_version {2,3}
                        The python version you are targeting, only applies
                        when building for production
```

Usage is meant to be pretty idiomatic:

Run `py-cloud-fn <function_name> <trigger_type>` to build your finished function.
Run with `-h` to get some guidance on options. The library will assume that you have a file named `main.py` if not specified.

The library will create a `cloudfn` folder wherever it is used, which can safely be put in `.gitignore`. It contains build files and cache for python packages.

## Dependencies
This library works with [pip](https://pypi.python.org/pypi) OOTB. Just add your `requirements.txt` file in the root
of the repo and you are golden. It obviously needs `pycloudfn` to be present.

### Handling a http request

look at the [Request](https://github.com/MartinSahlen/cloud-functions-python/blob/master/cloudfn/http.py)
object for the structure

```python
from cloudfn.http import handle_http_event, Response


def handle_http(req):
      return Response(
        status_code=200,
        body={'key': 2},
        headers={'content-type': 'application/json'},
    )


handle_http_event(handle_http)

```

If you don't return anything, or return something different than a `cloudfn.http.Response` object, the function will return a `200 OK` with an empty body. The body can be either a string, list or dictionary, other values will be forced to a string.

### Handling http with Flask

[Flask](http://flask.pocoo.org/) is a great framework for building microservices.
The library supports flask OOTB. If you need to have some routing / parsing and
verification logic in place, flask might be a good fit! Have a look at the
[example](https://github.com/MartinSahlen/cloud-functions-python/tree/master/examples/flask)
to see how easy it is!

```python
from cloudfn.flask_handler import handle_http_event
from flask import Flask, request
from flask.json import jsonify
app = Flask(__name__)


@app.route('/',  methods=['POST', 'GET'])
def hello():
    return jsonify(message='Hello world!', json=request.get_json()), 201


@app.route('/lol')
def helloLol():
    return 'Hello lol!'


handle_http_event(app)
```

### Handling http with Django

[Django](https://www.djangoproject.com/) is a great framework for building microservices.
The library supports django OOTB. Assuming you have setup your django application in a
normal fashion, this should be what you need. You need to setup a pretty minimal django
application (no database etc) to get it working. It might be a little overkill to squeeze
django into a cloud function, but there are some pretty nice features for doing request
verification and routing in django using for intance
[django rest framework](http://www.django-rest-framework.org/).

See the [example](https://github.com/MartinSahlen/cloud-functions-python/tree/master/examples/django)
for how you can handle a http request using django.

```python
from cloudfn.django_handler import handle_http_event
from mysite.wsgi import application


handle_http_event(application)
```

### Handling a bucket event

look at the [Object](https://github.com/MartinSahlen/cloud-functions-python/blob/master/cloudfn/storage.py)
for the structure, it follows the convention in the [Storage API](https://cloud.google.com/storage/docs/json_api/v1/objects)

```python
from cloudfn.storage import handle_bucket_event
import jsonpickle


def bucket_handler(obj):
    print jsonpickle.encode(obj)


handle_bucket_event(bucket_handler)
```

### Handling a pubsub message

look at the [Message](https://github.com/MartinSahlen/cloud-functions-python/blob/master/cloudfn/pubsub.py)
for the structure, it follows the convention in the [Pubsub API](https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage)

```python
from cloudfn.pubsub import handle_pubsub_event
import jsonpickle


def pubsub_handler(message):
    print jsonpickle.encode(message)


handle_pubsub_event(pubsub_handler)
```

## Deploying a function
I have previously built [go-cloud-fn](https://github.com/MartinSahlen/go-cloud-fn/), in which there is a complete CLI available for you to deploy a function. I did not want to go there now, but rather be concerned about `building` the function and be super light weight. Deploying a function can be done like this:

### HTTP

```sh
py-cloud-fn my-function http --production && \
cd cloudfn/target && gcloud beta functions deploy my-function \
--trigger-http --stage-bucket <bucket> && cd ../..
```

### Storage

```sh
py-cloud-fn  my-bucket-function bucket -p && cd cloudfn/target && \
gcloud beta functions deploy my-bucket-function --trigger-bucket \
<trigger-bucket> --stage-bucket <stage-bucket> && cd ../..
```

### Pubsub

```sh
py-cloud-fn my-topic-function bucket -p && cd cloudfn/target && \
gcloud beta functions deploy my-topic-function --trigger-topic <topic> \
--stage-bucket <bucket> && cd ../..
```

### Adding support for packages that doesnt work

- Look at the build output for what might be wrong.
- Look for what modules might be missing.
- Add a line-delimited file for **hidden imports** and a folder called **cloudfn-hooks**
in the root of your repo, see more at [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/hooks.html) for how it works. Check out [this](https://github.com/MartinSahlen/cloud-functions-python/blob/master/cloudfn/hooks)
for how to add hooks.

## License

Copyright © 2017 Martin Sahlen

Distributed under the MIT License
