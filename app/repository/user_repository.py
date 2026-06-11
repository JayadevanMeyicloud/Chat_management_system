from core.database import get_connection


def create_user(cognito_sub, name, email):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (cognito_sub, name, email)
                VALUES (%s, %s, %s)
                RETURNING id, cognito_sub, name, email, role
                """,
                (cognito_sub, name, email)
            )

            user = cursor.fetchone()
            connection.commit()

            return user

    finally:
        connection.close()

def get_user_by_id(user_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email,
                    role,
                    created_at
                FROM users
                WHERE id = %s
                AND deleted_at IS NULL
                """,
                (user_id,)
            )

            return cursor.fetchone()

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