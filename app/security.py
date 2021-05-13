import secrets

from app import config


def generate_token() -> str:
    return secrets.token_hex()


def get_secret_key():
    with open('secret.key') as f:
        key = f.read()
        if key:
            return key
    key = config.SECRET_KEY or generate_token()
    with open('secret.key', 'w') as f:
        f.write(key)
    return key
