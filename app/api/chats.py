from app import auth, db
from app.db.models import Chat, Message, User
from app.errors import InvalidRequest, NotFoundError, Unauthorized
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


def _get_chat(chat_id: int, auth_user: User):
    chat = db.session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("No chat found with this id.")
    if auth_user not in chat.users:
        raise Unauthorized("You are not in this chat.")
    return chat


@bp.get('/')
@auth.route()
def get_users_chats(auth_user: User):
    return auth_user.chats


@bp.get('/<int:chat_id>')
@auth.route()
def get_chat_by_id(chat_id: int, auth_user: User):
    return _get_chat(chat_id, auth_user)


@bp.get('/messages/latest')
@auth.route()
def get_latest_message_chat(auth_user: User):
    return [
        {"chat": x.chat, "last_message": x}
        for x in [
            db.session.query(Message)
            .filter_by(chat_id=chat.id)
            .order_by(Message.created_at.desc())
            .first()
            for chat in auth_user.chats
        ]
        if x is not None
    ]


@bp.get('/<int:chat_id>/messages')
@auth.route()
def get_chat_messages(chat_id: int, auth_user: User):
    chat = _get_chat(chat_id, auth_user)
    return chat.messages


class ChatCreateSchema(Static):
    users_ids = list
    name = str


def _create_users_list(users_ids: list, auth_user: User):
    users = []
    if auth_user.id not in users_ids:
        users_ids.append(auth_user.id)
    for user_id in users_ids:
        user = db.session.get(User, user_id)
        if not user:
            raise InvalidRequest("User not found")
        users.append(user)
    return users


@bp.post('/')
@auth.route()
def create_chat(data: ChatCreateSchema, auth_user: User):
    users = _create_users_list(data.users_ids, auth_user)
    chat = Chat(name=data.name, users=users, creator=auth_user)
    db.session.add(chat)
    db.session.commit()
    return chat


@bp.post('/<int:chat_id>')
@auth.route()
def update_chat(data: dict, chat_id: int, auth_user: User):
    chat = _get_chat(chat_id, auth_user)
    if "users_ids" in data:
        users = _create_users_list(data.users_ids, auth_user)
        chat.users = users
    if "name" in data:
        chat.name = data.name
    db.session.commit()
    return chat


@bp.delete('/<int:chat_id>')
@auth.route()
def delete_chat(chat_id: int, auth_user: User):
    chat = _get_chat(chat_id, auth_user)
    if chat.creator != auth_user:
        raise Unauthorized("You are not the creator of this chat.")
    db.session.delete(chat)
    db.session.commit()


class MessageCreateSchema(Static):
    content = str


@bp.post('/<int:chat_id>/messages')
@auth.route()
def send_message(chat_id: int, data: MessageCreateSchema, auth_user: User):
    chat = _get_chat(chat_id, auth_user)
    message = Message(content=data.content, chat=chat, sender=auth_user)
    db.session.add(message)
    db.session.commit()
    return message.to_dict()
