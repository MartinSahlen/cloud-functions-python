import subprocess
import os
import sys
import argparse
from jinja2 import Template

'''
Need to fail on non docker or gcloud or functions emulator
not existing. Give informative message.
Customize docker container name?

py-cloud-fn build <function_name> --production | -p (default --emulator | e) \
&& gcloud beta functions deploy <function_name> ...

super-light. Lighter than go-cloud-fn which is very hard wrapping
target folder ignore.
'''


def repo_root():
    return os.path.dirname(__file__) + '/../'


def hooks_path():
    return repo_root() + 'hooks'


def image_name():
    return 'pycloudfn-builder'


def docker_path():
    return repo_root() + 'docker/'


def output_name():
    return 'func'


def build_for_production(file_name='main.py'):
    return [
        'docker', 'build', '-f', docker_path() + 'Dockerfile',
        '-t', image_name(), docker_path(), '&&', 'docker', 'run',
        '--rm', '-ti', '-v', '$(pwd):/app', '-v',
        hooks_path()+':'+hooks_path(), image_name(), '/bin/sh', '-c',
        '\'cd app && (test -d pip-cache || virtualenv pip-cache) && ',
        '. pip-cache/bin/activate && '
        'test -f requirements.txt && pip install -r requirements.txt || echo '
        'No requirements.txt present  && ' +
        ' '.join(build_for_local(file_name)) + '\'',
    ]


def build_for_local(file_name='main.py'):
    return [
        'pyinstaller ', file_name, '-y', '-n', output_name(),
        '--clean', '--onedir',
        '--additional-hooks-dir', hooks_path(),
        '--hidden-import', 'htmlentitydefs',
        '--hidden-import', 'HTMLParser',
        '--hidden-import', 'Cookie',
    ]


def build_cmd(file_name='main.py', production=False):
    if production:
        return build_for_production(file_name=file_name)
    return build_for_local(file_name=file_name)


def build_function(function_name, file_name='main.py', trigger_type='http',
                   production=False):
    exit_code = subprocess.call(
        ' '.join(build_cmd(file_name=file_name, production=production)),
        stdout=sys.stdout,
        stdin=sys.stdin,
        shell=True)
    if exit_code == 0:
        build_javascript(function_name, trigger_type=trigger_type)
    sys.exit(exit_code)


def build_javascript(function_name, trigger_type='http'):
    js = open(repo_root() + 'template/index.js').read()
    print js
    t = Template(js)
    rendered_js = t.render(config={
            'output_name': output_name(),
            'function_name': function_name,
            'trigger_http': trigger_type == 'http',
        }
    )
    open('index.js', 'w').write(rendered_js)


def main():
    parser = argparse.ArgumentParser(
        description='Build a GCP Cloud Function in python.'
        )
    parser.add_argument('function_name', type=str,
                        help='the name of your cloud function')
    parser.add_argument('trigger_type', type=str,
                        help='the trigger type of your cloud function',
                        choices=['http', 'pubsub', 'bucket'])
    parser.add_argument('-p', '--production', action='store_true',
                        help='Build function for production environment')

    args = parser.parse_args()
    build_function(args.function_name,
                   production=args.production,
                   trigger_type=args.trigger_type)
