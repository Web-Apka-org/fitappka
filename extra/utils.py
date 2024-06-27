from datetime import datetime
from .exceptions import WrongDateFormat


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

    raise WrongDateFormat(f'Incorrect date format (accepted: {formats})')
