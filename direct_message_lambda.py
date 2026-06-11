
import json

from app.repository.user_repository import get_user_by_cognito_sub
from app.services.direct_chat_service import (
    create_chat,
    fetch_direct_chats
)

from app.services.direct_message_service import (
    send_message,
    fetch_message,
    remove_message
)

from app.utils.response_handler import create_response
from app.utils.logger import get_logger

from app.utils.exceptions import (
    DirectChatAlreadyExistsError,
    SelfChatNotAllowedError,
    ChatAccessDeniedError,
    DuplicateMessageError,
    MessageNotFoundError,
    MessageDeleteForbiddenError
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

        path_parameters = event.get("pathParameters") or {}

        chat_id = path_parameters.get("chat_id")
        message_id = path_parameters.get("message_id")

        # CREATE DIRECT CHAT
        if path == "/api/v1/direct-chats" and method == "POST":

            logger.info({
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
                "Direct chat ready",
                {
                    "chat": response
                }
            )

        # GET DIRECT CHATS
        if path == "/api/v1/direct-chats" and method == "GET":

            response = fetch_direct_chats(current_user_id)

            return create_response(
                200,
                "Direct chats fetched successfully",
                {
                    "chats": response
                }
            )

        # SEND DIRECT MESSAGE
        if (
            path == f"/api/v1/direct-chats/{chat_id}/messages"
            and method == "POST"
        ):

            response = send_message(
                chat_id,
                current_user_id,
                body["client_message_id"],
                body["content"]
            )

            logger.info({
                "event": "message_sent",
                "chat_id": chat_id,
                "user_id": current_user_id
            })

            return create_response(
                201,
                "Message sent successfully",
                {
                    "message": response
                }
            )

        # GET DIRECT MESSAGES
        if (
            path == f"/api/v1/direct-chats/{chat_id}/messages"
            and method == "GET"
        ):

            response = fetch_message(
                chat_id,
                current_user_id
            )

            return create_response(
                200,
                "Messages fetched successfully",
                {
                    "messages": response
                }
            )

        # DELETE DIRECT MESSAGE
        if (
            path == f"/api/v1/direct-chats/{chat_id}/messages/{message_id}"
            and method == "DELETE"
        ):

            remove_message(
                chat_id,
                message_id,
                current_user_id
            )

            logger.info({
                "event": "message_deleted",
                "message_id": message_id,
                "user_id": current_user_id
            })

            return create_response(
                200,
                "Message deleted successfully"
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
        ChatAccessDeniedError,
        DuplicateMessageError,
        MessageNotFoundError,
        MessageDeleteForbiddenError
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