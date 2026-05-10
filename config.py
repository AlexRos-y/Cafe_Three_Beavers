import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cafe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
