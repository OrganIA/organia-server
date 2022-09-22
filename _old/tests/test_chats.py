from . import client, PREFIX
from .fixtures import clean_db
from .helpers import assert_response

SAMPLE_CHAT = {
    'users_ids': [
        {
            "user_id": 1
        },
        {
            "user_id": 2
        },
    ]
}


def get_chats_of_user():
    response = client.get(f'{PREFIX}/chats/')
    return assert_response(response, type_=list)


def get_chat_by_id(id):
    response = client.get(f'{PREFIX}/chats/{id}')
    return assert_response(response, status_code=200)


def create_chat():
    response = client.post(
        f'{PREFIX}/chats/',
        json=SAMPLE_CHAT
    )
    return assert_response(response, status_code=201)


def test_create_chat():
    assert len(get_chats_of_user()) == 0
    assert_response(create_chat(), include=SAMPLE_CHAT)
    chat = get_chats_of_user()
    assert len(chat) == 1
    chat = chat[0]
    assert_response(chat, include=SAMPLE_CHAT)
    return chat
