import json
import boto3
import os

cognito = boto3.client("cognito-idp")

USER_POOL_ID = os.environ["USER_POOL_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]

def lambda_handler(event, context):

    try:
        body = json.loads(event.get("body", "{}"))

        email = body.get("email")
        password = body.get("password")

        if not email or not password:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "message": "email and password required"
                })
            }

        response = cognito.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "user_sub": response["UserSub"]
                }
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "message": str(e)
            })
        }