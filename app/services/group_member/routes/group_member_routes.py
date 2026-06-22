from utils.router import Router

from service.groupMember_service import add_member, fetch_members, remove_member

router = Router()

@router.post("/api/v1/groups/{group_id}/members")
def add_member_route(event, context, group_id):

    body = event.get("body_data") or {}

    response = add_member(
        group_id,
        event.get("current_user_id"),
        body.get("user_id")
    )

    return {
        "statusCode": 201,
        "message": "Member added successfully",
        "data": {
            "member": response
        }
    }
    
@router.get("/api/v1/groups/{group_id}/members")
def get_members_route(event, context, group_id):

    response = fetch_members(group_id)

    return {
        "statusCode": 200,
        "message": "Members fetched successfully",
        "data": {
            "members": response
        }
    }
    
@router.delete("/api/v1/groups/{group_id}/members/{user_id}")
def remove_member_route(event, context, group_id, user_id):

    remove_member(
        group_id,
        event.get("current_user_id"),
        user_id
    )

    return {
        "statusCode": 200,
        "message": "Member removed successfully"
    }