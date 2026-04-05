import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST=os.getenv('MYSQL_DATABASE_HOST','localhost')
    MYSQL_PORT=int(os.getenv('MYSQL_DATABASE_PORT',3306))
    MYSQL_USER=os.getenv('MYSQL_DATABASE_USER')
    MYSQL_PASSWORD=os.getenv('MYSQL_DATABASE_PASSWORD')
    MYSQL_DB=os.getenv('MYSQL_DATABASE_DB')
    MYSQL_CHARSET=os.getenv('MYSQL_DATABASE_CHARSET','utf8mb4')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    SECRET_KEY=os.getenv('SECRET_KEY')


