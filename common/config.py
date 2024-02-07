import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG", "FALSE").upper() == "TRUE"

DB_URI = os.environ.get("DB_URI")

if DB_URI is None:
    db_name = os.environ["DB_NAME"]
    db_username = os.environ["DB_USERNAME"]
    db_password = os.environ["DB_PASSWORD"]
    db_endpoint = os.environ.get("DB_ENDPOINT")

    if db_endpoint is None:
        db_port = os.environ["DB_PORT"]
        db_host = os.environ["DB_HOST"]
        db_endpoint = f"{db_host}:{db_port}"

    DB_URI = f"postgresql+asyncpg://{db_username}:{db_password}@{db_endpoint}/{db_name}"

SECRET = os.getenv("SECRET", "SecretPhrase1!")

LOG_DIR = 'logs'
