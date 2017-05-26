import subprocess
import os
import sys
import argparse
from jinja2 import Template

'''
Need to fail on non docker or gcloud
not existing. Give informative message.
Customize docker container name?

py-cloud-fn my-function http --production && \
cd cloudfn/target && gcloud beta functions deploy my-function \
--trigger-http --stage-bucket cloudfuncbucket --memory 2048MB && cd ../..

super-light. Lighter than go-cloud-fn which is very hard wrapping
'''


def package_root():
    return os.path.dirname(__file__) + '/'


def hooks_path(production=False):
    if production:
        return 'pip-cache/lib/python2.7/site-packages/cloudfn/hooks'
    return package_root() + 'hooks'


def image_name():
    return 'pycloudfn-builder'


def docker_path():
    return package_root() + 'docker/'


def output_name():
    return 'func'


def build_in_docker(file_name='main.py'):
    return [
        'docker', 'build', '-f', docker_path() + 'Dockerfile',
        '-t', image_name(), docker_path(), '&&', 'docker', 'run',
        '--rm', '-ti', '-v', '$(pwd):/app', image_name(), '/bin/sh', '-c',
        '\'cd app && test -d cloudfn || mkdir cloudfn && cd cloudfn '
        '&& test -d pip-cache || virtualenv pip-cache ' +
        '&& . pip-cache/bin/activate && ' +
        'test -f ../requirements.txt && pip install -r ../requirements.txt ' +
        '|| echo no requirements.txt present && ' +
        ' '.join(build(file_name, production=True)) + '\'',
    ]


def build(file_name='main.py', production=False):
    base = [
        'pyinstaller', '../' + file_name, '-y', '-n', output_name(),
        '--clean', '--onedir',
        '--additional-hooks-dir', hooks_path(production=production),
        '--hidden-import', 'htmlentitydefs',
        '--hidden-import', 'HTMLParser',
        '--hidden-import', 'Cookie',
    ]
    prefix = ''
    if os.path.isdir(prefix + './cloudfn-hooks'):
        base.append('--additional-hooks-dir')
        base.append('../cloudfn-hooks')
    if os.path.isfile(prefix + './.hidden-imports'):
        with open(prefix + '.hidden-imports') as f:
            for line in f:
                if not f == '':
                    base.append('--hidden-import')
                    base.append(line.rstrip())
    if not production:
        base.insert(0, 'test -d cloudfn || mkdir cloudfn && cd cloudfn && ')
    return base


def build_cmd(file_name='main.py', production=False):
    if production:
        return build_in_docker(file_name=file_name)
    return build(file_name=file_name)


def build_function(function_name, file_name='main.py', trigger_type='http',
                   production=False):
    exit_code = subprocess.call(
        ' '.join(build_cmd(file_name=file_name, production=production)),
        stdout=sys.stdout,
        stdin=sys.stdin,
        shell=True)
    if exit_code == 0:
        build_javascript(function_name, trigger_type=trigger_type)
    else:
        sys.exit(exit_code)
    sys.exit(cleanup())


def build_javascript(function_name, trigger_type='http'):
    js = open(package_root() + 'template/index.js').read()
    t = Template(js)
    rendered_js = t.render(config={
            'output_name': output_name(),
            'function_name': function_name,
            'trigger_http': trigger_type == 'http',
        }
    )
    open('cloudfn/index.js', 'w').write(rendered_js)


def cleanup():
    return subprocess.call(
        'cd cloudfn && rm -rf target && mkdir target && mv index.js target ' +
        '&& mv dist target',
        shell=True)


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
    parser.add_argument('-f', '--file_name', type=str, default='main.py',
                        help='The file name of the file you wish to build')

    args = parser.parse_args()
    build_function(args.function_name,
                   production=args.production,
                   trigger_type=args.trigger_type, file_name=args.file_name)
