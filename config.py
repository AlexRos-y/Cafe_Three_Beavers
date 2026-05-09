import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cafe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Яндекс.Карты
    YANDEX_MAPS_API_KEY = "7f9cd07c-0f26-4523-9f72-e4b7542a45d5"