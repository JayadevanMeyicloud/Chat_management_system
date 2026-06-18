import json

from app.services.users.service.cognito_service import register_user, verify_otp, login_user
from app.utils.response_handler import create_response
from app.utils.logger import get_logger
from app.utils.exceptions import (
    UserAlreadyExistsError,
    InvalidPasswordError,
    InvalidRequestError,
    InvalidCredentialsError,
    UserNotFoundError
)
from app.services.users.service.user_service import fetch_user

logger = get_logger(__name__)


def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")
    path_parameters = event.get("pathParameters") or {}
    user_id = path_parameters.get("user_id")

    logger.info({"event": "request_received", "method": method, "path": path})

    try:
        body = json.loads(event.get("body") or "{}")

        # REGISTER 
        if path == "/api/v1/auth/users" and method == "POST":
            register_user(
                body.get("name"),
                body.get("email"),
                body.get("password"))

            logger.info({"event": "register_success", "email": body.get("email")})

            return create_response(201, "User registered successfully")

        #GET users
        if path == f"/api/v1/auth/users/{user_id}" and method == "GET":

            response = fetch_user(user_id)

            return create_response(
                200,
                "User fetched successfully",
                {
                    "user": response
                }
            )

        # VERIFY 
        if path == "/api/v1/auth/verify" and method == "POST":
            verify_otp(
                body.get("email"), 
                body.get("otp"))

            logger.info({"event": "verify_success", "email": body.get("email")})

            return create_response(200, "Email verified successfully")

        # LOGIN 
        if path == "/api/v1/auth/login" and method == "POST":
            response = login_user(body.get("email"), body.get("password"))
            auth = response["AuthenticationResult"]

            logger.info({"event": "login_success", "email": body.get("email")})

            return create_response(
                200,
                "Login successful",
                {
                    "access_token": auth["AccessToken"],
                    "refresh_token": auth["RefreshToken"],
                    "id_token": auth["IdToken"]
                }
            )

        logger.warning({"event": "route_not_found", "path": path, "method": method})

        return create_response(404, "Route not found")

    except UserAlreadyExistsError as e:
        logger.error({"event": "register_failed", "error": str(e)})
        return create_response(409, str(e))

    except InvalidPasswordError as e:
        logger.error({"event": "register_failed", "error": str(e)})
        return create_response(400, str(e))

    except InvalidCredentialsError as e:
        logger.error({"event": "login_failed", "error": str(e)})
        return create_response(401, str(e))

    except InvalidRequestError as e:
        logger.error({"event": "request_failed", "error": str(e)})
        return create_response(400, str(e))

    except UserNotFoundError as e:
        logger.error({"event": "request_failed", "error": str(e)})
        return create_response(404, str(e))

    except Exception as e:
        logger.exception({"event": "internal_error", "error": str(e)})
        return create_response(500, "Internal server error")
    
