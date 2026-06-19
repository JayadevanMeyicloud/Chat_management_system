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
        
def get_group_by_id(group_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    created_by,
                    created_at
                FROM groups
                WHERE id = %s
                AND deleted_at IS NULL
                """,
                (group_id,)
            )

            group = cursor.fetchone()

            if not group:
                return None

            return {
                "id": str(group[0]),
                "name": group[1],
                "description": group[2],
                "created_by": str(group[3]),
                "created_at": group[4].isoformat()
            }

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
        
def is_group_admin(
    group_id,
    user_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM groups
                WHERE id = %s
                AND created_by = %s
                AND deleted_at IS NULL
                """,
                (
                    group_id,
                    user_id
                )
            )

            return cursor.fetchone()

    finally:
        connection.close()
        
def is_member_exists(
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


def add_group_member(
    group_id,
    user_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO group_members (
                    group_id,
                    user_id
                )
                VALUES (%s, %s)

                RETURNING
                    group_id,
                    user_id,
                    joined_at
                """,
                (
                    group_id,
                    user_id
                )
            )

            member = cursor.fetchone()

            connection.commit()

            return {
                "group_id": str(member[0]),
                "user_id": str(member[1]),
                "joined_at": member[2].isoformat()
            }

    finally:
        connection.close()

def remove_group_member(
    group_id,
    user_id
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM group_members
                WHERE group_id = %s
                AND user_id = %s
                """,
                (
                    group_id,
                    user_id
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

def get_user_by_id(user_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )

            return cursor.fetchone()

    finally:
        connection.close()