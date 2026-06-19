import json

from app.services.message_delivery_status.repository.message_delivery_repository import get_user_by_cognito_sub

from app.services.message_delivery_status.service.message_delivery_service import (
    update_delivery,
    fetch_delivery_report
)

from layers.common.psycopg.python.utils.response_handler import create_response
from layers.common.psycopg.python.utils.logger import get_logger

from layers.common.psycopg.python.utils.exceptions import (
    MessageNotFoundError,
    InvalidDeliveryStatusError,
    DeliveryAccessDeniedError,
    DeliveryRecordNotFoundError
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
        current_user_role = current_user[4]

        body = event.get("body") or "{}"

        if isinstance(body, str):
            body = json.loads(body)

        path_parameters = event.get("pathParameters") or {}

        message_id = path_parameters.get("message_id")

        # UPDATE DELIVERY STATUS
        if (
            path == f"/api/v1/message/delivery/{message_id}"
            and method == "PATCH"
        ):

            response = update_delivery(
                message_id,
                current_user_id,
                body["status"]
            )

            logger.info({
                "event": "delivery_updated",
                "message_id": message_id,
                "user_id": current_user_id
            })

            return create_response(
                200,
                "Delivery status updated successfully",
                {
                    "delivery": response
                }
            )

        # GET DELIVERY REPORT
        if (
            path == f"/api/v1/message/delivery/{message_id}/report"
            and method == "GET"
        ):

            response = fetch_delivery_report(
                message_id,
                current_user_id,
                current_user_role
            )

            logger.info({
                "event": "delivery_report_fetched",
                "message_id": message_id,
                "user_id": current_user_id
            })

            return create_response(
                200,
                "Delivery report fetched successfully",
                {
                    "report": response
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
        MessageNotFoundError,
        InvalidDeliveryStatusError,
        DeliveryAccessDeniedError,
        DeliveryRecordNotFoundError
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