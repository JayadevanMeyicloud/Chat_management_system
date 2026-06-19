import json

# from app.services.users.repository.user_repository import (
#     get_user_by_cognito_sub
# )

from app.services.direct_chat.repository.direct_chat_repository import (
    get_user_by_cognito_sub
)
from app.services.direct_chat.service.direct_chat_service import (
    create_chat,
    fetch_direct_chats
)

from layers.common.psycopg.python.utils.response_handler import create_response
from layers.common.psycopg.python.utils.logger import get_logger

from layers.common.psycopg.python.utils.exceptions import (
    DirectChatAlreadyExistsError,
    SelfChatNotAllowedError,
    ChatAccessDeniedError
)

logger = get_logger(__name__)


def lambda_handler(event, context):

    try:
        path = event.get("path")
        method = event.get("httpMethod")

        logger.info({
            "event": "request_received",
            "method": method,
            "path": path
        })

        claims = event["requestContext"]["authorizer"]["claims"]
        cognito_sub = claims["sub"]

        current_user = get_user_by_cognito_sub(cognito_sub)
        current_user_id = str(current_user[0])

        body = event.get("body") or "{}"

        if isinstance(body, str):
            body = json.loads(body)

        # CREATE DIRECT CHAT
        if (
            path == "/api/v1/direct-chats"
            and method == "POST"
        ):

            logger.info({
                "event": "create_direct_chat_requested",
                "receiver_id": body.get("receiver_id")
            })

            response = create_chat(
                current_user_id,
                body["receiver_id"]
            )

            logger.info({
                "event": "direct_chat_created",
                "user_id": current_user_id
            })

            return create_response(
                201,
                "Direct chat created successfully",
                {
                    "chat": response
                }
            )

        # GET DIRECT CHATS
        if (
            path == "/api/v1/direct-chats"
            and method == "GET"
        ):

            response = fetch_direct_chats(
                current_user_id
            )

            logger.info({
                "event": "direct_chats_fetched",
                "user_id": current_user_id
            })

            return create_response(
                200,
                "Direct chats fetched successfully",
                {
                    "chats": response
                }
            )

        logger.warning({
            "event": "route_not_found",
            "method": method,
            "path": path
        })

        return create_response(
            404,
            "Route not found"
        )

    except (
        DirectChatAlreadyExistsError,
        SelfChatNotAllowedError,
        ChatAccessDeniedError
    ) as e:

        logger.error({
            "event": "request_failed",
            "error": str(e)
        })

        return create_response(
            e.status_code,
            str(e)
        )

    except Exception as e:

        logger.exception({
            "event": "internal_error",
            "error": str(e)
        })

        return create_response(
            500,
            "Internal server error"
        )