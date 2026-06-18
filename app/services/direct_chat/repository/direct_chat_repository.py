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
def get_existing_chat(user1_id, user2_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM direct_chats
                WHERE
                    (user1_id = %s AND user2_id = %s)
                    OR
                    (user1_id = %s AND user2_id = %s)
                """,
                (
                    user1_id,
                    user2_id,
                    user2_id,
                    user1_id
                )
            )

            return cursor.fetchone()

    finally:
        connection.close()


def create_direct_chat(user1_id, user2_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO direct_chats (
                    user1_id,
                    user2_id
                )
                VALUES (%s, %s)

                RETURNING
                    id,
                    user1_id,
                    user2_id,
                    created_at
                """,
                (
                    user1_id,
                    user2_id
                )
            )

            chat = cursor.fetchone()

            connection.commit()

            return {
                "id": str(chat[0]),
                "user1_id": str(chat[1]),
                "user2_id": str(chat[2]),
                "created_at": chat[3].isoformat()
            }

    finally:
        connection.close()


def get_direct_chats(user_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    dc.id,
                    dc.created_at,

                    u.id AS user_id,
                    u.name,
                    u.email

                FROM direct_chats dc

                JOIN users u
                ON (
                    (dc.user1_id = %s AND dc.user2_id = u.id)
                    OR
                    (dc.user2_id = %s AND dc.user1_id = u.id)
                )

                ORDER BY dc.created_at DESC
                """,
                (
                    user_id,
                    user_id
                )
            )
            chats = cursor.fetchall()

            return [
                {
                    "id": str(chat[0]),
                    "created_at": chat[1].isoformat(),
                    "user_id": str(chat[2]),
                    "name": chat[3],
                    "email": chat[4]
                }
                for chat in chats
            ]

    finally:
        connection.close()

def is_chat_participant(chat_id, user_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM direct_chats
                WHERE id = %s
                AND (
                    user1_id = %s
                    OR user2_id = %s
                )
                """,
                (
                    chat_id,
                    user_id,
                    user_id
                )
            )

            return cursor.fetchone()

    finally:
        connection.close()

#direct_message_delivery

def get_chat_receiver(
    chat_id,
    sender_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    CASE
                        WHEN user1_id = %s THEN user2_id
                        ELSE user1_id
                    END AS receiver_id
                FROM direct_chats
                WHERE id = %s
                """,
                (
                    sender_id,
                    chat_id
                )
            )

            receiver = cursor.fetchone()

            return str(receiver[0])

    finally:
        connection.close()      