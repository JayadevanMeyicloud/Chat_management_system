from core.database import get_connection


def is_duplicate_message(
    sender_id,
    client_message_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM group_messages
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


def create_message(
    group_id,
    sender_id,
    content,
    client_message_id=None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO group_messages (
                    group_id,
                    sender_id,
                    content,
                    client_message_id
                )
                VALUES (%s, %s, %s, %s)

                RETURNING
                    id,
                    group_id,
                    sender_id,
                    content,
                    created_at
                """,
                (
                    group_id,
                    sender_id,
                    content,
                    client_message_id
                )
            )

            message = cursor.fetchone()

            connection.commit()

            return {
                "id": str(message[0]),
                "group_id": str(message[1]),
                "sender_id": str(message[2]),
                "content": message[3],
                "created_at": message[4].isoformat()
            }

    finally:
        connection.close()


def get_messages(group_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    gm.id,
                    gm.group_id,
                    gm.sender_id,
                    u.name,
                    gm.content,
                    gm.created_at
                FROM group_messages gm
                JOIN users u
                    ON u.id = gm.sender_id
                WHERE gm.group_id = %s
                ORDER BY gm.created_at ASC
                """,
                (group_id,)
            )

            messages = cursor.fetchall()

            return [
                {
                    "id": str(message[0]),
                    "group_id": str(message[1]),
                    "sender_id": str(message[2]),
                    "sender_name": message[3],
                    "content": message[4],
                    "created_at": message[5].isoformat()
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
                    group_id,
                    sender_id,
                    content,
                    created_at
                FROM group_messages
                WHERE id = %s
                """,
                (message_id,)
            )

            message = cursor.fetchone()

            if not message:
                return None

            return {
                "id": str(message[0]),
                "group_id": str(message[1]),
                "sender_id": str(message[2]),
                "content": message[3],
                "created_at": message[4].isoformat()
            }

    finally:
        connection.close()


def delete_message(message_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM group_messages
                WHERE id = %s
                """,
                (message_id,)
            )

            connection.commit()

    finally:
        connection.close()

#create Delivery record

def create_delivery_records(
    message_id,
    member_ids
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            values = [
                (message_id, user_id)
                for user_id in member_ids
            ]

            cursor.executemany(
                """
                INSERT INTO group_message_deliveries (
                    message_id,
                    user_id
                )
                VALUES (%s, %s)
                """,
                values
            )

            connection.commit()

    finally:
        connection.close()