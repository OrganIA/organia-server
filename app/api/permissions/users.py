from . import check


def can_edit(current, other=None):
    if current == other:
        return
    check(current.role.can_manage_users)
