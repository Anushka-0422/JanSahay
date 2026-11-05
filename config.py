import os
from dotenv import load_dotenv
from flask import render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.engine import URL

from app.models import User
from app.routes import auth
from app.routes import auth

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    # JWT Cookie Configuration
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_CSRF_CHECK_FORM = True

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False