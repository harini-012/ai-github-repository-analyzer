import json

from database import get_db_connection


def convert_files(value):

    if not value:
        return []

    if isinstance(value, list):
        return value

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

    try:

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
            (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """

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
                json.dumps(files)
            )
        )

        repository_id = cursor.fetchone()[0]

        connection.commit()

        return repository_id

    finally:

        cursor.close()
        connection.close()


def get_user_repositories(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

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
            WHERE user_id = %s
            ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))

        rows = cursor.fetchall()

        repositories = []

        for row in rows:

            repositories.append({
                "id": row[0],
                "github_url": row[1],
                "name": row[2],
                "description": row[3],
                "language": row[4],
                "stars": row[5],
                "forks": row[6],
                "files": convert_files(row[7]),
                "created_at": row[8]
            })

        return repositories

    finally:

        cursor.close()
        connection.close()


def get_repository(repository_id, user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

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
            WHERE id = %s
            AND user_id = %s
        """

        cursor.execute(
            query,
            (repository_id, user_id)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "github_url": row[1],
            "name": row[2],
            "description": row[3],
            "language": row[4],
            "stars": row[5],
            "forks": row[6],
            "files": convert_files(row[7]),
            "created_at": row[8]
        }

    finally:

        cursor.close()
        connection.close()


def delete_repository(repository_id, user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        query = """
            DELETE FROM repositories
            WHERE id = %s
            AND user_id = %s
        """

        cursor.execute(
            query,
            (repository_id, user_id)
        )

        connection.commit()

    finally:

        cursor.close()
        connection.close()