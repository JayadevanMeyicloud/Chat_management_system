class AppError(Exception):
    status_code = 500
    default_message = "Internal Server Error"
    
    def __init__(self,message=None):
        super().__init__(message or self.default_message)
        
        
class InvalidRequestError(AppError):
    status_code = 400
    default_message = "Invalid request"
       
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
    