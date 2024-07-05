from datetime import datetime

from rest_framework.response import Response

from .exceptions import WrongDateFormatError


def getDatetime(date_str: str, formats=['%Y-%m-%d']) -> datetime:
    if not isinstance(formats, list):
        raise TypeError('\'formats\' must be list.')

    for format in formats:
        try:
            date = datetime.strptime(date_str, format)
        except ValueError:
            continue
        else:
            return date

    raise WrongDateFormatError(f'Incorrect date format (accepted: {formats})')


def ErrorResponse(message: str = None, status=403):
    return Response(
        {
            'Error': str(message)
        },
        status=status
    )
