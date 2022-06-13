import os
from pathlib import Path
import yaml

PATH = Path('./config.yaml')


def _get_int(key, default=None):
    result = os.environ.get(key, default)
    if result:
        result = int(result)
    return result


def _get_bool(key, default=None):
    result = os.environ.get(key, default)
    if not result:
        return False
    result = result.lower()
    if result in ['n', 'no', 'false', 'f', '0', 'none', 'null']:
        return False
    return True


# A cryptographically secured key will be generated if none is provided
SECRET_KEY = os.environ.get('SECRET_KEY')

LOGIN_EXPIRATION_DAYS = _get_int('LOGIN_EXPIRATION_DAYS', 30)

DB_URL = os.environ.get('DB_URL', 'sqlite:///./app.db')

FORCE_LOGIN = _get_bool('FORCE_LOGIN')

DISCORD_LOGS = os.environ.get('DISCORD_LOGS')

LOG_SQL = _get_bool('LOG_SQL', 'no')

SENDGRID_API_URL = os.environ.get(
    'SENDGRID_API_URL', 'https://api.sendgrid.com/v3/mail/send'
)

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

SENDGRID_SENDER_EMAIL = os.environ.get(
    'SENDGRID_SENDER_EMAIL', 'botorgania@gmail.com'
)


def load_file():
    if not PATH.is_file():
        return
    with PATH.open() as f:
        data = yaml.safe_load(f)
    for key, value in data.items():
        os.environ[key] = value
