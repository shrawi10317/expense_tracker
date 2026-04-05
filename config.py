import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    DEBUG = os.getenv("DEBUG", "False") == "True"

    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
                "postgres://", "postgresql://", 1
            )
    else:
        MYSQL_HOST = os.getenv('MYSQL_DATABASE_HOST', 'localhost')
        MYSQL_PORT = int(os.getenv('MYSQL_DATABASE_PORT', 3306))
        MYSQL_USER = os.getenv('MYSQL_DATABASE_USER')
        MYSQL_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD')
        MYSQL_DB = os.getenv('MYSQL_DATABASE_DB')

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False