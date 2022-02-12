from . import check


def can_edit(current_user, other_user=None):
    """Checks if current_user is allowed to edit other_user"""
    if current_user == other_user:
        # We are always allowed to edit ourselves
        return
    check(current_user.role.can_manage_users)
