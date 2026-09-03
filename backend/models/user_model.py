from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(name, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    query = """
        INSERT INTO users
        (name, email, password)
        VALUES (:1, :2, :3)
        RETURNING id INTO :4
    """

    new_id = cursor.var(int)

    cursor.execute(
        query,
        (name, email, hashed_password, new_id)
    )

    connection.commit()

    user_id = new_id.getvalue()[0]

    cursor.close()
    connection.close()

    return user_id


def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, name, email, password
        FROM users
        WHERE email = :1
    """

    cursor.execute(query, (email,))

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "password": row[3]
    }


def verify_password(password, hashed_password):
    return check_password_hash(
        hashed_password,
        password
    )