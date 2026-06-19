from app.core.database import get_connection


def check_duplicate_message(
    sender_id,
    client_message_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM direct_messages
                WHERE sender_id = %s
                AND client_message_id = %s
                """,
                (
                    sender_id,
                    client_message_id
                )
            )

            return cursor.fetchone()

    finally:
        connection.close()


def create_direct_message(
    direct_chat_id,
    sender_id,
    client_message_id,
    content
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO direct_messages (
                    direct_chat_id,
                    sender_id,
                    client_message_id,
                    content
                )
                VALUES (%s, %s, %s, %s)

                RETURNING
                    id,
                    direct_chat_id,
                    sender_id,
                    client_message_id,
                    content,
                    created_at
                """,
                (
                    direct_chat_id,
                    sender_id,
                    client_message_id,
                    content
                )
            )

            message = cursor.fetchone()

            connection.commit()

            return {
                "id": str(message[0]),
                "direct_chat_id": str(message[1]),
                "sender_id": str(message[2]),
                "client_message_id": message[3],
                "content": message[4],
                "created_at": message[5].isoformat()
            }

    finally:
        connection.close()


def get_direct_messages(chat_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    dm.id,
                    dm.sender_id,
                    u.name,
                    dm.content,
                    dm.created_at

                FROM direct_messages dm

                JOIN users u
                ON dm.sender_id = u.id

                WHERE dm.direct_chat_id = %s

                ORDER BY dm.created_at ASC
                """,
                (chat_id,)
            )

            messages = cursor.fetchall()

            return [
                {
                    "id": str(message[0]),
                    "sender_id": str(message[1]),
                    "sender_name": message[2],
                    "content": message[3],
                    "created_at": message[4].isoformat()
                }
                for message in messages
            ]

    finally:
        connection.close()


def get_message_by_id(message_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    sender_id,
                    direct_chat_id
                FROM direct_messages
                WHERE id = %s
                """,
                (message_id,)
            )

            return cursor.fetchone()

    finally:
        connection.close()


def delete_direct_message(message_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM direct_messages
                WHERE id = %s
                """,
                (message_id,)
            )

            connection.commit()

    finally:
        connection.close()

#direct_message_delivery

def create_delivery_record(
    message_id,
    receiver_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO direct_message_deliveries (
                    message_id,
                    user_id
                )
                VALUES (%s, %s)
                """,
                (
                    message_id,
                    receiver_id
                )
            )

            connection.commit()

    finally:
        connection.close()
        
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