import os

from utils.exceptions import BadEnvironmentError


def android_tools_bin_dir() -> str:
    android_home = os.environ.get('ANDROID_HOME')
    return os.path.join(android_home, 'tools', 'bin')


def check_environment_variable_set(variable: str):
    variable_value = os.environ.get(variable, None)
    if not variable_value:
        message = '{} is not set!'.format(variable)
        raise BadEnvironmentError(message)


def get_temp_file(name: str) -> str:
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, name)
