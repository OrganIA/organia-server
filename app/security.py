from datetime import datetime, timedelta
from typing import Optional
import os
import secrets


def get_secret_key():
    with open('secret.key') as f:
        key = f.read()
        if key:
            return key
    key = os.environ.get('key', secrets.token_hex())
    with open('secret.key', 'w') as f:
        f.write(key)
    return key


ALGORITHM = 'HS256'


def create_token(data: dict, delta: Optional[timedelta] = None):
    data = data.copy()
    data['exp'] = datetime.utcnow() + (delta or timedelta(days=30))
