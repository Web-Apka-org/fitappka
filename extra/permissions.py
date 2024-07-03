import logging
from jwt import InvalidTokenError

from rest_framework.permissions import BasePermission

from account.models import User
from . import Token


class JWTPermission(BasePermission):
    '''
    JWT based authentication.
    '''

    def has_permission(self, request, view) -> True | False:
        addr = request.META['REMOTE_ADDR']

        if 'HTTP_TOKEN' not in request.META:
            logging.error(f'{addr} :: No token in HTTP header.')
            return False

        token = request.META['HTTP_TOKEN']
        header: dict

        try:
            header = Token.decode_header(token)

            # check if user still exist
            User.objects.get(pk=header['user_id'])

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
        except User.DoesNotExist:
            logging.error(f'{addr} :: User does not exist.')
            return False
        else:
            return True
