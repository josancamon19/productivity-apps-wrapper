import datetime
from pytz import timezone


def get_today_str():
    return datetime.datetime.now(tz=timezone('America/Bogota')).strftime('%Y-%m-%d')


def get_today():
    return datetime.datetime.now(tz=timezone('America/Bogota')).date()
