from utils.router import Router
from service.direct_chat_service import create_chat,fetch_direct_chats


router = Router()


@router.post("/api/v1/direct-chats")
def create_direct_chat_route(event,context):
     
    body = event.get("body_data, {}")
     
    current_user_id = event.get("current_user_id")
    response = create_chat(
          body.get("receiver_id"),
          current_user_id
      )

    return {
          "statusCode":201,
          "message":"Direct chat created successfully",
          "data":{
              "chat_id":response
          }
      }
    
@router.get("/api/v1/direct-chats")
def get_direct_chat_route(event,context):
    
    current_user_id = event.get("current_user_id")
    response = fetch_direct_chats(current_user_id)
    
    return {
        "statusCode":200,
        "message":"Direct chats retrieved successfully",
        "data":{
            "chats":response
        }
    }