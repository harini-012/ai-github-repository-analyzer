from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(name, email, password):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        hashed_password = generate_password_hash(password)

        query = """
            INSERT INTO users
            (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        cursor.execute(
            query,
            (name, email, hashed_password)
        )

        user_id = cursor.fetchone()[0]

        connection.commit()

        return user_id

    finally:
        cursor.close()
        connection.close()


def get_user_by_email(email):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT id, name, email, password
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))

        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "password": row[3]
        }

    finally:
        cursor.close()
        connection.close()


def verify_password(password, hashed_password):

    return check_password_hash(
        hashed_password,
        password
    )