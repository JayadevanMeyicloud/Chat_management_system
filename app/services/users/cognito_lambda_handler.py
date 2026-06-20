import json
from routes.user_routes import router
from utils.response_handler import create_response
from utils.exceptions import AppError
from utils.logger import get_logger

logger = get_logger(__name__)

def lambda_handler(event,context):
    
    logger.info({
        "event":"request_received",
        "method":event.get("httpMethod"),
        "path":event.get("path")
    })
    
    try:
        event["body_data"] = json.loads(event.get("body") or "{}")
        response = router.resolve(event,context)
        return create_response(
            response["statusCode"],
            response["message"],
            response.get("data")
        )
    except AppError as e :
        return create_response(
            e.status_code,
            str(e)
        )
    except Exception as e:

        logger.exception(e)

        return create_response(
            500,
            "Internal server error"
        )