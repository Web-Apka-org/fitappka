from datetime import datetime
import secrets
import jwt
from jwt.exceptions import InvalidTokenError

from django.conf import settings

from .models import User
from .exceptions import WrongTokenError, UserDoesNotExist


def generate(user_id: int) -> (str, str):
    '''
    Generate two tokens, first for authenticated access and second
    for generate new tokens (refresh).

    Throws TypeError.
    '''
    if not isinstance(user_id, int):
        raise TypeError('\'user_id\' must be int.')

    today = datetime.now()
    access_expire = int((
            today + settings.JWT_TOKEN_EXPIRE).timestamp()
    )
    refresh_expire = int((
            today + settings.JWT_REFRESH_TOKEN_EXPIRE).timestamp()
    )

    # access token
    access = jwt.encode(
        {'exp': access_expire},
        settings.PRIVATE_KEY,
        algorithm='EdDSA',
        headers={
            'user_id': user_id,
            'for': 'access',
            'secret': secrets.token_urlsafe(32)
        }
    )

    # refresh token
    refresh = jwt.encode(
        {'exp': refresh_expire},
        settings.PRIVATE_KEY,
        algorithm='EdDSA',
        headers={
            'user_id': user_id,
            'for': 'refresh',
            'secret': secrets.token_urlsafe(32)
        }
    )

    return access, refresh


def decode(token: str) -> dict:
    '''
    Return decoded token.

    Throws WrongTokenError.
    '''
    try:
        decoded = jwt.api_jwt.decode_complete(
            token,
            settings.PUBLIC_KEY,
            algorithms=['EdDSA']
        )
    except InvalidTokenError as ex:
        raise WrongTokenError(ex)
    else:
        return decoded


def decode_header(token: str) -> dict:
    '''
    Return only decoded header token.

    Throws WrongTokenError.
    '''
    try:
        decoded = jwt.api_jwt.decode_complete(
            token,
            settings.PUBLIC_KEY,
            algorithms=['EdDSA']
        )
    except InvalidTokenError as ex:
        raise WrongTokenError(ex)
    else:
        return decoded['header']


def get_user(token: str) -> User:
    '''
    Return User model instance from token.

    Throws TypeError and UserDoesNotExist exceptions.
    '''
    if not isinstance(token, str):
        raise TypeError('token must be str.')

    try:
        header = decode_header(token)
        user = User.objects.get(pk=header['user_id'])
    except InvalidTokenError as ex:
        raise WrongTokenError(ex)
    except User.ObjectDoesNotExist:
        raise UserDoesNotExist('User does not exist.')
    else:
        return user
