import datetime
from pytz import timezone
import os


def get_today_str():
    return datetime.datetime.now(tz=timezone(os.getenv('SYNC_TIMEZONE'))).strftime('%Y-%m-%d')


def get_today():
    return datetime.datetime.now(tz=timezone(os.getenv('SYNC_TIMEZONE'))).date()
