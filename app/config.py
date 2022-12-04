import os
from pathlib import Path

import yaml

PATH = Path('./config.yaml')


def _to_int(value: str) -> int:
    return int(value)


def _to_bool(value: str) -> bool:
    value = value.lower()
    if value in ['n', 'no', 'false', 'f', '0', 'none', 'null']:
        return False
    return True


def env(key, default=None, coerce=None):
    result = os.environ.get(key, default)
    coerce = coerce or type(default)
    if not result or result == default:
        return result
    if coerce == int:
        result = _to_int(result)
    elif coerce == bool:
        result = _to_bool(result)
    return result


PORT = env('PORT', 8000)

# A cryptographically secured key will be generated if none is provided
# Used to hash passwords etc
SECRET_KEY = env('SECRET_KEY')

# Longetivity of a session
LOGIN_EXPIRATION_DAYS = env('LOGIN_EXPIRATION_DAYS', 30)

DB_URL = env('DB_URL', 'sqlite:///./data/app.db')
# Should SQL queries be logged?
LOG_SQL = env('LOG_SQL', False)

# Identifies as admin if no authorization header is provided
FORCE_LOGIN = env('FORCE_LOGIN', False)

AUTO_CREATE_DB = env('AUTO_CREATE_DB', True)


def load_file():
    if not PATH.is_file():
        return
    with PATH.open() as f:
        data = yaml.safe_load(f)
    for key, value in data.items():
        os.environ[key] = str(value)
