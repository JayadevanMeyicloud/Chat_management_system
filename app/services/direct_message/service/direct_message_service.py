from repository.direct_message_repository import is_chat_participant, get_chat_receiver

from repository.direct_message_repository import (
    check_duplicate_message,
    create_direct_message,
    get_direct_messages,
    get_message_by_id,
    delete_direct_message,
    create_delivery_record,
)
from utils.exceptions import (
    UnAuthorizedError,
    ForbiddenError,
    InvalidRequestError,
    NotFoundError,
)


# message should be store in direct_message and direct_message_delivery
def send_message(chat_id, sender_id, client_message_id, content):

    if not is_chat_participant(chat_id, sender_id):
        raise ForbiddenError("You are not a participant in this chat")

    if check_duplicate_message(sender_id, client_message_id):
        raise InvalidRequestError("Duplicate Message or client_message_id already exists")

    message = create_direct_message(chat_id, sender_id, client_message_id, content)

    receiver_id = get_chat_receiver(chat_id, sender_id)

    create_delivery_record(message["id"], receiver_id)

    return message


def fetch_message(chat_id, user_id):

    if not is_chat_participant(chat_id, user_id):
        raise ForbiddenError("you are not a participant in this chat")

    return get_direct_messages(chat_id)


def remove_message(chat_id, message_id, user_id):

    if not is_chat_participant(chat_id, user_id):
        raise ForbiddenError("you are not a participant in this chat")

    message = get_message_by_id(message_id)

    if not message:
        raise NotFoundError("Message not found")

    sender_id = str(message[1])

    if sender_id != user_id:
        raise UnAuthorizedError("You can delete only your own messages")

    delete_direct_message(message_id)
