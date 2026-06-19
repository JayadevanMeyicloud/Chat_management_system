
import boto3

# from layers.common.psycopg.python.core.config import CLIENT_ID
# from app.services.users.repository.user_repository import create_user

# from layers.common.psycopg.python.utils.exceptions import (
#     UserAlreadyExistsError,
#     InvalidCredentialsError,
#     InvalidPasswordError,
#     InvalidRequestError
# )
from core.config import CLIENT_ID

from repository.user_repository import create_user

from utils.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InvalidPasswordError,
    InvalidRequestError
)

client = boto3.client("cognito-idp")


# ---------------- REGISTER ----------------
def register_user(name, email, password):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    "Name": "name",
                    "Value": name
                },
                {
                    "Name": "email",
                    "Value": email
                }
            ]
        )

        cognito_sub = response["UserSub"]

        create_user(
            cognito_sub,
            name,
            email
        )

        return response

    except client.exceptions.UsernameExistsException:
        raise UserAlreadyExistsError()

    except client.exceptions.InvalidPasswordException:
        raise InvalidPasswordError()

    except Exception as e:
        raise InvalidRequestError(str(e))


# ---------------- VERIFY ----------------
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

    except Exception as e:
        raise InvalidRequestError(str(e))


# ---------------- LOGIN ----------------
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
        raise InvalidCredentialsError("Invalid Credentials")

    except client.exceptions.UserNotConfirmedException:
        raise InvalidRequestError("Email not verified")

    except Exception as e:
        raise InvalidRequestError(str(e))