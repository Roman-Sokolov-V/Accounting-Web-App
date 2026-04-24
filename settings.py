import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE = "postgres"
# DATABASE = "sqlite"

if DATABASE == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{'db.sqlite3'}"

elif DATABASE == "postgres":
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB}"
    )
