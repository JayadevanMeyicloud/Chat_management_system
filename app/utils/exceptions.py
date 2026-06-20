class AppError(Exception):
    status_code = 500
    default_message = "Internal Server Error"
    
    def __init__(self,message=None):
        super().__init__(message or self.default_message)
        
class InvalidRequestError(AppError):
    status_code = 400
    default_message = "Invalid request"
    
# class InvalidRequestError(Exception):
#     status_code = 400

#     def __init__(self, message="Invalid request"):
#         super().__init__(message)

    
class UnAuthorizedError(AppError):
    status_code = 401
    default_message = "UnAuthorized"
    
class ForbiddenError(AppError):
    status_code = 403
    default_message = "Forbidden"
    
class NotFoundError(AppError):
    status_code = 404
    default_message = "Not Found"
    
class ConflictError(AppError):
    status_code = 409
    default_message = "Conflict"
















class UserAlreadyExistsError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__("User already exists")

class InvalidPasswordError(Exception):
    status_code = 400

    def __init__(self):
        super().__init__("Password must contain uppercase, lowercase, number, special character and minimum 8 characters")


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
        
class AdminOnlyActionError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__("Only admins can perform this action")


class GroupAlreadyExistsError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__("Group already exists")

class GroupAccessDeniedError(Exception):
    status_code = 403

    def __init__(self):
        super().__init__("Access denied")
        
class GroupMemberAlreadyExistsError(Exception):
    status_code = 409

    def __init__(self):
        super().__init__("User is already a member of this group")
        

class GroupMemberNotFoundError(Exception):
    status_code = 404

    def __init__(self):
        super().__init__("Group member not found")