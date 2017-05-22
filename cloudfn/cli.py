import subprocess
import os
import sys

'''
Need to fail on non docker or gcloud or functions emulator
not existing. Give informative message.
Customize docker container name?
api: py-cloud-fn build <function_name> --production | -p (default --emulator | e) && gcloud beta functions deploy <function_name> ...
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
        'pip install -r requirements.txt && ' +
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


def deploy_for_production(function_name='hello'):
    return [
        'gcloud', 'beta', 'functions', 'deploy', function_name,
        '--trigger-http', '--entry-point', 'serve', '--stage-bucket',
        'cloudfuncbucket', '--memory', '2048MB',
    ]


def build_cmd(filename='main.py', local=True):
    if local:
        return build_for_local(filename)
    return build_for_production(filename)


def main():
    process = subprocess.Popen(
        ' '.join(build_for_production()),
        stdout=sys.stdout,
        stdin=sys.stdin,
        shell=True)
    output, error = process.communicate()
    print output
