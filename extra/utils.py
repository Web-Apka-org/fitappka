from datetime import datetime
from .exceptions import WrongDatetime


def getDatetime(date_str: str) -> datetime | None:
    len_date_str = len(date_str)

    try:
        if len_date_str == 10:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            raise ValueError('Incorrect date format. (accepted: %Y-%m-%d)')
    except ValueError as ex:
        raise WrongDatetime(ex)
    else:
        return date
