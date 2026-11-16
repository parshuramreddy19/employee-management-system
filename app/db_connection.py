
import os
import psycopg
from dotenv import load_dotenv


# Load environment variables from app/.env
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env")
)


def get_connection():

    db_config = {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT")
    }

    # Check whether any database settings are missing
    missing_settings = [
        key for key, value in db_config.items()
        if not value
    ]

    if missing_settings:
        raise ValueError(
            f"Missing database settings: {', '.join(missing_settings)}"
        )

    # Connect to PostgreSQL
    connection = psycopg.connect(**db_config)

    return connection
