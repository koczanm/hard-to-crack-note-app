from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.utils import generate_xsrf_token
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.globals['xsrf_token'] = generate_xsrf_token

db = SQLAlchemy(app)

from app import routes
