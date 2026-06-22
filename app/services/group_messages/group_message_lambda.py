
import json

from repository.groupMessage_repository import get_user_by_cognito_sub
from routes.group_messages_routes import router
from utils.exceptions import AppError
from utils.logger import get_logger
from utils.response_handler import create_response

logger = get_logger(__name__)

def lambda_handler(event, context):
    
    logger.info ({
        "event": "request_received",
        "method": event.get("httpMethod"),
        "path": event.get("path")
    })
    try:
        #fetch logged in user from Token
        claims = event["requestContext"]["authorizer"]["claims"]
        cognito_sub = claims["sub"]
        current_user = get_user_by_cognito_sub(cognito_sub)
        event["current_user_id"] = str(current_user[0])
        event["body_data"] = json.loads(event.get("body") or "{}")
        response = router.resolve(event, context)
        
        return create_response(
            response["statusCode"],
            response["message"],
            response.get("data")
        )
    except AppError as e:
        logger.error({"event": "request_failed", "error": str(e)})
        return create_response(e.status_code, str(e))
    
    except Exception as e:
        logger.exception(e)
        return create_response(500, "Internal server error")