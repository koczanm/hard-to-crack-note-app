from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app import routes

app.jinja_env.globals['xsrf_token'] = routes.generate_xsrf_token