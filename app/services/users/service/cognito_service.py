import boto3

from core.config import CLIENT_ID
from repository.user_repository import create_user

from utils.exceptions import (
    ConflictError,
    InvalidRequestError,
    UnAuthorizedError
)

client = boto3.client("cognito-idp")


# REGISTER
def register_user(name, email, password):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "name", "Value": name},
                {"Name": "email", "Value": email}
            ]
        )

        create_user(response["UserSub"],name,email)
        return response

    except client.exceptions.UsernameExistsException:
        raise ConflictError("User already exists")

    except client.exceptions.InvalidPasswordException:
        raise InvalidRequestError(
            "Password must contain uppercase, lowercase, "
            "number, special character and minimum 8 characters"
        )
        
# VERIFY OTP
def verify_otp(email, otp):
    try:
        return client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=otp
        )

    except client.exceptions.CodeMismatchException:
        raise InvalidRequestError("Invalid OTP code")

    except client.exceptions.ExpiredCodeException:
        raise InvalidRequestError("OTP expired")

# LOGIN
def login_user(email, password):
    try:
        return client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            ClientId=CLIENT_ID,
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            }
        )

    except client.exceptions.NotAuthorizedException:
        raise UnAuthorizedError("Invalid credentials")

    except client.exceptions.UserNotConfirmedException:
        raise InvalidRequestError("Email not verified")