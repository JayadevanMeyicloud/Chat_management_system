
from app.services.group_messages.repository.groupMessage_repository import (
    is_duplicate_message,
    create_message,
    get_messages,
    get_message_by_id,
    delete_message,
    create_delivery_records,
    get_group_members,
    get_group_by_id,
    is_group_member
)

from app.utils.exceptions import (
    GroupNotFoundError,
    GroupMembershipRequiredError,
    GroupMessageNotFoundError,
    GroupMessageDeleteForbiddenError,
    DuplicateMessageError
)


# =========================
# SEND MESSAGE
# =========================
# def send_message(group_id, sender_id, content, client_message_id=None):

#     group = get_group_by_id(group_id)
#     if not group:
#         raise GroupNotFoundError()

#     member = is_group_member(group_id, sender_id)
#     if not member:
#         raise GroupMembershipRequiredError()

#     if not content or not content.strip():
#         raise Exception("Message content cannot be empty")

#     if client_message_id:
#         duplicate = is_duplicate_message(sender_id, client_message_id)
#         if duplicate:
#             raise DuplicateMessageError()

#     return create_message(
#         group_id=group_id,
#         sender_id=sender_id,
#         content=content,
#         client_message_id=client_message_id
#     )
def send_message(
    group_id,
    sender_id,
    content,
    client_message_id=None
):

    group = get_group_by_id(group_id)

    if not group:
        raise GroupNotFoundError()

    if not is_group_member(group_id, sender_id):
        raise GroupMembershipRequiredError()

    if not content or not content.strip():
        raise Exception("Message content cannot be empty")

    if (
        client_message_id and
        is_duplicate_message(
            sender_id,
            client_message_id
        )
    ):
        raise DuplicateMessageError()

    message = create_message(
        group_id=group_id,
        sender_id=sender_id,
        content=content,
        client_message_id=client_message_id
    )

    members = get_group_members(group_id)

    delivery_users = [
        member_id
        for member_id in members
        if member_id != sender_id
    ]

    if delivery_users:
        create_delivery_records(
            message["id"],
            delivery_users
        )

    return message


# =========================
# FETCH ALL MESSAGES
# =========================
def fetch_messages(group_id, limit=50, offset=0):

    group = get_group_by_id(group_id)
    if not group:
        raise GroupNotFoundError()

    return get_messages(group_id)


# =========================
# GET SINGLE MESSAGE
# =========================
def get_message(message_id):

    message = get_message_by_id(message_id)

    if not message:
        raise GroupMessageNotFoundError()

    return message


# =========================
# DELETE MESSAGE
# =========================
def delete_message_service(message_id, current_user_id):

    message = get_message_by_id(message_id)

    if not message:
        raise GroupMessageNotFoundError()

    # Only sender can delete
    if str(message["sender_id"]) != str(current_user_id):
        raise GroupMessageDeleteForbiddenError()

    delete_message(message_id)

    return {"deleted": True}