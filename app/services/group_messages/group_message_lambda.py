import json

from repository.groupMessage_repository import get_user_by_cognito_sub

from service.groupMessage_service import (
    send_message,
    fetch_messages,
    get_message,
    delete_message_service
)

from utils.exceptions import AppError
from utils.logger import get_logger
from utils.response_handler import create_response

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

        path_params = event.get("pathParameters") or {}
        group_id = path_params.get("group_id")
        message_id = path_params.get("message_id")

        if path == f"/api/v1/groups/{group_id}/messages" and method == "POST":
            result = send_message(
                group_id=group_id,
                sender_id=current_user_id,
                content=body.get("content"),
                client_message_id=body.get("client_message_id")
            )

            logger.info({
                "event": "message_sent",
                "group_id": group_id,
                "user_id": current_user_id
            })

            return create_response(201, "Message sent successfully", result)

        if path == f"/api/v1/groups/{group_id}/messages" and method == "GET":
            result = fetch_messages(group_id)
            return create_response(200, "Messages fetched successfully", result)

        if path == f"/api/v1/groups/{group_id}/messages/{message_id}" and method == "GET":
            result = get_message(message_id)
            return create_response(200, "Message fetched successfully", result)

        if path == f"/api/v1/groups/{group_id}/messages/{message_id}" and method == "DELETE":
            result = delete_message_service(
                message_id=message_id,
                current_user_id=current_user_id
            )

            logger.info({
                "event": "message_deleted",
                "message_id": message_id,
                "deleted_by": current_user_id
            })

            return create_response(200, "Message deleted successfully", result)

        logger.warning({
            "event": "route_not_found",
            "method": method,
            "path": path
        })

        return create_response(404, "Route not found")

    except AppError as e:
        logger.error({
            "event": "request_failed",
            "error": str(e)
        })
        return create_response(e.status_code, str(e))

    except Exception as e:
        logger.exception({
            "event": "internal_error",
            "error": str(e)
        })
        return create_response(500, "Internal server error")