import os


class Config(object):
    ENV='production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SESSION_COOKIE_HTTPONLY=True
    #SESSION_COOKIE_SECURE=True
    #PREFERRED_URL_SCHEME='https'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/hard-to-crack-note-app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False