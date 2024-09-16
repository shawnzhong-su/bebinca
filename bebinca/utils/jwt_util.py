from datetime import datetime, timedelta

import bcrypt  # python -m pip install bcrypt
import jwt  # python -m pip install pyjwt
from jwt.exceptions import ExpiredSignatureError

from bebinca.configs import settings
from bebinca.exts.logs import logger


def set_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def validate_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_token(data: dict):
    token_data = data.copy()  # data = {'id': 3}
    expiration_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expiration_time = datetime.now() + expiration_delta
    token_data.update({'exp': expiration_time.timestamp()})
    encoded_token = jwt.encode(token_data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_token


def extract_uid(token: str):
    decoded_payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    user_id = decoded_payload.get('id')
    user_id = int(user_id)
    return user_id


def verify_token(request):
    token = request.headers.get('Authorization')
    if not token:
        return None, 'token is missing'
    try:
        user_id = extract_uid(token)
    except (ExpiredSignatureError, InvalidTokenError):
        return None, 'invalid token'
    except Exception as e:
        logger.error(f'token verification error: {str(e)}')
        return None, 'token verification error'
    if not user_id:
        return None, 'user does not exist'
    return user_id, None
