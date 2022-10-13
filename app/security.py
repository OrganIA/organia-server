import secrets
from pathlib import Path

from app import config

SECRET_FILE = Path('./secret.key')


def generate_token() -> str:
    return secrets.token_hex()


def get_secret_key() -> str:
    with SECRET_FILE.open() as f:
        key = f.read()
        if key:
            return key
    key = config.SECRET_KEY or generate_token()
    with SECRET_FILE.open('w') as f:
        f.write(key)
    return key
