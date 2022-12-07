from pydantic import BaseModel

from app import auth, db
from app.db.models import Role
from app.db.models.user import User
from app.errors import AlreadyTakenError, NotAcceptableError, NotFoundError
from app.utils.bp import Blueprint

bp = Blueprint(__name__)


class RoleSchema(BaseModel):
    name: str
    can_edit_users: bool
    can_edit_hospitals: bool
    can_edit_listings: bool
    can_edit_staff: bool
    can_edit_roles: bool
    can_edit_persons: bool


class RolePatchSchema(BaseModel):
    name: str | None
    can_edit_users: bool | None
    can_edit_hospitals: bool | None
    can_edit_listings: bool | None
    can_edit_staff: bool | None
    can_edit_roles: bool | None
    can_edit_persons: bool | None


@bp.get('/')
def get_roles():
    return db.session.query(Role)


@bp.get('/<int:role_id>')
def get_role(role_id: int):
    role = db.session.get(Role, role_id)
    if not role:
        raise NotFoundError("No role found with this id.")
    return role


@bp.post('/')
@auth.route(edit_roles=True)
def create_role(data: RoleSchema):
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role = Role(**data.dict())
    db.session.add(role)
    db.session.commit()
    return role


@bp.post('/<int:role_id>')
@auth.route(edit_roles=True)
def update_role(role_id: int, data: RolePatchSchema):
    if db.session.query(Role).filter_by(name=data.name).first():
        raise AlreadyTakenError("name", data.name)
    role = get_role(role_id)
    for key, value in data.dict().items():
        if value is not None:
            setattr(role, key, value)
    db.session.commit()
    return role


@bp.delete('/<int:role_id>')
@auth.route(edit_roles=True)
def delete_role(role_id: int):
    if not (role := db.session.query(Role).filter_by(id=role_id).first()):
        raise NotFoundError("No role found with this id.")
    if db.session.query(User).filter_by(role=role).count() > 0:
        raise NotAcceptableError(
            "Please remove or update all users who have this role before"
            " removing it."
        )
    db.session.delete(role)
    db.session.commit()
