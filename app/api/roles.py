from app import auth, db
from app.db.models import Role
from app.db.models.user import User
from app.errors import (
    AlreadyTakenError,
    NotAcceptableError,
    NotFoundError,
    Unauthorized,
)
from app.utils.bp import Blueprint
from app.utils.static import Static

bp = Blueprint(__name__)


class RoleSchema(Static):
    name = str
    can_edit_users = bool
    can_edit_hospitals = bool
    can_edit_listings = bool
    can_edit_staff = bool
    can_edit_roles = bool
    can_edit_persons = bool
    can_invite = bool


class RoleUpdateSchema(Static):
    __ERROR_ON_UNFOUND__ = False
    name = str
    can_edit_users = bool
    can_edit_hospitals = bool
    can_edit_listings = bool
    can_edit_staff = bool
    can_edit_roles = bool
    can_edit_persons = bool
    can_invite = bool


@bp.get('/')
@auth.route()
def get_roles():
    return db.session.query(Role).all()


@bp.get('/<int:role_id>')
@auth.route()
def get_role(role_id: int):
    return db.session.get(Role, role_id).to_dict()


@bp.post('/')
@auth.route()
def create_role(data: RoleSchema, auth_user: User):
    if not auth_user.role.can_edit_roles:
        raise Unauthorized('You do not have permission to create roles.')
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role = Role(**data.dict)
    db.session.add(role)
    db.session.commit()
    return role.to_dict()


@bp.post('/<int:role_id>')
@auth.route()
def update_role(role_id: int, data: RoleUpdateSchema, auth_user: User):
    if not auth_user.role.can_edit_roles:
        raise Unauthorized('You do not have permission to update roles.')
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role = db.session.get(Role, role_id)
    for key, value in data.dict.items():
        if value == 'null':
            setattr(role, key, None)
        elif value is not None:
            setattr(role, key, value)
    db.session.commit()
    return role.to_dict()


@bp.delete('/<int:role_id>')
@auth.route()
def delete_role(role_id: int, data: RoleUpdateSchema, auth_user: User):
    if not auth_user.role.can_edit_roles:
        raise Unauthorized('You do not have permission to delete roles.')
    if not (role := db.session.query(Role).filter_by(id=role_id).first()):
        raise NotFoundError("No role found with this id.")
    elif db.session.query(User).filter_by(role_id=role_id).all():
        raise NotAcceptableError(
            "Please remove or update all users who have this role before"
            " removing it."
        )
    else:
        db.session.delete(role)
        db.session.commit()
