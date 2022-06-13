from . import check


def can_edit(current_user, role=None):
    check(current_user.role.can_manage_roles)
