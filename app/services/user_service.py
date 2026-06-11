from repository.user_repository import get_user_by_id
from utils.exceptions import UserNotFoundError


# def fetch_user_by_email(email):

#     user = get_user_by_email(email)

#     if not user:
#         raise UserNotFoundError()

#     return {
#         "id": str(user[0]),
#         "name": user[1],
#         "email": user[2],
#         "role": user[3],
#         "created_at": user[4].isoformat()
#     }

def fetch_user(user_id):

    user = get_user_by_id(user_id)

    if not user:
        raise UserNotFoundError()

    return {
        "id": str(user[0]),
        "name": user[1],
        "email": user[2],
        "role": user[3],
        "created_at": user[4].isoformat()
    }