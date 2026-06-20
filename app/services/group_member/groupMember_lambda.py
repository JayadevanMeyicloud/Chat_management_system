import json

from repository.groupMember_repository import get_user_by_cognito_sub

from service.groupMember_service import add_member, fetch_members, remove_member

from utils.response_handler import create_response

from utils.logger import get_logger
from utils.exceptions import AppError

logger = get_logger(__name__)


def lambda_handler(event, context):

    try:
        path = event.get("path")
        method = event.get("httpMethod")

        logger.info({"event": "request_received", "method": method, "path": path})

        claims = event["requestContext"]["authorizer"]["claims"]
        cognito_sub = claims["sub"]

        current_user = get_user_by_cognito_sub(cognito_sub)
        current_user_id = str(current_user[0])

        body = event.get("body") or "{}"

        if isinstance(body, str):
            body = json.loads(body)

        path_parameters = event.get("pathParameters") or {}

        group_id = path_parameters.get("group_id")
        user_id = path_parameters.get("user_id")

        # ADD MEMBER
        if path == f"/api/v1/groups/{group_id}/members" and method == "POST":
            response = add_member(group_id, current_user_id, body["user_id"])

            logger.info(
                {
                    "event": "member_added",
                    "group_id": group_id,
                    "user_id": body["user_id"],
                    "added_by": current_user_id,
                }
            )

            return create_response(
                201, "Member added successfully", {"member": response}
            )

        # GET MEMBERS
        if path == f"/api/v1/groups/{group_id}/members" and method == "GET":
            response = fetch_members(group_id)

            return create_response(
                200, "Members fetched successfully", {"members": response}
            )

        # REMOVE MEMBER
        if (
            path == f"/api/v1/groups/{group_id}/members/{user_id}"
            and method == "DELETE"
        ):
            remove_member(group_id, current_user_id, user_id)

            logger.info(
                {
                    "event": "member_removed",
                    "group_id": group_id,
                    "user_id": user_id,
                    "removed_by": current_user_id,
                }
            )

            return create_response(200, "Member removed successfully")

        logger.warning({"event": "route_not_found", "method": method, "path": path})

        return create_response(404, "Route not found")

    except AppError as e:
        logger.error({"event": "request_failed", "error": str(e)})

        return create_response(e.status_code, str(e))

    except Exception as e:
        logger.exception({"event": "internal_error", "error": str(e)})

        return create_response(500, "Internal server error")
