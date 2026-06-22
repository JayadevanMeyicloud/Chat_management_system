from utils.router import Router
from service.direct_message_service import send_message, remove_message, fetch_message

router = Router()

#Send Message
@router.post("/api/v1/direct-chats/{chat_id}/messages")
def send_message_route(event, context,chat_id):
    
    body = event.get("body_data") or {}
    current_user_id = event.get("current_user_id")
    
    response= send_message(
        chat_id,
        current_user_id,
        body.get("client_message_id"),
        body.get("content")
    )
    
    return {
        "statusCode":201,
        "message":"Message sent successfully",
        "data":{
            "message_id":response
        }
    }
    
@router.get("/api/v1/direct-chats/{chat_id}/messages")
def fetch_message_route(event, context, chat_id):
    
    current_user_id = event.get("current_user_id")
    response = fetch_message(chat_id, current_user_id)
    
    return {
        "statusCode":200,
        "message":"Messages fetched successfully",
        "data":{
            "messages":response
        }
    }
    
@router.delete("/api/v1/direct-chats/{chat_id}/messages/{message_id}")
def remove_message_route(event, context, chat_id, message_id):
    
    current_user_id = event.get("current_user_id")
    remove_message(chat_id, message_id, current_user_id)
    
    return {
        "statusCode":200,
        "message":"Message deleted successfully",
        "data":None
    }

