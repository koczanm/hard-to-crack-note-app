import os


class Config(object):
    ENV='production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SECURE=True
    PREFERRED_URL_SCHEME='https'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False