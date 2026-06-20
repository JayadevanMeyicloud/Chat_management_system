from utils.router import Router
from service.cognito_service import register_user,verify_otp,login_user
from service.user_service import fetch_user

router = Router()

@router.post("/api/v1/auth/users")
def register_route(event, context):
    
    body = event.get("body_data",{})
    register_user(
        body.get("name"),
        body.get("email"),
        body.get("password")
    )
    
    return {
    "statusCode": 201,
    "message": "User registered successfully",
    "data": None
}
@router.get("/api/v1/auth/users/{user_id}")
def get_user_route(event, context,user_id):
    
    response = fetch_user(user_id)

    return {"statusCode": 200, "message": "User fetched successfully", 
            "data":
                {"user": response}
            }
    
@router.post("/api/v1/auth/verify")
def verify_route(event, context):
    
    body = event.get("body_data",{})
    verify_otp(
        body.get("email"),
        body.get("otp")
    )

    return {
    "statusCode":200,
    "message":"User verified successfully",
    "data":None
}
    
@router.post("/api/v1/auth/login")
def login_route(event, context):

    body = event.get("body_data", {})
    
    response = login_user(
        body.get("email"),
        body.get("password")
    )

    auth = response["AuthenticationResult"]

    return {
        "statusCode":200,
        "message":"Login successful",
        "data":{
            "access_token":auth["AccessToken"],
            "refresh_token":auth["RefreshToken"],
            "id_token":auth["IdToken"]
        }
    }