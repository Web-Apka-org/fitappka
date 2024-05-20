from datetime import datetime


def getDatetime(date_str):
    len_date_str = len(date_str)

    try:
        if len_date_str == 10:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        elif len_date_str == 16:
            date = datetime.strptime(date_str, '%Y-%m-%d,%H:%M')
        else:
            return None
    except ValueError as ve:
        return None

    return date
