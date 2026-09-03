import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")