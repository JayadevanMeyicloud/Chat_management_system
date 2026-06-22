import json
from routes.direct_message_routes import router
from repository.direct_message_repository import get_user_by_cognito_sub
from utils.response_handler import create_response
from utils.logger import get_logger
from utils.exceptions import AppError


logger = get_logger(__name__)


def lambda_handler(event, context):

    try:
        logger.info(
            {
                "event": "request_received",
                "method": event.get("httpMethod"),
                "path": event.get("path"),
            }
        )

        # Cognito user

        claims = event["requestContext"]["authorizer"]["claims"]

        cognito_sub = claims["sub"]

        current_user = get_user_by_cognito_sub(cognito_sub)

        event["current_user_id"] = str(current_user[0])

        # Parse body

        event["body_data"] = json.loads(event.get("body") or "{}")

        response = router.resolve(event, context)

        return create_response(
            response["statusCode"], response["message"], response.get("data")
        )

    except AppError as e:
        logger.error({"event": "request_failed", "error": str(e)})

        return create_response(e.status_code, str(e))

    except Exception as e:
        logger.exception(e)

        return create_response(500, "Internal server error")
