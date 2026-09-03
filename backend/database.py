import psycopg2
from config import Config


def get_db_connection():
    return psycopg2.connect(
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT,
        database=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD
    )


def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                github_url VARCHAR(500) NOT NULL,
                name VARCHAR(255),
                description TEXT,
                language VARCHAR(100),
                stars INTEGER DEFAULT 0,
                forks INTEGER DEFAULT 0,
                files TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_repository_user
                    FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id SERIAL PRIMARY KEY,
                repository_id INTEGER NOT NULL,
                summary TEXT,
                technologies TEXT,
                architecture TEXT,
                important_files TEXT,
                suggestions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_analysis_repository
                    FOREIGN KEY (repository_id)
                    REFERENCES repositories(id)
                    ON DELETE CASCADE
            );
        """)

        connection.commit()
        print("DATABASE INITIALIZATION SUCCESSFUL")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()