from repository.groupMessage_repository import (
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

from utils.exceptions import(
    InvalidRequestError,
    ForbiddenError,
    NotFoundError,
    ConflictError
)

def send_message(
    group_id,
    sender_id,
    content,
    client_message_id=None
):

    group = get_group_by_id(group_id)

    if not group:
        raise NotFoundError("Group Not Found Error")

    if not is_group_member(group_id, sender_id):
        raise ForbiddenError("You are not a member of this group")

    if not content or not content.strip():
        raise InvalidRequestError("Message content cannot be empty")

    if ( client_message_id and is_duplicate_message(sender_id,client_message_id)):
        raise ConflictError("Duplicate message detected")

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

#Fetch all Messages from group
def fetch_messages(group_id):

    group = get_group_by_id(group_id)
    if not group:
        raise NotFoundError("Group Not Found ")

    return get_messages(group_id)

#Get single message
def get_message(message_id):

    message = get_message_by_id(message_id)

    if not message:
        raise NotFoundError("Message not found")

    return message

#Delete Messages
def delete_message_service(message_id, current_user_id):

    message = get_message_by_id(message_id)

    if not message:
        raise NotFoundError("Message not found")

    # Only sender can delete
    if str(message["sender_id"]) != str(current_user_id):
        raise ForbiddenError('You are not authorized to delete this message')
    

    delete_message(message_id)

    return {"deleted": True}