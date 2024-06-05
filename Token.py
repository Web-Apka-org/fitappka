import logging
from datetime import datetime
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import secrets

from django.conf import settings

from account.models import User


def generate(user_id: int = None) -> str, str:
    '''
    Generate two tokens, first for authenticated access and second
    for generate new tokens (refresh).
    '''
    if user_id is None:
        raise TypeError('user_id is None')

    if not isinstance(user_id, int):
        raise TypeError('user_id must be int.')

    today = datetime.now()
    access_expire = int((
            today + settings.JWT_TOKEN_EXPIRE).timestamp()
    )
    refresh_expire = int((
            today + setting.JWT_REFRESH_TOKEN_EXPIRE).timestamp()
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


def get_user(token: str = None) -> Optional[User, None]:
    if token is None:
        raise TypeError('token is None')

    if not isinstance(token, str):
        raise TypeError('token must be str.')

    header: dict

    try:
        decoded_token = jwt.api_jwt.decode_complete(
            token,
            settings.PUBLIC_KEY,
            algorithms=['EdDSA']
        )

        header = decoded_token['header']
    except ExpiredSignatureError as ex:
        pass
    except InvalidTokenError as ex:
        pass

    if 'user_id' not in header:
        # logging here in future
        return None

    
