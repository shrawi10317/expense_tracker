from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import psycopg2
import app
# 1️⃣ Create db object here (without app)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

      # DB connection function
    def get_db_connection():
        return psycopg2.connect(app.config["DATABASE_URL"])

    app.get_db_connection = get_db_connection

    # 2️⃣ Initialize db with app
    db.init_app(app)

    # 3️⃣ Register blueprints here AFTER db exists
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.expenses import expenses_bp
    app.register_blueprint(expenses_bp)

    return app


