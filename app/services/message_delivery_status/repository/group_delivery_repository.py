from layers.common.psycopg.python.core.database import get_connection


def update_group_delivery_status(
    message_id,
    user_id,
    status
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if status == "delivered":

                cursor.execute(
                    """
                    UPDATE group_message_deliveries
                    SET
                        status = %s,
                        delivered_at = NOW()
                    WHERE message_id = %s
                    AND user_id = %s

                    RETURNING
                        message_id,
                        user_id,
                        status
                    """,
                    (
                        status,
                        message_id,
                        user_id
                    )
                )

            else:

                cursor.execute(
                    """
                    UPDATE group_message_deliveries
                    SET
                        status = %s,
                        read_at = NOW()
                    WHERE message_id = %s
                    AND user_id = %s

                    RETURNING
                        message_id,
                        user_id,
                        status
                    """,
                    (
                        status,
                        message_id,
                        user_id
                    )
                )

                connection.commit()
            return cursor.fetchone()

    finally:
        connection.close()


def get_group_delivery_report(message_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    status,
                    COUNT(*)
                FROM group_message_deliveries
                WHERE message_id = %s
                GROUP BY status
                """,
                (message_id,)
            )

            return cursor.fetchall()

    finally:
        connection.close()