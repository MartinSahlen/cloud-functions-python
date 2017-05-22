import subprocess
import os


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
        '--rm', '-ti', '-v', '$(pwd):/app', image_name(), '/bin/sh', '-c',
        'cd app && virtualenv pip-cache && source ./pip-cache/bin/activate'
        ' && pip install -r requirements.txt',
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
        stdout=subprocess.PIPE,
        shell=True)
    output, error = process.communicate()
    print output
