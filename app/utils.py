import re


def regex_validate_username(username):
    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', username):
        return True

    return False


def regex_validate_password(password):
    if re.match(r'^[a-zA-Z0-9@$!%*?&]{8,32}$', password):
        return True

    return False
