from . import check


def can_edit(current, other):
    check(current == other)
    check(current.role.can_manage_users)