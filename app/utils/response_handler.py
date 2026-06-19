import json

def create_response(status_code, message, data=None):
    return {
        "statusCode": status_code,
        "body": json.dumps(
            {
                "success": status_code < 400,
                "message": message,
                "data": data or {}
            },
            default=str
        )
    }