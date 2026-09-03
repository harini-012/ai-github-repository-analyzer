import json
from database import get_db_connection


def read_clob(value):
    """Convert Oracle CLOB to a normal Python string."""
    if value is None:
        return None

    if hasattr(value, "read"):
        return value.read()

    return value


def convert_files(value):
    """Convert stored CLOB/JSON data into a Python list."""
    value = read_clob(value)

    if not value:
        return []

    try:
        files = json.loads(value)

        if isinstance(files, list):
            return files

        return []

    except (json.JSONDecodeError, TypeError):
        return []


def save_repository(
    user_id,
    github_url,
    name,
    description,
    language,
    stars,
    forks,
    files
):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO repositories
        (
            user_id,
            github_url,
            name,
            description,
            language,
            stars,
            forks,
            files
        )
        VALUES
        (:1, :2, :3, :4, :5, :6, :7, :8)
        RETURNING id INTO :9
    """

    new_id = cursor.var(int)

    cursor.execute(
        query,
        (
            user_id,
            github_url,
            name,
            description,
            language,
            stars,
            forks,
            json.dumps(files),
            new_id
        )
    )

    connection.commit()

    repository_id = new_id.getvalue()[0]

    cursor.close()
    connection.close()

    return repository_id


def get_user_repositories(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            github_url,
            name,
            description,
            language,
            stars,
            forks,
            files,
            created_at
        FROM repositories
        WHERE user_id = :1
        ORDER BY created_at DESC
    """

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    repositories = []

    for row in rows:

        # IMPORTANT:
        # Read CLOB while connection is still open
        files = convert_files(row[7])

        repositories.append({
            "id": row[0],
            "github_url": row[1],
            "name": row[2],
            "description": row[3],
            "language": row[4],
            "stars": row[5],
            "forks": row[6],
            "files": files,
            "created_at": row[8]
        })

    cursor.close()
    connection.close()

    return repositories


def get_repository(repository_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            github_url,
            name,
            description,
            language,
            stars,
            forks,
            files,
            created_at
        FROM repositories
        WHERE id = :1
        AND user_id = :2
    """

    cursor.execute(
        query,
        (repository_id, user_id)
    )

    row = cursor.fetchone()

    if not row:
        cursor.close()
        connection.close()
        return None

    # IMPORTANT:
    # Convert CLOB BEFORE closing connection
    files = convert_files(row[7])

    repository = {
        "id": row[0],
        "github_url": row[1],
        "name": row[2],
        "description": row[3],
        "language": row[4],
        "stars": row[5],
        "forks": row[6],
        "files": files,
        "created_at": row[8]
    }

    cursor.close()
    connection.close()

    return repository


def delete_repository(repository_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM repositories
        WHERE id = :1
        AND user_id = :2
    """

    cursor.execute(
        query,
        (repository_id, user_id)
    )

    connection.commit()

    cursor.close()
    connection.close()