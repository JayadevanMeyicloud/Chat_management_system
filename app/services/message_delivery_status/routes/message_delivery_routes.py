from utils.router import Router

from service.message_delivery_service import update_delivery, fetch_delivery_report

router = Router()


@router.patch("/api/v1/message/delivery/{message_id}")
def update_delivery_route(event, context, message_id):

    body = event.get("body_data") or {}

    response = update_delivery(
        message_id, event.get("current_user_id"), body.get("status")
    )

    return {
        "statusCode": 200,
        "message": "Delivery status updated successfully",
        "data": {"delivery": response},
    }


@router.get("/api/v1/message/delivery/{message_id}/report")
def get_delivery_report_route(event, context, message_id):

    response = fetch_delivery_report(
        message_id, event.get("current_user_id"), event.get("current_user_role")
    )

    return {
        "statusCode": 200,
        "message": "Delivery report fetched successfully",
        "data": {"report": response},
    }
