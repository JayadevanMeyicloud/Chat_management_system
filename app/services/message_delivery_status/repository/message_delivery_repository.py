from core.database import get_connection
def get_user_by_cognito_sub(cognito_sub):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE cognito_sub = %s
                """,
                (cognito_sub,)
            )

            return cursor.fetchone()

    finally:
        connection.close()
def get_message_type(message_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT sender_id
                FROM group_messages
                WHERE id = %s
                """,
                (message_id,)
            )

            group_message = cursor.fetchone()

            if group_message:
                return {
                    "type": "group",
                    "sender_id": str(group_message[0])
                }

            cursor.execute(
                """
                SELECT sender_id
                FROM direct_messages
                WHERE id = %s
                """,
                (message_id,)
            )

            direct_message = cursor.fetchone()

            if direct_message:
                return {
                    "type": "direct",
                    "sender_id": str(direct_message[0])
                }

            return None

    finally:
        connection.close()