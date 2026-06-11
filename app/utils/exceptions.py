class UserAlreadyExistsError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__("User already exists")


class InvalidPasswordError(Exception):
    status_code = 400

    def __init__(self):
        super().__init__("Password must contain uppercase, lowercase, number, special character and minimum 8 characters")


class InvalidRequestError(Exception):
    status_code = 400

    def __init__(self, message="Invalid request"):
        super().__init__(message)


class InvalidCredentialsError(Exception):
    status_code = 401

    def __init__(self):
        super().__init__("Invalid credentials")


class UserNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__("User not found")
        
class GroupNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__("Group not found")


class GroupMembershipRequiredError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__(
            "You are not a member of this group"
        )


class GroupMessageNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__(
            "Group message not found"
        )


class GroupMessageDeleteForbiddenError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__(
            "You can delete only your own messages"
        )


class DuplicateMessageError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__(
            "Duplicate message detected"
        )
        
class DirectChatAlreadyExistsError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__("Direct chat already exists")


class SelfChatNotAllowedError(Exception):
    status_code = 400

    def __init__(self):
        super().__init__("Cannot create chat with yourself")


class ChatAccessDeniedError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__(
            "Forbidden. You are not a participant in this chat"
        )


class DuplicateMessageError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__(
            "Duplicate message. client_message_id already exists"
        )


class MessageNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__("Message not found")


class MessageDeleteForbiddenError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__(
            "Forbidden. You can only delete your own messages"
        )
        
class MessageNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__("Message not found")


class InvalidDeliveryStatusError(Exception):
    status_code = 400

    def __init__(self):
        super().__init__("Invalid delivery status")


class DeliveryAccessDeniedError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__("Access denied")


class DeliveryRecordNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__("Delivery record not found")