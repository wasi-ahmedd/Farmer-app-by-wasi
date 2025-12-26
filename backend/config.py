import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # ✅ FORCE PostgreSQL on Railway (NO SQLite fallback)
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGO = "HS256"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
