import logging
from datetime import datetime
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import secrets

from django.conf import settings
from rest_framework.permissions import BasePermission

from account.models import User


class WrongTokenError(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class JWTPermission(BasePermission):
    '''
    JWT based authentication.
    '''

    def has_permission(self, request, view) -> True | False:
        logger = logging.getLogger(__name__)
        addr = request.META['REMOTE_ADDR']
        token = str(request.META['HTTP_TOKEN'])

        try:
            decoded_token = jwt.api_jwt.decode_complete(
                token,
                settings.PUBLIC_KEY,
                algorithms=['EdDSA']
            )

            header = decoded_token['header']

            if 'user_id' not in header:
                logger.error(f'{addr} :: No \'user_id\' in token header')
                return False

            if 'for' not in header:
                logger.error(f'{addr} :: No \'for\' in token header')
                return False

            if header['for'] != 'access':
                logger.error(f'{addr} :: This is not acces token.')
                return False
        except InvalidTokenError as ex:
            logger.error(f'{addr} :: {ex}')
            return False
        except ExpiredSignatureError as ex:
            logger.error(f'{addr} :: {ex}')
            return False

        return True


def generate(user_id: int = None) -> (str, str):
    '''
    Generate two tokens, first for authenticated access and second
    for generate new tokens (refresh).

    Throws TypeError.
    '''
    if user_id is None:
        raise TypeError('user_id is None')

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
        settings.PRIVIATE_KEY,
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
        algorithm='EdDSA',
        headers={
            'user_id': user_id,
            'for': 'refresh',
            'secret': secrets.token_urlsafe(32)
        }
    )

    return access, refresh


def get_user(token: str = None) -> User:
    '''
    Return User model instance from token.

    Throws TypeError and UserDoesNotExist exceptions.
    '''
    if token is None:
        raise TypeError('token is None')

    if not isinstance(token, str):
        raise TypeError('token must be str.')

    header = jwt.get_unverified_header(token)
    user: User

    try:
        user = User.objects.get(pk=header['user_id'])
    except User.ObjectDoesNotExist:
        raise UserDoesNotExist('User does not exist.')

    return user
