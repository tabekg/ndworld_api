import uuid
from datetime import datetime, timezone, timedelta
from functools import wraps

import jwt

from flask import request, g

from models.auth import AuthSession, AuthProvider
from models.user import User, Role
from utils.config import ACCESS_TOKEN_EXPIRE_DAYS, SECRET_KEY
from utils.exception import ResponseException


def create_access_token(data):
    return jwt.encode({
        **data,
        'iss': 'ndworld',
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }, SECRET_KEY, algorithm="HS256")


def check_auth_token(type_=None):
    token = request.headers['Authorization'][7:] if 'Authorization' in request.headers else None

    if not token:
        token = request.cookies.get('token')

    try:
        if not token:
            g.user = None
        else:
            data = jwt.decode(
                token,
                SECRET_KEY,
                options={"require": ["exp", "iss"]},
                issuer='ndworld',
                algorithms=["HS256"],
            )
            g.auth_session = g.db.query(AuthSession).filter(AuthSession.hash == data['sessionHash']).one()
            g.user = g.db.query(User) \
                .filter(User.id == g.auth_session.user_id, User.is_disabled.isnot(True)) \
                .first()
            g.role = g.auth_session.role if g.user else None
            if type_ == 'company':
                assert g.role and g.role.company
                g.company = g.role.company
                g.agency = None
            elif type_ == 'agency':
                assert g.role and g.role.agency
                g.agency = g.role.agency
                g.company = None
            else:
                g.company = None
                g.agency = None
    except Exception as e:
        raise ResponseException(payload=str(e), status='token_is_invalid', status_code=401)


def check_user(role=None, type_=None):
    if request.method == 'OPTIONS':
        return
    check_auth_token(type_)
    if not hasattr(g, 'user') or not g.user:
        raise ResponseException(payload='User not authorized', status='not_authorized', status_code=401)
    if role is not None:
        raise ResponseException(payload='The user has no permission', status='access_denied', status_code=403)


def auth_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def wrapped_function(*args, **kwargs):
            check_user(role=role)
            return fn(*args, **kwargs)

        return wrapped_function

    return wrapper


def agency_auth_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def wrapped_function(*args, **kwargs):
            check_user(role=role, type_='agency')
            return fn(*args, **kwargs)

        return wrapped_function

    return wrapper


def company_auth_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def wrapped_function(*args, **kwargs):
            check_user(role=role, type_='company')
            return fn(*args, **kwargs)

        return wrapped_function

    return wrapper


def create_auth_session(db, user_id: int, role_id: int = None, fcm_token=None):
    if role_id:
        assert db.query(Role).filter(Role.id == role_id, Role.user_id == user_id).one()

    session = AuthSession(user_id=user_id, role_id=role_id)

    session.hash = uuid.uuid4().hex
    session.fcm_token = fcm_token or None
    session.ip_address = request.remote_addr
    session.user_agent = request.headers.get('User-Agent')
    session.expired_at = datetime.now(tz=timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    session.is_active = True
    session.last_action_at = datetime.now(tz=timezone.utc)

    db.add(session)
    db.flush()

    return session


def create_auth_provider(db, user_id: int, name: str, identifier: str):
    provider = AuthProvider(user_id=user_id)

    provider.name = name
    provider.identifier = identifier or None

    db.add(provider)
    db.flush()

    return provider
