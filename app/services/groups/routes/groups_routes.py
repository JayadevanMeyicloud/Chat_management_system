from utils.router import Router

from service.group_service import (
    create_new_group,
    fetch_groups,
    fetch_group,
    remove_group,
    change_group_settings,
)

router = Router()

#create group
@router.post("/api/v1/groups")
def create_group_route(event, context):

    body = event.get("body_data") or {}

    response = create_new_group(
        event.get("current_user_id"), body.get("name"), body.get("description")
    )

    return {
        "statusCode": 201,
        "message": "Group created successfully",
        "data": {"group": response},
    }

#get all groups
@router.get("/api/v1/groups")
def get_groups_route(event, context):

    response = fetch_groups()

    return {
        "statusCode": 200,
        "message": "Groups fetched successfully",
        "data": {"groups": response},
    }

#get single group
@router.get("/api/v1/groups/{group_id}")
def get_group_route(event, context, group_id):

    response = fetch_group(group_id)

    return {
        "statusCode": 200,
        "message": "Group fetched successfully",
        "data": {"group": response},
    }


@router.delete("/api/v1/groups/{group_id}")
def delete_group_route(event, context, group_id):

    remove_group(group_id, event.get("current_user_id"))

    return {"statusCode": 200, "message": "Group deleted successfully"}


@router.patch("/api/v1/groups/{group_id}/settings")
def update_group_settings_route(event, context, group_id):

    body = event.get("body_data") or {}

    response = change_group_settings(
        group_id,
        event.get("current_user_id"),
        body.get("name"),
        body.get("description"),
    )

    return {
        "statusCode": 200,
        "message": "Group settings updated successfully",
        "data": {"group": response},
    }
