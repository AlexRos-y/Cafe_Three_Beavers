import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "three-beavers-secret-key-2026"
    SQLALCHEMY_DATABASE_URI = "sqlite:///cafe.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    YANDEX_MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY")
