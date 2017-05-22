import subprocess
import os

def repo_root():
    return os.path.dirname(__file__) + '/../'

def hooks_path():
    return repo_root() + 'hooks'

'''
docker run --rm -ti -v $(pwd):/app lol /bin/sh -c 'cd app && pyinstaller test.py -y -n func' && \
gcloud beta functions deploy hello --trigger-http --entry-point serve --stage-bucket cloudfuncbucket --memory 2048MB
'''

def build_cmd(local=True):
    if local:
        return [
        'pyinstaller', 'main.py', '-y','-n' ,'func',
        '--clean', '--onedir',
        '--additional-hooks-dir', hooks_path(),
        '--hidden-import', 'htmlentitydefs',
        '--hidden-import', 'HTMLParser',
        '--hidden-import', 'Cookie',
        ]
    return ['echo', 'hello']

def main():
    process = subprocess.Popen(build_cmd(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print output
