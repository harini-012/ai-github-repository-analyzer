from database import get_db_connection


def read_clob(value):
    """
    Safely read an Oracle CLOB while the database
    connection is still open.
    """

    if value is None:
        return None

    if hasattr(value, "read"):
        return value.read()

    return value


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
            (
                :1,
                :2,
                :3,
                :4,
                :5,
                :6
            )
            RETURNING id INTO :7
        """

        new_id = cursor.var(int)

        cursor.execute(
            query,
            (
                repository_id,
                summary,
                technologies,
                architecture,
                important_files,
                suggestions,
                new_id
            )
        )

        connection.commit()

        analysis_id = new_id.getvalue()[0]

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
            WHERE repository_id = :1
            ORDER BY created_at DESC
        """

        cursor.execute(
            query,
            (repository_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        # IMPORTANT:
        # Read CLOBs BEFORE closing the connection.

        summary = read_clob(row[2])
        technologies = read_clob(row[3])
        architecture = read_clob(row[4])
        important_files = read_clob(row[5])
        suggestions = read_clob(row[6])

        analysis = {
            "id": row[0],
            "repository_id": row[1],
            "summary": summary,
            "technologies": technologies,
            "architecture": architecture,
            "important_files": important_files,
            "suggestions": suggestions,
            "created_at": row[7]
        }

        return analysis

    finally:

        cursor.close()
        connection.close()