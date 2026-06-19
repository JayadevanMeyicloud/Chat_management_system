from repository.direct_chat_repository import (
    get_existing_chat,
    create_direct_chat,
    get_direct_chats
)

from utils.exceptions import (
    DirectChatAlreadyExistsError,
    SelfChatNotAllowedError
)


def create_chat(current_user_id, receiver_id):

    # Prevent users from creating a chat with themselves
    if current_user_id == receiver_id:
        raise SelfChatNotAllowedError()

    # Check whether a direct chat already exists
    existing_chat = get_existing_chat(
        current_user_id,
        receiver_id
    )

    # Allow only one direct chat between two users
    if existing_chat:
        raise DirectChatAlreadyExistsError()

    # Create a new direct chat
    return create_direct_chat(
        current_user_id,
        receiver_id
    )


def fetch_direct_chats(user_id):

    # Get all direct chats for the logged-in user
    return get_direct_chats(user_id)

