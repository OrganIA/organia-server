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
server = 'http://localhost:8000'
prefix = '/api'


AUTH_NOTE = (
    '> :lock: This request requires authentication. Pass `Bearer: the-token` in'
    ' the `Authorization` header.'
)

ADMIN_NOTE = (
    '> :police_car: This request requires specific permissions. An user must be'
    ' authenticated via a token and their role must have the permissions'
    ' {perms} to access this route.'
)

file = inspect.getsourcelines(sys.modules[__name__])[0]
errors = []


@dataclass
class Route:
    path: str
    requests: list[dict] = field(default_factory=list)
    auth: bool = True
    admin: bool = False
    show: bool = True
    perms: list[str] = field(default_factory=list)

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
            print(self.method.upper(), self.path)
            self.responses.append(
                {
                    'request': request,
                    'response': requests.request(
                        self.method, url, json=body, params=params
                    ),
                }
            )
            last = self.responses[-1]['response']
            print(last.status_code)
            if last.status_code == 500:
                errors.append(last)

    @property
    def href(self):
        last_was_dash = False
        s = ''
        for c in self.title.lower():
            if c in (' ',):
                if not last_was_dash:
                    s += '-'
                last_was_dash = True
            else:
                if c not in ('#', '/', ':', '(', ')', '?', '&', '=', ','):
                    s += c
                last_was_dash = False
        return s.strip('-')

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
        if self.perms:
            line(ADMIN_NOTE.format(perms=', '.join(self.perms)))
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


user_login = {
    "email": f"user{random.randint(0, 1000)}@email.com",
    "password": "password",
}
user_login2 = {
    "email": f"user{random.randint(0, 1000)}@email.com",
    "password": "password",
}
user_register = dict(
    **user_login,
    firstname="prenom",
    lastname="nom",
    phone_number="+33123456789",
)
user_login_fail1 = {"email": "user@email.com", "password": "not-the-password"}
user_login_fail2 = {
    "email": user_login["email"],
    "password": "not-the-password",
}

calls = [
    # Information about the server, such as the version or the OS.
    # Useful to check if the server is up, or to check if it is running
    # the latest version.
    Get('/', auth=False),
    # Register a new user, response should be the same as login, so no need to
    # login after registering.
    Post('/auth/register', [user_register, user_register], auth=False),
    Post('/auth/register', user_login2, auth=False, show=False),
    # Login and get a token.
    Post(
        '/auth/login',
        [user_login, user_login_fail1, user_login_fail2],
        auth=False,
    ),
    # List all users
    Get('/users'),
    # Get info about the current user
    Get('/users/me'),
    # Get info about a specific user
    Get('/users/1'),
    # Delete a user
    Delete('/users/3', perms=['edit_users']),
    # Create a new chat
    Post('/chats', {"name": "Chat name", "users_ids": [1, 2]}),
    # Get all the chats the current user is part of
    Get('/chats'),
    # Get a specific chat
    Get('/chats/1'),
    # Send a message
    Post(
        '/chats/1/messages',
        {"content": "Hello world!"},
    ),
    # Get all chats the current user is part of and the last message of each
    Get('/chats/messages/latest'),
    # Get all messages for a specific chat
    Get('/chats/1/messages'),
    # Delete a chat
    Delete('/chats/1'),
    # Lists all user roles
    Get('/roles'),
    # Get a specific role
    Get('/roles/1'),
    # Create a new role
    Post(
        '/roles',
        {
            "name": "New role",
            "can_edit_users": False,
            "can_edit_hospitals": False,
            "can_edit_listings": False,
            "can_edit_staff": False,
            "can_edit_roles": False,
            "can_edit_persons": False,
        },
        perms=['edit_roles'],
    ),
    # Update a role
    Post('/roles/3', {"name": "Updated role"}, perms=['edit_roles']),
    # Delete a role
    Delete('/roles/3', perms=['edit_roles']),
    # Create a receiver listing for a liver, creating the Person and Organ in
    # one go
    Post(
        '/listings',
        {
            "type": "RECEIVER",
            "person": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+33123456789",
                "gender": "MALE",
                "birth_date": "1990-02-10",
                "abo": "A",
                "rhesus": "+",
            },
            "organ_type": "LIVER",
            "organ": {
                "tumors_count": 2,
                "biggest_tumor_size": 10,
                "alpha_fetoprotein": 10,
            },
        },
    ),
    # Create a receiver listing for a lung, creating the Person and Organ in
    # one go
    # - `diagnosis_group` can be A, B, C, or D
    # - `detailed_diagnosis` can be one of the following: BRONCHIECTASIS,
    # EISENMENGER, BRONCHIOLITIS, LAM, or SARCOIDOSIS
    # - `body_mass_index` for a normal person is expected to be between 18.5 and
    # 25
    # - `pulmonary_artery_systolic` is expected to be between 17 and 20, > 30 is
    # considered critical
    # - `carbon_dioxide_partial_pressure` is expected to be between 35 and 40
    # - `pulmonary_capilary_wedge_pressure` is expected to be between 8 and 12,
    # \> 20 is considered critical
    # - `creatinine` is expected to be between 7 and 13
    Post(
        '/listings',
        {
            "type": "RECEIVER",
            "person": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+33123456789",
                "gender": "MALE",
                "birth_date": "1990-02-10",
                "abo": "A",
                "rhesus": "+",
            },
            "organ_type": "LUNG",
            "organ": {
                "diagnosis_group": "A",
                "detailed_diagnosis": "LAM",
                "body_mass_index": 17.9,
                "diabetes": False,
                "assistance_required": False,
                "pulmonary_function_percentage": 0.85,
                "pulmonary_artery_systolic": 25.2,
                "oxygen_requirement": 0.5,
                "six_minutes_walk_distance_over_150_feet": True,
                "continuous_mech_ventilation": True,
                "carbon_dioxide_partial_pressure": 36.3,
                "carbon_dioxide_partial_pressure_15_percent_increase": False,
                "activities_of_daily_life_required": False,
                "pulmonary_capilary_wedge_pressure": 9.2,
                "creatinine": 10.2,
            },
        },
    ),
    # Create a receiver listing for a kidney, creating the Person in one go
    Post(
        '/listings',
        {
            "type": "RECEIVER",
            "person": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+33123456789",
                "gender": "MALE",
                "birth_date": "1990-02-10",
                "abo": "A",
                "rhesus": "+",
            },
            "organ": {
                "is_under_dialysis": True,
                "is_retransplantation": False,
                "dialysis_start_date": "2022-12-12",
                "arf_date": "2022-12-12",
                "date_transplantation": "2022-12-12",
                "re_registration_date": "2022-12-12",
                "A": 1.2,
                "B": 1.3,
                "DR": 1.4,
                "DQ": 1.5,
            },
            "organ_type": "KIDNEY",
        },
    ),
    # Create a donor listing for a liver, creating the Person in one go
    Post(
        '/listings',
        {
            "type": "DONOR",
            "person": {
                "first_name": "Johnatan",
                "last_name": "Joeystarr",
                "phone_number": "+33123456789",
                "gender": "MALE",
                "birth_date": "1990-02-10",
                "abo": "A",
                "rhesus": "+",
            },
            "organ_type": "LIVER",
        },
    ),
    # Create a donor listing for a kidney, creating the Person in one go
    Post(
        '/listings',
        {
            "type": "DONOR",
            "person": {
                "first_name": "Johnatan",
                "last_name": "Joeystarr",
                "phone_number": "+33123456789",
                "gender": "MALE",
                "birth_date": "1990-02-10",
                "abo": "A",
                "rhesus": "+",
            },
            "organ_type": "KIDNEY",
        },
    ),
    # Create a donor listing for a lung, creating the Person in one go
    Post(
        '/listings',
        {
            "type": "DONOR",
            "person": {
                "first_name": "Johnatan",
                "last_name": "Joeystarr",
                "phone_number": "+33123456789",
                "gender": "MALE",
                "birth_date": "1990-02-10",
                "abo": "A",
                "rhesus": "+",
            },
            "organ_type": "LUNG",
        },
    ),
    # Update a listing
    Post(
        '/listings/1',
        {
            "start_date": "2020-02-10",
        },
    ),
    # Update only a subset of the fields of a listing
    Post(
        '/listings/1',
        {
            "organ": {
                "alpha_fetoprotein": 20,
            },
            "person": {
                "first_name": "Jojo",
            },
        },
    ),
    # Get all listings
    Get('/listings/'),
    # Only get donor listings
    Get('/listings/?type=donor'),
    # Only get receiver listings
    Get('/listings/?type=receiver'),
    # Get a specific listing
    Get('/listings/1'),
    # Get a list of all matching receivers for a liver listing, with the score
    Get('/listings/4/matches'),
    # Get a list of all matching receivers for a lung listing, with the score
    Get('/listings/5/matches'),
    # Get a list of all matching receivers for a kidney listing, with the score
    Get('/listings/6/matches'),
    # Delete a listing
    Delete('/listings/2'),
]


if __name__ == '__main__':
    with target.open('w') as f:
        f.write(
            '# API Documentation\nGenerated on: '
            + datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
            + '\n\n'
        )
        for call in calls:
            if not call.show:
                continue
            f.write(f'- [{call.title}](#{call.href})\n')
        f.write('\n\n')
        for call in calls:
            if not call.show:
                call.fetch()
                continue
            f.write(call.to_markdown())
            f.write('\n\n')
    print('Errors:', errors)
