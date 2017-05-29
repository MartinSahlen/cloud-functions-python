import subprocess
import os
import sys
import argparse
from django.template import Template, Context


def package_root():
    return os.path.dirname(__file__) + '/'


def hooks_path(python_version, production):
    if production:
        if python_version == 3:
            return cache_dir(python_version) + \
                '/lib/python3.5/site-packages/cloudfn/hooks'
        if python_version == 2:
            return cache_dir(python_version) + \
                '/lib/python2.7/site-packages/cloudfn/hooks'
    return package_root() + 'hooks'


def cache_dir(python_version):
    return 'pip-cache-' + str(python_version)


def image_name(python_version):
    return 'pycloudfn-builder' + str(python_version)


def docker_path():
    return package_root() + 'docker/'


def output_name():
    return 'func'


def get_django_settings():
    m = os.environ.get('DJANGO_SETTINGS_MODULE', '')
    if m == '':
        return m
    return 'DJANGO_SETTINGS_MODULE='+m


def dockerfile(python_version):
    if python_version == 2:
        return 'DockerfilePython2'
    if python_version == 3:
        return 'DockerfilePython3'
    raise Exception('Python version not supported: ' + str(python_version))


def build_in_docker(file_name, python_version):
    return [
        'docker', 'build', '-f', docker_path() + dockerfile(python_version),
        '-t', image_name(python_version), docker_path(), '&&', 'docker', 'run',
        '--rm', '-ti', '-v', '$(pwd):/app', image_name(python_version),
        '/bin/sh', '-c',
        '\'cd app && test -d cloudfn || mkdir cloudfn && cd cloudfn '
        '&& test -d ' + cache_dir(python_version) + ' || virtualenv ' +
        cache_dir(python_version) + ' ' +
        '&& . ' + cache_dir(python_version) + '/bin/activate && ' +
        'test -f ../requirements.txt && pip install -r ../requirements.txt ' +
        '|| echo no requirements.txt present && ' +
        get_django_settings() + ' ' +
        ' '.join(build(file_name, python_version, True)) + '\'',
    ]


def build(file_name, python_version, production):
    base = [
        'pyinstaller', '../' + file_name, '-y', '-n', output_name(),
        '--clean', '--onedir',
        '--additional-hooks-dir', hooks_path(python_version, production),
        '--runtime-hook',
        hooks_path(python_version, production) + '/unbuffered.py',
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


def build_cmd(file_name, python_version, production):
    if production:
        return build_in_docker(file_name, python_version)
    return build(file_name, python_version, production)


def build_function(function_name, file_name,
                   trigger_type, python_version, production):
    exit_code = subprocess.call(
        ' '.join(build_cmd(file_name, python_version, production)),
        stdout=sys.stdout,
        stdin=sys.stdin,
        shell=True)
    if exit_code == 0:
        build_javascript(function_name, trigger_type)
    else:
        sys.exit(exit_code)
    sys.exit(cleanup())


def build_javascript(function_name, trigger_type):
    js = open(package_root() + 'template/index.js').read()
    t = Template(js)
    rendered_js = t.render(Context({
            'output_name': output_name(),
            'function_name': function_name,
            'trigger_http': trigger_type == 'http',
        })
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
    parser.add_argument('--python_version', type=int, default=2,
                        help='The python version you are targeting, '
                        'only applies when building for production',
                        choices=[2, 3])

    args = parser.parse_args()
    build_function(args.function_name,
                   args.file_name,
                   args.trigger_type,
                   args.python_version,
                   args.production,
                   )
