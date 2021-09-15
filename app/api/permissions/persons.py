from . import check


def can_edit(current):
    check(current.role.can_manage_persons)