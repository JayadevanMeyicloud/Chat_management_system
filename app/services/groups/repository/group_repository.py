from core.database import get_connection


# def get_group_by_id(group_id):
#     connection = get_connection()

#     try:
#         with connection.cursor() as cursor:

#             cursor.execute(
#                 """
#                 SELECT id
#                 FROM groups
#                 WHERE id = %s
#                 AND deleted_at IS NULL
#                 """,
#                 (group_id,)
#             )

#             return cursor.fetchone()

#     finally:
#         connection.close()
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

def get_group_by_name(name):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM groups
                WHERE name = %s
                """,
                (name,)
            )

            return cursor.fetchone()

    finally:
        connection.close()


def create_group(
    name,
    description,
    created_by
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO groups (
                    name,
                    description,
                    created_by
                )
                VALUES (%s, %s, %s)

                RETURNING
                    id,
                    name,
                    description,
                    created_by,
                    created_at
                """,
                (
                    name,
                    description,
                    created_by
                )
            )

            group = cursor.fetchone()

            connection.commit()

            return {
                "id": str(group[0]),
                "name": group[1],
                "description": group[2],
                "created_by": str(group[3]),
                "created_at": group[4].isoformat()
            }

    finally:
        connection.close()


def get_groups():
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
                WHERE deleted_at IS NULL
                ORDER BY created_at DESC
                """
            )

            groups = cursor.fetchall()

            return [
                {
                    "id": str(group[0]),
                    "name": group[1],
                    "description": group[2],
                    "created_by": str(group[3]),
                    "created_at": group[4].isoformat()
                }
                for group in groups
            ]

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


def delete_group(group_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE groups
                SET deleted_at = NOW()
                WHERE id = %s
                """,
                (group_id,)
            )

            connection.commit()

    finally:
        connection.close()


def update_group_settings(
    group_id,
    name,
    description
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE groups
                SET
                    name = %s,
                    description = %s,
                    updated_at = NOW()
                WHERE id = %s

                RETURNING
                    id,
                    name,
                    description,
                    updated_at
                """,
                (
                    name,
                    description,
                    group_id
                )
            )

            group = cursor.fetchone()

            connection.commit()

            return {
                "id": str(group[0]),
                "name": group[1],
                "description": group[2],
                "updated_at": group[3].isoformat()
            }

    finally:
        connection.close()
def get_user_role(user_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT role
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )

            role = cursor.fetchone()

            return role[0] if role else None

    finally:
        connection.close()
