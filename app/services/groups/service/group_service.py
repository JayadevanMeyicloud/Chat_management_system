from app.services.groups.repository.group_repository import (
    get_group_by_name,
    create_group,
    get_groups,
    get_group_by_id,
    is_group_admin,
    delete_group,
    update_group_settings,
    get_user_role
)

from app.utils.exceptions import (
    AdminOnlyActionError,
    GroupAlreadyExistsError,
    GroupNotFoundError,
    GroupAccessDeniedError
)


def create_new_group(
    current_user_id,
    name,
    description
):
    role = get_user_role(current_user_id)

    if role != "admin":
        raise AdminOnlyActionError()

    existing_group = get_group_by_name(name)

    if existing_group:
        raise GroupAlreadyExistsError()

    return create_group(
        name,
        description,
        current_user_id
    )

#Fetch all groups
def fetch_groups():
    return get_groups()


#Fetch group by id
def fetch_group(group_id):

    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    return group

# Admin only - Delete group
def remove_group(
    group_id,
    current_user_id
):
    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    if not is_group_admin(
        group_id,
        current_user_id
    ):
        raise GroupAccessDeniedError()

    delete_group(group_id)

# Admin only - Update settings
def change_group_settings(
    group_id,
    current_user_id,
    name,
    description
):
    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    if not is_group_admin(
        group_id,
        current_user_id
    ):
        raise GroupAccessDeniedError()

    return update_group_settings(
        group_id,
        name,
        description
    )