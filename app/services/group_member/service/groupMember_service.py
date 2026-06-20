from repository.groupMember_repository import (
    get_group_by_id,
    is_group_admin,
    is_member_exists,
    add_group_member,
    get_group_members,
    remove_group_member,
    get_user_by_id,
)
from utils.exceptions import (
    NotFoundError,
    ConflictError,
    ForbiddenError
)

# Add member to group
def add_member(group_id, current_user_id, user_id):
    group = get_group_by_id(group_id)

    if not group:
        raise NotFoundError("Group not found")

    if not is_group_admin(group_id, current_user_id):
        raise ForbiddenError("Only admin can perform this action")

    user = get_user_by_id(user_id)

    if not user:
        raise NotFoundError("User not found")

    if is_member_exists(group_id, user_id):
        raise ConflictError("group member already exists")

    return add_group_member(group_id, user_id)


# Fetch all members
def fetch_members(group_id):

    group = get_group_by_id(group_id)

    if not group:
        raise NotFoundError("group not found")

    return get_group_members(group_id)


# Remove member from group
def remove_member(group_id, current_user_id, user_id):
    group = get_group_by_id(group_id)

    if not group:
        raise NotFoundError("Group not found")

    if not is_group_admin(group_id, current_user_id):
        raise ForbiddenError("Only admin can perform this action")

    member = is_member_exists(group_id, user_id)

    if not member:
        raise NotFoundError("group member not found")

    remove_group_member(group_id, user_id)
