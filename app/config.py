import os


def _get_int(key, default=None):
    result = os.environ.get(key, default)
    if result:
        result = int(result)
    return result


# A cryptographically secured key will be generated if none is provided
SECRET_KEY = os.environ.get('SECRET_KEY')

LOGIN_EXPIRATION_DAYS = _get_int('LOGIN_EXPIRATION_DAYS', 30)

DB_URL = os.environ.get('DB_URL', 'sqlite:///./app.db')

CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

FORCE_LOGIN = bool(os.environ.get('FORCE_LOGIN'))

DISCORD_LOGS = os.environ.get('DISCORD_LOGS')

LOG_SQL = bool(os.environ.get('LOG_SQL', 1))
