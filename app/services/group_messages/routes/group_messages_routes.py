from utils.router import Router
from service.groupMessage_service import send_message,fetch_messages,get_message,delete_message_service

router = Router()

@router.post("/api/v1/groups/{group_id}/messages")
def send_message_route(event, context, group_id):

    body = event.get("body_data") or {}

    result = send_message(
        group_id=group_id,
        sender_id=event.get("current_user_id"),
        content=body.get("content"),
        client_message_id=body.get("client_message_id")
    )

    return {
        "statusCode": 201,
        "message": "Message sent successfully",
        "data": result
    }


@router.get("/api/v1/groups/{group_id}/messages")
def fetch_messages_route(event, context, group_id):

    result = fetch_messages(group_id)

    return {
        "statusCode": 200,
        "message": "Messages fetched successfully",
        "data": result
    }


@router.get("/api/v1/groups/{group_id}/messages/{message_id}")
def get_message_route(event, context, group_id, message_id):

    result = get_message(message_id)

    return {
        "statusCode": 200,
        "message": "Message fetched successfully",
        "data": result
    }


@router.delete("/api/v1/groups/{group_id}/messages/{message_id}")
def delete_message_route(event, context, group_id, message_id):

    result = delete_message_service(
        message_id=message_id,
        current_user_id=event.get("current_user_id")
    )

    return {
        "statusCode": 200,
        "message": "Message deleted successfully",
        "data": result
    }