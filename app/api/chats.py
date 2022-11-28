from app import auth, db
from app.db.models import Chat, ChatGroup, Message, User
from app.errors import InvalidRequest, NotFoundError, Unauthorized
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


@bp.get('/')
@auth.route()
def get_users_chats(auth_user: User):
    chat_group = (
        db.session.query(ChatGroup).filter_by(user_id=auth_user.id).all()
    )
    item_list = []
    for group in chat_group:
        tmp_list = (
            db.session.query(ChatGroup).filter_by(chat_id=group.chat_id).all()
        )
        tmp_list_chats = (
            db.session.query(Chat).filter_by(id=group.chat_id).all()
        )
        user_list = []
        for users in tmp_list:
            user_list.append(users.user_id)
        item_list.append(
            {
                "chat_id": group.chat_id,
                "users_ids": user_list,
                "chat_name": tmp_list_chats[0].chat_name,
                "creator_id": tmp_list_chats[0].creator_id,
            }
        )
    return item_list


@bp.get('/<int:chat_id>')
@auth.route()
def get_chat_by_id(chat_id: int, auth_user: User):
    chat_group = (
        db.session.query(ChatGroup)
        .filter_by(user_id=auth_user.id, chat_id=chat_id)
        .all()
    )
    if not chat_group:
        raise NotFoundError("No chat found for the user with this id.")
    chat = db.session.query(Chat).filter_by(id=chat_id).first()
    group = db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
    user_list = []
    for elem in group:
        user_list.append(elem.user_id)
    result = {
        "chat_id": group[0].chat_id,
        "users_ids": user_list,
        "chat_name": chat.chat_name,
        "creator_id": chat.creator_id,
    }
    return result


@bp.get('/messages/latest')
@auth.route()
def get_latest_message_chat(auth_user: User):
    chat_groups = (
        db.session.query(ChatGroup).filter_by(user_id=auth_user.id)
    ).all()
    if not chat_groups:
        return []
    latest_messages = []
    for chat_group in chat_groups:
        message = (
            db.session.query(Message)
            .filter_by(chat_id=chat_group.chat_id)
            .order_by(Message.created_at.desc())
        ).first()
        if message:
            latest_messages.append(message.to_dict())
    return sorted(
        latest_messages, key=lambda obj: obj['created_at'], reverse=True
    )


@bp.get('/<int:chat_id>/messages')
@auth.route()
def get_messages_of_chat(chat_id: int, auth_user: User):
    chat = (
        db.session.query(ChatGroup)
        .filter_by(chat_id=chat_id, user_id=auth_user.id)
        .all()
    )
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    return [
        message.to_dict()
        for message in db.session.query(Message)
        .filter_by(chat_id=chat_id)
        .all()
    ]


class ChatGroupsCreateSchema(Static):
    users_ids = list
    chat_name = str


@bp.post('/')
@auth.route()
def create_chat(data: ChatGroupsCreateSchema, auth_user: User):
    if auth_user.id not in data.users_ids:
        raise InvalidRequest(msg="Cannot create a chat for other users.")
    chat = Chat()
    chat.chat_name = data.chat_name
    chat.creator_id = auth_user.id
    db.session.add(chat)
    db.session.commit()
    item_list = {
        "chat_id": chat.id,
        "users_ids": [],
        "chat_name": data.chat_name,
        "creator_id": chat.creator_id,
    }
    for i in data.users_ids:
        db.session.add(ChatGroup(**{"user_id": i, "chat_id": chat.id}))
        item_list["users_ids"].append(db.session.get(User, i).id)
    db.session.commit()
    return item_list


@bp.post('/<int:chat_id>')
@auth.route()
def update_chat(data: dict, chat_id: int, auth_user: User):
    chat = db.session.query(Chat).filter_by(id=chat_id).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    if chat[0].creator_id != auth_user.id:
        raise InvalidRequest(msg="You are not the creator of this chat")
    item_list = {
        "chat_id": chat_id,
        "users_ids": [],
        "chat_name": chat[0].chat_name,
        "creator_id": chat[0].creator_id,
    }
    if "users_ids" in data:
        if auth_user.id not in data["users_ids"]:
            raise InvalidRequest(msg="Cannot remove the creator from the chat.")
        for i in data["users_ids"]:
            if db.session.query(User).filter_by(id=i).count() == 0:
                raise NotFoundError(f"User {i} not found.")

        chat_group = (
            db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
        )
        new_users_list = []
        for user_id in data["users_ids"]:
            new_users_list.append(user_id)
        former_users_list = []
        for former_user in chat_group:
            former_users_list.append(former_user.user_id)
        for i in former_users_list:
            if i not in new_users_list:
                db.session.query(ChatGroup).filter_by(
                    chat_id=chat_id, user_id=i
                ).delete()
        db.session.commit()
        for i in data["users_ids"]:
            if i not in former_users_list:
                item = ChatGroup(**{"user_id": i, "chat_id": chat_id})
                item.chat_id = chat_id
                db.session.add(item)
    if "chat_name" in data:
        setattr(chat[0], 'chat_name', data["chat_name"])
        item_list["chat_name"] = data["chat_name"]
    db.session.commit()
    chat_group = db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
    for chat in chat_group:
        item_list["users_ids"].append(chat.user_id)
    return item_list


@bp.delete('/<int:chat_id>')
@auth.route()
def delete_chat(chat_id: int, auth_user: User):
    chats = db.session.query(Chat).filter_by(id=chat_id).first()
    chat_groups = db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
    if chats and chat_groups:
        if auth_user.id != chats.creator_id:
            raise Unauthorized("You do not have permissions on this chat")
        for i in chat_groups:
            db.session.delete(i)
        db.session.delete(chats)
    else:
        raise NotFoundError("No chat found with this id.")
    db.session.commit()


class MessageCreateSchema(Static):
    sender_id = int
    chat_id = int
    content = str


@bp.post('/message')
@auth.route()
def send_message(data: MessageCreateSchema, auth_user: User):
    chat = (
        db.session.query(ChatGroup)
        .filter_by(chat_id=data.chat_id, user_id=auth_user.id)
        .all()
    )
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    message = Message(**data.dict)
    if not message:
        raise InvalidRequest
    db.session.add(message)
    db.session.commit()
    return message.to_dict()
