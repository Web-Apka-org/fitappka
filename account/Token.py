import logging
from datetime import datetime
import secrets
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

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
        addr = request.META['REMOTE_ADDR']

        if 'HTTP_TOKEN' not in request.META:
            logging.error(f'{addr} :: No token in HTTP header.')
            return False

        token = str(request.META['HTTP_TOKEN'])

        try:
            decoded_token = jwt.api_jwt.decode_complete(
                token,
                settings.PUBLIC_KEY,
                algorithms=['EdDSA']
            )

            header = decoded_token['header']

            if 'user_id' not in header:
                logging.error(f'{addr} :: No \'user_id\' in token header.')
                return False

            if 'for' not in header:
                logging.error(f'{addr} :: No \'for\' in token header.')
                return False

            if header['for'] != 'access':
                logging.error(f'{addr} :: This is not access token.')
                return False
        except InvalidTokenError as ex:
            logging.error(f'{addr} :: {ex}')
            return False
        except ExpiredSignatureError as ex:
            logging.error(f'{addr} :: {ex}')
            return False

        return True


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
    decoded: dict

    try:
        decoded = jwt.api_jwt.decode_complete(
            token,
            settings.PUBLIC_KEY,
            algorithms=['EdDSA']
        )
    except InvalidTokenError as ex:
        raise WrongTokenError(ex)

    return decoded


def decode_header(token: str) -> dict:
    '''
    Return only decoded header token.

    Throws WrongTokenError.
    '''
    decoded: dict

    try:
        decoded = jwt.api_jwt.decode_complete(
            token,
            settings.PUBLIC_KEY,
            algorithms=['EdDSA']
        )
    except InvalidTokenError as ex:
        raise WrongTokenError(ex)

    return decoded['header']


def get_user(token: str) -> User:
    '''
    Return User model instance from token.

    Throws TypeError and UserDoesNotExist exceptions.
    '''
    if not isinstance(token, str):
        raise TypeError('token must be str.')

    header = jwt.get_unverified_header(token)
    user: User

    try:
        user = User.objects.get(pk=header['user_id'])
    except User.ObjectDoesNotExist:
        raise UserDoesNotExist('User does not exist.')

    return user
