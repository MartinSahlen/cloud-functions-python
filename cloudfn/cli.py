import subprocess
import os
import sys
import argparse


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
        'pyinstaller ', file_name, '-y', '-n', 'func',
        '--clean', '--onedir',
        '--additional-hooks-dir', hooks_path(),
        '--hidden-import', 'htmlentitydefs',
        '--hidden-import', 'HTMLParser',
        '--hidden-import', 'Cookie',
    ]


def build_cmd(filename='main.py', production=True):
    if production:
        return build_for_production(filename)
    return buiod_for_local(filename)


def build_function(function_name, file_name='main.py', local=True):
    process = subprocess.Popen(
        ' '.join(build_for_production()),
        stdout=sys.stdout,
        stdin=sys.stdin,
        shell=True)
    output, error = process.communicate()


def main():
    parser = argparse.ArgumentParser(
        description='Build a GCP Cloud Function in python.'
        )
    parser.add_argument('function_name', type=str,
                        help='the name of your cloud function')
    parser.add_argument('-p', '--production', action='store_true',
                        help='Build the function for a production environment')

    args = parser.parse_args()
    build_function(args.function_name, args.production)
