#!/usr/bin/env python

import inspect
import json
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import requests

target = Path('docs/api.md')
server = 'http://localhost:5000'
prefix = '/api'


AUTH_NOTE = (
    '> :lock: This request requires authentication. Pass `Bearer: the-token` in'
    ' the `Authorization` header.'
)

ADMIN_NOTE = (
    '> :police_car: This request requires admin privileges. An user must be'
    ' authenticated via a token and have the `is_admin` flag set to `True`.'
)

file = inspect.getsourcelines(sys.modules[__name__])[0]


@dataclass
class Route:
    path: str
    requests: list[dict] = field(default_factory=list)
    auth: bool = True
    admin: bool = False

    method = None
    desc = None
    responses: list = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def _extract_desc(self):
        """Extracts the description from the source code.

        Every line starting with `#` immediately above the class instantiation
        is considered part of the description.
        """
        frame = list(inspect.stack())[-1]
        desc = ''
        lineno = frame.lineno - 2
        while True:
            line = file[lineno].strip()
            if not line.startswith('#'):
                break
            desc = line[2:] + '\n' + desc
            lineno -= 1
        self.desc = desc
        print(self.desc)

    def __post_init__(self):
        self._extract_desc()
        self.path = prefix + self.path
        if not isinstance(self.requests, list):
            self.requests = [self.requests]

    def fetch(self):
        if self.responses:
            return
        url = server + self.path
        if not self.requests:
            self.requests.append({})
        for request in self.requests:
            body = request.get('body', request if self.method != 'get' else {})
            params = request.get(
                'params', request if self.method == 'get' else {}
            )
            self.responses.append(
                {
                    'request': request,
                    'response': requests.request(
                        self.method, url, json=body, params=params
                    ),
                }
            )

    @property
    def href(self):
        s = f'{self.title}'.lower()
        for c in (' ', '/'):
            s = s.replace(c, '-')
        return s

    @property
    def title(self):
        return f'{self.method.upper()} {self.path}'

    def to_markdown(self):
        self.fetch()

        def format_json(data: bytes or dict):
            if isinstance(data, bytes):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    return data.decode()
            return '```json\n' + json.dumps(data, indent=2) + '\n```\n'

        lines = []

        def line(*args):
            for arg in args:
                if not arg:
                    continue
                lines.append(arg)

        line(f'## {self.title}')
        line(self.desc)
        if self.admin:
            line(ADMIN_NOTE)
        elif self.auth:
            line(AUTH_NOTE)
        for response in self.responses:
            if response.get('request'):
                line('### Request')
                line(format_json(response['request']))
            line('### Response')
            line(format_json(response['response'].content))
            line(f'**Status:** {response["response"].status_code}')
        return '\n'.join(lines)


class Get(Route):
    method = 'get'


class Post(Route):
    method = 'post'


class Delete(Route):
    method = 'delete'


user_login = {"email": "user@email.com", "password": "password"}
user_register = {
    "email": f"user{random.randint(0, 1000)}@email.com",
    "password": "password",
    "firstname": "prenom",
    "lastname": "nom",
    "phone_number": "123456789",
}
user_login_fail = {"email": "user@email.com", "password": "not-the-password"}

calls = [
    # Information about the server, such as the version or the OS.
    # Useful to check if the server is up, or to check if it is running
    # the latest version.
    Get('/', auth=False),
    # Login and get a token.
    Post('/auth/login', [user_login, user_login_fail], auth=False),
    # Register a new user, response should be the same as login, so no need to
    # login after registering.
    Post('/auth/register', [user_register, user_login], auth=False),
    # List all users
    Get('/users'),
    # Get info about the current user
    Get('/users/me'),
    # Get info about a specific user
    Get('/users/1'),
    # Delete a user
    Delete('/users/3', admin=True),
    # Get the list of listings
    Get('/listings', [{}, {'page': 2, 'per_page': 10}, {'search': 'jean'}]),
    # Get a specific listing
    Get('/listings/1'),
    # Get the matching listings for an organ
    Get('/listings/1/matches'),
    # Get all the users chats
    Get('/chats'),
    # Get a specific chat
    Get('/chats/1'),
    # Create a new chat
    Post('/chats', {"chat_name": "Chat name", "users_ids": [1, 2]}),
    # Get all latest messages
    Get('/chats/messages/latest'),
    # Get all messages for a specific chat
    Get('/chats/1/messages'),
    # Send a message
    Post(
        '/chats/1/messages',
        {"content": "Hello world!", "sender_id": 1, "chat_id": 1},
    ),
    # Delete a chat
    Delete('/chats/1'),
]


if __name__ == '__main__':
    with target.open('w') as f:
        f.write(
            '# API Documentation\nGenerated on: '
            + datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
            + '\n\n'
        )
        for call in calls:
            f.write(f'- [{call.title}](#{call.href})\n')
        f.write('\n\n')
        for call in calls:
            f.write(call.to_markdown())
            f.write('\n\n')
