from repository.message_delivery_repository import get_message_type

from repository.group_delivery_repository import (
    update_group_delivery_status,
    get_group_delivery_report
)

from repository.direct_delivery_repository import (
    update_direct_delivery_status,
    get_direct_delivery_report
)
from utils.exceptions import(
    InvalidRequestError,
    ForbiddenError,
    NotFoundError,
)

VALID_STATUSES = [
    "pending",
    "delivered",
    "read"
]


def update_delivery( message_id,user_id,status):

    if status not in VALID_STATUSES:
        raise InvalidRequestError("Invalid delivery status")

    message = get_message_type(message_id)

    if not message:
        raise NotFoundError("Message not found")
    
    if message["type"] == "group":

        delivery = update_group_delivery_status(message_id,user_id,status)
        
    else:

        delivery = update_direct_delivery_status(message_id,user_id,status)

    if not delivery:
        raise NotFoundError("Delivery record not found")

    return {
        "message_id": str(delivery[0]),
        "user_id": str(delivery[1]),
        "status": delivery[2]
    }


def fetch_delivery_report( message_id,current_user_id,current_user_role ):

    message = get_message_type(message_id)

    if not message:
        raise NotFoundError("Message not found")

    if (
        current_user_role != "admin"
        and message["sender_id"] != current_user_id
    ):
        raise ForbiddenError("Delivery Access Denied")

    if message["type"] == "group":
        report_rows = get_group_delivery_report(message_id)

    else:
        report_rows = get_direct_delivery_report(message_id)

    report = {
        "message_id": message_id,
        "pending": 0,
        "delivered": 0,
        "read": 0
    }

    total_users = 0

    for row in report_rows:

        report[row[0]] = row[1]
        total_users += row[1]

    report["total_users"] = total_users

    return report