import json

from repository.group_repository import get_user_by_cognito_sub

from service.group_service import (
    create_new_group,
    fetch_groups,
    fetch_group,
    remove_group,
    change_group_settings
)

from utils.response_handler import create_response
from utils.logger import get_logger

from utils.exceptions import (
    AdminOnlyActionError,
    GroupAlreadyExistsError,
    GroupNotFoundError,
    GroupAccessDeniedError
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

        group_id = path_parameters.get("group_id")

        # CREATE GROUP
        if path == "/api/v1/groups" and method == "POST":

            response = create_new_group(
                current_user_id,
                body["name"],
                body.get("description")
            )

            logger.info({
                "event": "group_created",
                "group_name": body["name"],
                "created_by": current_user_id
            })

            return create_response(
                201,
                "Group created successfully",
                {
                    "group": response
                }
            )

        # GET ALL GROUPS
        if path == "/api/v1/groups" and method == "GET":

            response = fetch_groups()

            return create_response(
                200,
                "Groups fetched successfully",
                {
                    "groups": response
                }
            )

        # GET GROUP BY ID
        if (
            path == f"/api/v1/groups/{group_id}"
            and method == "GET"
        ):

            response = fetch_group(group_id)

            return create_response(
                200,
                "Group fetched successfully",
                {
                    "group": response
                }
            )

        # DELETE GROUP (Admin Only)
        if (
            path == f"/api/v1/groups/{group_id}"
            and method == "DELETE"
        ):

            remove_group(
                group_id,
                current_user_id
            )

            logger.info({
                "event": "group_deleted",
                "group_id": group_id,
                "deleted_by": current_user_id
            })

            return create_response(
                200,
                "Group deleted successfully"
            )

        # UPDATE GROUP SETTINGS (Admin Only)
        if (
            path == f"/api/v1/groups/{group_id}/settings"
            and method == "PATCH"
        ):

            response = change_group_settings(
                group_id,
                current_user_id,
                body["name"],
                body.get("description")
            )

            logger.info({
                "event": "group_settings_updated",
                "group_id": group_id,
                "updated_by": current_user_id
            })

            return create_response(
                200,
                "Group settings updated successfully",
                {
                    "group": response
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
        AdminOnlyActionError,
        GroupAlreadyExistsError,
        GroupNotFoundError,
        GroupAccessDeniedError
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