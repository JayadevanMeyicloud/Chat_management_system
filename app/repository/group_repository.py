from core.database import get_connection


def get_group_by_id(group_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM groups
                WHERE id = %s
                AND deleted_at IS NULL
                """,
                (group_id,)
            )

            return cursor.fetchone()

    finally:
        connection.close()

def get_group_members(group_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT user_id
                FROM group_members
                WHERE group_id = %s
                """,
                (group_id,)
            )

            return [
                str(member[0])
                for member in cursor.fetchall()
            ]

    finally:
        connection.close()