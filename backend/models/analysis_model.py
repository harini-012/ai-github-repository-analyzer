from database import get_db_connection


def save_analysis(
    repository_id,
    summary,
    technologies,
    architecture,
    important_files,
    suggestions
):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO analyses
            (
                repository_id,
                summary,
                technologies,
                architecture,
                important_files,
                suggestions
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        cursor.execute(
            query,
            (
                repository_id,
                summary,
                technologies,
                architecture,
                important_files,
                suggestions
            )
        )

        analysis_id = cursor.fetchone()[0]

        connection.commit()

        return analysis_id

    finally:

        cursor.close()
        connection.close()


def get_analysis(repository_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        query = """
            SELECT
                id,
                repository_id,
                summary,
                technologies,
                architecture,
                important_files,
                suggestions,
                created_at
            FROM analyses
            WHERE repository_id = %s
            ORDER BY created_at DESC
        """

        cursor.execute(
            query,
            (repository_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "repository_id": row[1],
            "summary": row[2],
            "technologies": row[3],
            "architecture": row[4],
            "important_files": row[5],
            "suggestions": row[6],
            "created_at": row[7]
        }

    finally:

        cursor.close()
        connection.close()