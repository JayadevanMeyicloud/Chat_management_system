from repository.groupMember_repository import (
    get_group_by_id,
    is_group_admin,
    is_member_exists,
    add_group_member,
    get_group_members,
    remove_group_member,
    get_user_by_id
)


from utils.exceptions import (
    GroupNotFoundError,
    GroupAccessDeniedError,
    UserNotFoundError,
    GroupMemberAlreadyExistsError,
    GroupMemberNotFoundError
)


# Add member to group
def add_member(
    group_id,
    current_user_id,
    user_id
):
    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    if not is_group_admin(
        group_id,
        current_user_id
    ):
        raise GroupAccessDeniedError()

    user = get_user_by_id(user_id)

    if not user:
        raise UserNotFoundError()

    if is_member_exists(
        group_id,
        user_id
    ):
        raise GroupMemberAlreadyExistsError()

    return add_group_member(
        group_id,
        user_id
    )


# Fetch all members
def fetch_members(group_id):

    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    return get_group_members(group_id)


# Remove member from group
def remove_member(
    group_id,
    current_user_id,
    user_id
):
    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    if not is_group_admin(
        group_id,
        current_user_id
    ):
        raise GroupAccessDeniedError()

    member = is_member_exists(
        group_id,
        user_id
    )

    if not member:
        raise GroupMemberNotFoundError()

    remove_group_member(
        group_id,
        user_id
    )