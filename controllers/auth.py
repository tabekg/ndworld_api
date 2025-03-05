from datetime import datetime, timezone, timedelta
from functools import wraps

import jwt

from flask import request, g

from utils.config import ACCESS_TOKEN_EXPIRE_DAYS, SECRET_KEY
from utils.exception import ResponseException


def create_access_token(data):
    return jwt.encode({
        **data,
        'iss': 'ndworld',
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }, SECRET_KEY, algorithm="HS256")


def check_auth_token():
    token = request.headers['Authorization'][7:] if 'Authorization' in request.headers else None
    try:
        if not token:
            g.user = None
        else:
            data = jwt.decode(
                token,
                SECRET_KEY,
                options={"require": ["exp", "iss"]},
                issuer='besoft:cloud',
                algorithms=["HS256"],
            )
            # TODO: user model
            # g.user = g.db.query(User) \
            #     .filter_by(id=data['id']) \
            #     .first()
            # if g.user and g.user.is_disabled is True:
            #     g.user = None
    except Exception as e:
        raise ResponseException(payload=str(e), status='token_is_invalid', status_code=401)


def check_user(roles=None):
    if request.method == 'OPTIONS':
        return
    check_auth_token()
    if not hasattr(g, 'user') or not g.user:
        raise ResponseException(payload='User not authorized', status='not_authorized', status_code=401)
    if roles is not None and g.user.role not in roles:
        raise ResponseException(payload='The user has no permission', status='access_denied', status_code=403)


def auth_required(roles=None):
    def wrapper(fn):
        @wraps(fn)
        def wrapped_function(*args, **kwargs):
            check_user(roles=roles)
            return fn(*args, **kwargs)

        return wrapped_function

    return wrapper
