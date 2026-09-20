import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "novatech-super-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "novatech-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database', 'novatech.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
