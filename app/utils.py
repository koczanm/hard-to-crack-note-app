import re
import uuid

from flask import session


def generate_xsrf_token():
    if '_xsrf_token' not in session:
        session['_xsrf_token'] = uuid.uuid4().hex

    return session['_xsrf_token']


def validate_username(username):
    if username is not None and re.match(r'^[a-zA-Z0-9_-]{4,16}$', username):
        return True

    return False


def validate_password(password):
    if password is not None and re.match(r'^[a-zA-Z0-9@$!%*?&]{8,32}$', password):
        return True

    return False


def validate_title(title):
    if title is not None and len(title) > 0 and len(title) < 16:
        return True

    return False


def valitdate_body(body):
    if body is not None and len(body) > 0 and len(body) < 128:
        return True

    return False
