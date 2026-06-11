from core.database import get_connection


def is_group_member(
    group_id,
    user_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT 1
                FROM group_members
                WHERE group_id = %s
                AND user_id = %s
                """,
                (
                    group_id,
                    user_id
                )
            )

            return cursor.fetchone()

    finally:
        connection.close()